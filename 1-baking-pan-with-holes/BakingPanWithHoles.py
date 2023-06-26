from CodeToCAD import *

Scene.default().setDefaultUnit("mm")


class BakingPan:
    width = "300mm"
    length = "350mm"
    height = "33.5mm"

    thickness = Dimension.fromString("3.5mm")
    wallDraftAngle = 180-100

    shelfWidth = Dimension.fromString("20mm")

    # fillets
    outerCornerRadius = "70mm"
    bottomEdgesRadius = "10mm"
    topEdgesInnerRadius = "5mm"
    topEdgesOuterRadius = "1mm"

    # holes
    numberOfHolesX = 6
    numberOfHolesY = 9
    holeRadius = Dimension.fromString("17/2mm")

    # late initialization
    pan: CodeToCADInterface.Part

    def createPanBody(self):

        self.pan = Part("pan").createCube(
            self.width,
            self.length,
            self.height)

        self.pan.hollow(
            self.shelfWidth*2,
            self.shelfWidth*2,
            self.thickness/2)

    def filletCorners(self, part: CodeToCADInterface.Part) -> CodeToCADInterface.Part:

        panCornerEdges = [PresetLandmark.leftBack, PresetLandmark.leftFront,
                          PresetLandmark.rightBack, PresetLandmark.rightFront]
        panCornerOuterAndInnerEdgePairs: list[list[CodeToCADInterface.LandmarkOrItsName]] = [
        ]

        for edge in panCornerEdges:
            edgeLandmark = part.getLandmark(edge)

            edgeLandmarkLocation = edgeLandmark.getLocationLocal()

            # right/left are x-axis, front/back are y-axis, relative positions respectively
            offsetX = self.shelfWidth * (-1 if "right" in edge.name else 1)
            offsetY = self.shelfWidth * (1 if "Front" in edge.name else -1)

            edgeLandmarkInner = part.createLandmark(
                edge.name + "Inner", edgeLandmarkLocation.x + offsetX, edgeLandmarkLocation.y + offsetY, edgeLandmarkLocation.z)

            panCornerOuterAndInnerEdgePairs.append(
                [edgeLandmark, edgeLandmarkInner])

        for pair in panCornerOuterAndInnerEdgePairs:
            part.filletEdges(
                self.outerCornerRadius, pair, useWidth=True
            )

        return part

    def filletBottomInnerEdges(self):

        self.pan.filletFaces(self.bottomEdgesRadius, [
                             self.pan.getLandmark("bottomInner")])

    def createBottomInnerLandmarks(self):

        panBottomLocation = self.pan.getLandmark(
            PresetLandmark.bottom).getLocationLocal()
        panBottomInner = self.pan.createLandmark(
            "bottomInner", panBottomLocation.x + self.holeRadius * 2, panBottomLocation.y, panBottomLocation.z + self.thickness)
        panHoleLocation = self.pan.createLandmark(
            "hole", panBottomLocation.x + self.holeRadius * 2, panBottomLocation.y, panBottomLocation.z)

    def createBottomHoles(self):
        panHoleLocation = self.pan.getLandmark("hole")
        self.pan.hole(panHoleLocation, self.holeRadius, self.thickness,
                      linearPatternInstanceCount=self.numberOfHolesX//2, linearPatternInstanceSeparation=self.holeRadius*4, linearPattern2ndInstanceCount=self.numberOfHolesY//2, linearPattern2ndInstanceSeparation=self.holeRadius*4, linearPattern2ndInstanceAxis="y", flipAxis=True, mirror=True, mirrorAboutEntityOrLandmark=self.pan.getLandmark(PresetLandmark.center), mirrorAxis="x")
        self.pan.hole(panHoleLocation, self.holeRadius, self.thickness,
                      linearPatternInstanceCount=self.numberOfHolesX//2, linearPatternInstanceSeparation=self.holeRadius*4, linearPattern2ndInstanceCount=self.numberOfHolesY//2, linearPattern2ndInstanceSeparation=self.holeRadius*-4, linearPattern2ndInstanceAxis="y", flipAxis=True, mirror=True, mirrorAboutEntityOrLandmark=self.pan.getLandmark(PresetLandmark.center), mirrorAxis="x")

    def createShelf(self):
        shelf = Part("shelf").createCube(
            self.width,
            self.length,
            Dimension.fromString(self.height) - self.thickness)

        shelf.hollow(
            self.shelfWidth*2 - self.thickness,
            self.shelfWidth*2 - self.thickness,
            0)

        shelf = self.filletCorners(part=shelf)

        Joint(self.pan.getLandmark(PresetLandmark.bottom), shelf.getLandmark(
            PresetLandmark.bottom)).limitLocationXYZ(0, 0, 0)

        self.pan.subtract(shelf)

    def create(self):

        self.createPanBody()

        self.pan = self.filletCorners(self.pan)

        self.createBottomInnerLandmarks()

        self.filletBottomInnerEdges()

        self.createBottomHoles()

        self.createShelf()

        material = Material("granite").addImageTexture(
            "./Granite07small_3K_BaseColor.png")

        self.pan.setMaterial(material)


if __name__ == "__main__":
    BakingPan().create()
