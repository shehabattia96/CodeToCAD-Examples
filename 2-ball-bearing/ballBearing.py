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

    def create(self, isCombinePartsIntoOne=False) -> CodeToCADInterface.Part:
        grooveInnerRadius = self.innerRadius - self.grooveDepth

        ballBearingOuterHoleRadius = self.innerRadius + \
            self.ballRadius * 2 - self.grooveDepth * 2

        # MARK: create inner and outer bearing bodies:

        ballBearingOuter = Part("ballBearingOuter").createCylinder(
            self.outerRadius,
            self.width
        )

        ballBearingOuter.hole(ballBearingOuter.getLandmark(
            PresetLandmark.top), ballBearingOuterHoleRadius,
            self.width)

        ballBearingInner = Part("ballBearingInner").createCylinder(
            self.innerRadius,

            self.width
        )

        ballBearingInner.hole(ballBearingInner.getLandmark(
            PresetLandmark.top), self.shaftRadius,
            self.width)

        # MARK: Create groove

        ballBearingInnerGroove = Part("ballBearingInnerGroove").createTorus(grooveInnerRadius,
                                                                            grooveInnerRadius + self.ballRadius * 2)

        ballBearingInner.subtract(
            ballBearingInnerGroove, deleteAfterSubtract=False)
        ballBearingOuter.subtract(
            ballBearingInnerGroove)

        # MARK: create balls

        ball = Part("ball").createSphere(self.ballRadius)

        Joint(ballBearingInner, ball).limitRotationXYZ(0, 0, 0)
        Joint(ballBearingInner, ballBearingOuter).limitRotationXYZ(
            0, 0, None)

        Joint(ballBearingInner.getLandmark(PresetLandmark.left), ball.getLandmark(
            PresetLandmark.right)).limitLocationXYZ(self.grooveDepth, 0, 0)

        ball.circularPattern(9, 360/9, ballBearingInner)

        return ballBearingInner if not isCombinePartsIntoOne else ballBearingInner.union(ballBearingOuter).union(ball).rename("ballBearing")


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
    ).create()
