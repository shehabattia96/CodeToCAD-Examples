from CodeToCAD import *


class BallBearing:

    shaftRadius = Dimension.fromString("30/2mm")

    ballRadius = Dimension.fromString("9.53/2mm")

    ballGroovePadding = Dimension.fromString("3.235mm")

    ballBearingOuterRadius = Dimension.fromString("62/2mm")
    ballBearingInnerRadius = Dimension.fromString("40.4/2mm")

    ballBearingInnerGrooveDepth = Dimension.fromString("1.95mm")

    def create(self) -> CodeToCADInterface.Part:
        grooveInnerRadius = self.ballBearingInnerRadius - self.ballBearingInnerGrooveDepth

        ballBearingOuterHoleRadius = self.ballBearingInnerRadius + \
            self.ballRadius * 2 - self.ballBearingInnerGrooveDepth * 2

        ballBearingWidth = self.ballRadius * 2 + self.ballGroovePadding * 2

        ballBearingOuter = Part("ballBearingOuter").createCylinder(
            self.ballBearingOuterRadius,
            ballBearingWidth
        )

        ballBearingOuter.hole(ballBearingOuter.getLandmark(
            PresetLandmark.top), ballBearingOuterHoleRadius, ballBearingWidth)

        ballBearingInner = Part("ballBearingInner").createCylinder(
            self.ballBearingInnerRadius,
            ballBearingWidth
        )

        ballBearingInnerGroove = Part("ballBearingInnerGroove").createTorus(grooveInnerRadius,
                                                                            grooveInnerRadius + self.ballRadius * 2)

        ballBearingInner.subtract(
            ballBearingInnerGroove, deleteAfterSubtract=False)
        ballBearingOuter.subtract(
            ballBearingInnerGroove)

        ballBearingInner.hole(ballBearingInner.getLandmark(
            PresetLandmark.top), self.shaftRadius, ballBearingWidth)

        ball = Part("ball").createSphere(self.ballRadius)

        Joint(ballBearingInner.getLandmark(PresetLandmark.left), ball.getLandmark(
            PresetLandmark.right)).limitLocationXYZ(self.ballBearingInnerGrooveDepth, 0, 0)

        ball.circularPattern(9, 360/9, ballBearingInner)

        return ballBearingInner


if __name__ == "__main__":
    BallBearing().create()
