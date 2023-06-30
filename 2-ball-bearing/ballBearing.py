from CodeToCAD import *


class BallBearing:

    def __init__(self, width: Dimension, outerRadius: Dimension, shaftRadius: Dimension, ballRadius: Dimension) -> None:
        self.width = width
        self.outerRadius = outerRadius
        self.shaftRadius = shaftRadius
        self.ballRadius = ballRadius

        self.grooveDepth = ballRadius * 0.3

        self.innerRadius = (outerRadius - shaftRadius -
                            ballRadius - self.grooveDepth) / 2 + shaftRadius

    # late initialization
    ballBearingOuter: CodeToCADInterface.Part
    ballBearingInner: CodeToCADInterface.Part
    ball: CodeToCADInterface.Part

    def create(self):
        grooveInnerRadius = self.innerRadius - self.grooveDepth

        ballBearingOuterHoleRadius = self.innerRadius + \
            self.ballRadius * 2 - self.grooveDepth * 2

        # MARK: create inner and outer bearing bodies:

        self.ballBearingOuter = Part("ballBearingOuter").createCylinder(
            self.outerRadius,
            self.width
        )

        self.ballBearingOuter.hole(self.ballBearingOuter.getLandmark(
            PresetLandmark.top), ballBearingOuterHoleRadius,
            self.width)

        self.ballBearingInner = Part("ballBearingInner").createCylinder(
            self.innerRadius,

            self.width
        )

        self.ballBearingInner.hole(self.ballBearingInner.getLandmark(
            PresetLandmark.top), self.shaftRadius,
            self.width)

        # MARK: Create groove

        ballBearingInnerGroove = Part("ballBearingInnerGroove").createTorus(grooveInnerRadius,
                                                                            grooveInnerRadius + self.ballRadius * 2)

        self.ballBearingInner.subtract(
            ballBearingInnerGroove, deleteAfterSubtract=False)
        self.ballBearingOuter.subtract(
            ballBearingInnerGroove)

        # MARK: create balls

        self.ball = Part("ball").createSphere(self.ballRadius)

        Joint(self.ballBearingInner, self.ball).limitRotationXYZ(0, 0, 0)
        Joint(self.ballBearingInner, self.ballBearingOuter).limitRotationXYZ(
            0, 0, None)

        Joint(self.ballBearingInner.getLandmark(PresetLandmark.left), self.ball.getLandmark(
            PresetLandmark.right)).limitLocationXYZ(self.grooveDepth, 0, 0)

        self.ball.circularPattern(9, 360/9, self.ballBearingInner)

        return self

    def setMaterial(self):
        # SA: this won't work anymore if combinePartsIntoOne is called.

        ballBearingMaterial = Material("ballBearing").setReflectivity(1.0)

        self.ballBearingOuter.setMaterial(ballBearingMaterial)
        self.ballBearingInner.setMaterial(ballBearingMaterial)
        self.ball.setMaterial(ballBearingMaterial)

        return self

    def combinePartsIntoOne(self) -> CodeToCADInterface.Part:
        return self.ballBearingInner.union(self.ballBearingOuter).union(self.ball).rename("ballBearing")


if __name__ == "__main__":
    Scene.default().setDefaultUnit("mm")

    width = Dimension.fromString("16mm")

    shaftRadius = Dimension.fromString("30/2mm")

    ballRadius = Dimension.fromString("9.53/2mm")

    outerRadius = Dimension.fromString("62/2mm")

    BallBearing(
        width=width,
        outerRadius=outerRadius,
        shaftRadius=shaftRadius,
        ballRadius=ballRadius
    ).create().setMaterial()
