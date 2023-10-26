from codetocad import *


class PillowBlock:

    wall_thickness_Radius = Dimension.from_string("2mm")
    base_height = Dimension.from_string("2mm")

    set_screw_radius = Dimension.from_string("3/2mm")

    mount_screw_radius = Dimension.from_string("5/2mm")

    def __init__(self, hole_radius: Dimension, width: Dimension) -> None:
        self.hole_radius = hole_radius
        self.width = width

    def create(self):
        block_radius = self.hole_radius + self.wall_thickness_Radius

        block = Part("pillowBlock").create_cube(
            block_radius*2,
            self.width,
            block_radius*2,
        )

        block.fillet_faces("4mm", [block.get_landmark(
            PresetLandmark.top)], use_width=True)

        front_location = block.get_landmark(
            PresetLandmark.front).get_location_local()
        front_hole_location = block.create_landmark(
            "frontHole", front_location.x, front_location.y - "1mm", front_location.z)
        block.hole(front_hole_location,
                   self.hole_radius, self.width, normal_axis="y", flip_axis=True)

        block.hole(block.get_landmark(landmark_name=PresetLandmark.top),
                   self.set_screw_radius, self.wall_thickness_Radius * 2)

        mount_screw_padding = Dimension.from_string("2mm")
        mount_screw_radius_with_padding = self.mount_screw_radius + mount_screw_padding

        block_base = Part("pillowBlockBase").create_cube(
            block_radius * 2 + (mount_screw_radius_with_padding * 4), self.width + mount_screw_padding * 2, self.base_height)

        block_base.fillet_faces("2mm", [block_base.get_landmark(
            PresetLandmark.top)], use_width=True)

        block_base_left_location = block_base.get_landmark(
            PresetLandmark.leftTop).get_location_local()
        block_base_hole_location = block_base.create_landmark(
            "mountHole", block_base_left_location.x + mount_screw_radius_with_padding, block_base_left_location.y, block_base_left_location.z)
        block_base.hole(block_base_hole_location, self.mount_screw_radius,
                        self.base_height, mirror=True, mirror_about_entity_or_landmark=block_base)

        Joint(block.get_landmark(PresetLandmark.bottom), block_base.get_landmark(
            PresetLandmark.top)).limit_location_xyz(0, 0, 0)

        return block.union(block_base)


if __name__ == "__main__":
    Scene.default().set_default_unit("mm")

    hole_radius = Dimension.from_string("5mm")
    width = Dimension.from_string("3mm")
    pillow_block = PillowBlock(hole_radius, width).create()

    from ball_bearing import BallBearing

    ball_bearing = BallBearing(width - "1mm", hole_radius, Dimension.from_string(
        "5/2mm"), hole_radius * 0.1).create().combine_parts_into_one().rotate_x(90)

    blueish_material = Material("blueish").setColor(
        0.0395728, 0.376706, 0.709804, 0.8)
    pillow_block.set_material(blueish_material)

    ball_bearing_material = Material("ball_bearing").set_reflectivity(1.0)
    ball_bearing.set_material(ball_bearing_material)
