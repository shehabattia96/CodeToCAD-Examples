from codetocad import Part, Material, Dimension, PresetLandmark, LandmarkOrItsName, Joint, Scene


class BakingPan:
    width = "300mm"
    length = "350mm"
    height = "33.5mm"

    thickness = Dimension.from_string("3.5mm")
    wall_draft_angle = 180-100

    shelf_width = Dimension.from_string("20mm")

    # fillets
    outer_corner_radius = "70mm"
    bottom_edges_radius = "10mm"
    top_edges_inner_radius = "5mm"
    top_edges_outer_radius = "1mm"

    # holes
    number_of_holes_x = 6
    number_of_holes_y = 9
    hole_radius = Dimension.from_string("17/2mm")

    # late initialization
    pan: Part

    def create_pan_body(self):

        self.pan = Part("pan").create_cube(
            self.width,
            self.length,
            self.height)

        self.pan.hollow(
            self.shelf_width*2,
            self.shelf_width*2,
            self.thickness/2)

    def fillet_corners(self, part: Part) -> Part:

        pan_corner_edges = [PresetLandmark.leftBack, PresetLandmark.leftFront,
                            PresetLandmark.rightBack, PresetLandmark.rightFront]
        pan_corner_outer_and_inner_edge_pairs: list[list[LandmarkOrItsName]] = [
        ]

        for edge in pan_corner_edges:
            edge_landmark = part.get_landmark(edge)

            edge_landmark_location = edge_landmark.get_location_local()

            # right/left are x-axis, front/back are y-axis, relative positions respectively
            offset_x = self.shelf_width * (-1 if "right" in edge.name else 1)
            offset_y = self.shelf_width * (1 if "Front" in edge.name else -1)

            edge_landmark_inner = part.create_landmark(
                edge.name + "Inner", edge_landmark_location.x + offset_x, edge_landmark_location.y + offset_y, edge_landmark_location.z)

            pan_corner_outer_and_inner_edge_pairs.append(
                [edge_landmark, edge_landmark_inner])

        for pair in pan_corner_outer_and_inner_edge_pairs:
            part.fillet_edges(
                self.outer_corner_radius,
                pair, use_width=True
            )

        return part

    def fillet_bottom_inner_edges(self):

        self.pan.fillet_faces(self.bottom_edges_radius, [
            self.pan.get_landmark("bottomInner")])

    def create_bottom_inner_landmarks(self):

        pan_bottom_location = self.pan.get_landmark(
            PresetLandmark.bottom).get_location_local()

        self.pan.create_landmark(
            "bottomInner", pan_bottom_location.x + self.hole_radius * 2, pan_bottom_location.y, pan_bottom_location.z + self.thickness)

        self.pan.create_landmark(
            "hole", pan_bottom_location.x + self.hole_radius * 2, pan_bottom_location.y, pan_bottom_location.z)

    def create_bottom_holes(self):
        pan_hole_location = self.pan.get_landmark("hole")
        self.pan.hole(pan_hole_location, self.hole_radius, self.thickness,
                      linear_pattern_instance_count=self.number_of_holes_x//2, linear_pattern_instance_separation=self.hole_radius*4, linear_pattern2nd_instance_count=self.number_of_holes_y//2, linear_pattern2nd_instance_separation=self.hole_radius*4, linear_pattern2nd_instance_axis="y", flip_axis=True, mirror=True, mirror_about_entity_or_landmark=self.pan.get_landmark(PresetLandmark.center), mirror_axis="x")
        self.pan.hole(pan_hole_location, self.hole_radius, self.thickness,
                      linear_pattern_instance_count=self.number_of_holes_x//2, linear_pattern_instance_separation=self.hole_radius*4, linear_pattern2nd_instance_count=self.number_of_holes_y//2, linear_pattern2nd_instance_separation=self.hole_radius*-4, linear_pattern2nd_instance_axis="y", flip_axis=True, mirror=True, mirror_about_entity_or_landmark=self.pan.get_landmark(PresetLandmark.center), mirror_axis="x")

    def create_shelf(self):
        shelf = Part("shelf").create_cube(
            self.width,
            self.length,
            Dimension.from_string(self.height) - self.thickness)

        shelf.hollow(
            self.shelf_width*2 - self.thickness,
            self.shelf_width*2 - self.thickness,
            0)

        shelf = self.fillet_corners(part=shelf)

        Joint(self.pan.get_landmark(PresetLandmark.bottom), shelf.get_landmark(
            PresetLandmark.bottom)).limit_location_xyz(0, 0, 0)

        self.pan.subtract(shelf)

    def create(self):

        self.create_pan_body()

        self.pan = self.fillet_corners(self.pan)

        self.create_bottom_inner_landmarks()

        self.fillet_bottom_inner_edges()

        self.create_bottom_holes()

        self.create_shelf()

        material = Material("granite").set_image_texture(
            "./Granite07small_3K_BaseColor.png")

        self.pan.set_material(material)


if __name__ == "__main__":
    Scene.default().set_default_unit("mm")

    BakingPan().create()
