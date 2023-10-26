from math import floor
from codetocad import *


class BallBearing:

    def __init__(self, width: Dimension, outer_radius: Dimension, shaft_Radius: Dimension, ball_radius: Dimension, number_of_balls=None) -> None:
        self.width = width
        self.outerRadius = outer_radius
        self.shaftRadius = shaft_Radius
        self.ball_radius = ball_radius

        self.groove_depth = ball_radius * 0.3

        self.inner_radius = (outer_radius - shaft_Radius -
                             ball_radius - self.groove_depth) / 2 + shaft_Radius

        print("ballRadius", ball_radius, "outerRadius", outer_radius)

        self.number_of_balls = number_of_balls or BallBearing.get_number_of_balls_from_outer_radius_and_ball_radius_ratio(
            outer_radius, ball_radius)

    # late initialization
    ball_bearing_outer: Part
    ball_bearing_inner: Part
    ball: Part

    def create(self):
        groove_inner_radius = self.inner_radius - self.groove_depth

        ball_bearing_outer_hole_radius = self.inner_radius + \
            self.ball_radius * 2 - self.groove_depth * 2

        # MARK: create inner and outer bearing bodies:

        self.ball_bearing_outer = Part("ballBearingOuter").create_cylinder(
            self.outerRadius,
            self.width
        )

        self.ball_bearing_outer.hole(self.ball_bearing_outer.get_landmark(
            PresetLandmark.top), ball_bearing_outer_hole_radius,
            self.width)

        self.ball_bearing_inner = Part("ballBearingInner").create_cylinder(
            self.inner_radius,

            self.width
        )

        self.ball_bearing_inner.hole(self.ball_bearing_inner.get_landmark(
            PresetLandmark.top), self.shaftRadius,
            self.width)

        # MARK: Create groove

        ballBearingInnerGroove = Part("ballBearingInnerGroove").create_torus(groove_inner_radius,
                                                                             groove_inner_radius + self.ball_radius * 2)

        self.ball_bearing_inner.subtract(
            ballBearingInnerGroove, delete_after_subtract=False)
        self.ball_bearing_outer.subtract(
            ballBearingInnerGroove)

        # MARK: create balls

        self.ball = Part("ball").create_sphere(self.ball_radius)

        Joint(self.ball_bearing_inner, self.ball).limit_rotation_xyz(0, 0, 0)
        Joint(self.ball_bearing_inner, self.ball_bearing_outer).limit_rotation_xyz(
            0, 0, None)

        Joint(self.ball_bearing_inner.get_landmark(PresetLandmark.left), self.ball.get_landmark(
            PresetLandmark.right)).limit_location_xyz(self.groove_depth, 0, 0)

        self.ball.circular_pattern(
            self.number_of_balls, 360 / self.number_of_balls, self.ball_bearing_inner)

        return self

    def set_material(self):
        # SA: this won't work anymore if combinePartsIntoOne is called.

        ball_bearing_material = Material("ballBearing").set_reflectivity(1.0)

        self.ball_bearing_outer.set_material(ball_bearing_material)
        self.ball_bearing_inner.set_material(ball_bearing_material)
        self.ball.set_material(ball_bearing_material)

        return self

    @staticmethod
    def get_number_of_balls_from_outer_radius_and_ball_radius_ratio(outer_radius: Dimension, ball_radius: Dimension) -> int:
        number_of_balls = floor(
            ((outer_radius+ball_radius)/ball_radius * 2).value)
        return number_of_balls - 1

    def combine_parts_into_one(self) -> Part:
        return self.ball_bearing_inner.union(self.ball_bearing_outer).union(self.ball).rename("ballBearing")


if __name__ == "__main__":
    Scene.default().set_default_unit("mm")

    width = Dimension.from_string("16mm")

    shaft_radius = Dimension.from_string("30/2mm")

    ball_radius = Dimension.from_string("9.53/2mm")

    outer_radius = Dimension.from_string("62/2mm")

    BallBearing(
        width=width,
        outer_radius=outer_radius,
        shaft_Radius=shaft_radius,
        ball_radius=ball_radius,
        number_of_balls=9
    ).create().set_material()
