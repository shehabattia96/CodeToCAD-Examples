from CodeToCAD import *


class PillowBlock:

    wallThicknessRadius = Dimension.fromString("2mm")
    baseHeight = Dimension.fromString("2mm")

    setScrewRadius = Dimension.fromString("3/2mm")

    mountScrewRadius = Dimension.fromString("5/2mm")

    def __init__(self, holeRadius: Dimension, width: Dimension) -> None:
        self.holeRadius = holeRadius
        self.width = width

    def create(self):
        blockRadius = self.holeRadius + self.wallThicknessRadius

        block = Part("pillowBlock").createCube(
            blockRadius*2,
            self.width,
            blockRadius*2,
        )

        block.filletFaces("4mm", [block.getLandmark(
            PresetLandmark.top)], useWidth=True)

        frontLocation = block.getLandmark(
            PresetLandmark.front).getLocationLocal()
        frontHoleLocation = block.createLandmark(
            "frontHole", frontLocation.x, frontLocation.y - "1mm", frontLocation.z)
        block.hole(frontHoleLocation,
                   self.holeRadius, self.width, normalAxis="y", flipAxis=True)

        block.hole(block.getLandmark(landmarkName=PresetLandmark.top),
                   self.setScrewRadius, self.wallThicknessRadius * 2)

        mountScrewPadding = Dimension.fromString("2mm")
        mountScrewRadiusWithPadding = self.mountScrewRadius + mountScrewPadding

        blockBase = Part("pillowBlockBase").createCube(
            blockRadius * 2 + (mountScrewRadiusWithPadding * 4), self.width + mountScrewPadding * 2, self.baseHeight)

        blockBase.filletFaces("2mm", [blockBase.getLandmark(
            PresetLandmark.top)], useWidth=True)

        blockBaseLeftLocation = blockBase.getLandmark(
            PresetLandmark.leftTop).getLocationLocal()
        blockBaseHoleLocation = blockBase.createLandmark(
            "mountHole", blockBaseLeftLocation.x + mountScrewRadiusWithPadding, blockBaseLeftLocation.y, blockBaseLeftLocation.z)
        blockBase.hole(blockBaseHoleLocation, self.mountScrewRadius,
                       self.baseHeight, mirror=True, mirrorAboutEntityOrLandmark=blockBase)

        Joint(block.getLandmark(PresetLandmark.bottom), blockBase.getLandmark(
            PresetLandmark.top)).limitLocationXYZ(0, 0, 0)

        return block.union(blockBase)


if __name__ == "__main__":
    Scene.default().setDefaultUnit("mm")

    holeRadius = Dimension.fromString("5mm")
    width = Dimension.fromString("3mm")
    PillowBlock(holeRadius, width).create()

    from ballBearing import BallBearing

    ballBearing = BallBearing(width - "1mm", holeRadius, Dimension.fromString(
        "5/2mm"), holeRadius * 0.1).create(isCombinePartsIntoOne=True).rotateX(90)
