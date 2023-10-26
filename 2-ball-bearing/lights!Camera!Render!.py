from codetocad import *

part: Part = Scene.default().get_selected_entity()

partLocation = part.get_location_world()
partDimensions = part.get_dimensions()

ground = Part("Ground").create_cube(
    partDimensions.x * 4, partDimensions.y * 4, "2mm")

Joint(part.get_landmark(PresetLandmark.bottom), ground.get_landmark(
    PresetLandmark.top)).limit_location_xyz(0, 0, 0)

camera = Camera("Camera").create_perspective().set_focal_length(300)

camera.translate_xyz(partLocation.x, partLocation.y + .3,
                     partLocation.z + 0.0).rotate_xyz(-90, 180, 0)

light = Light("light").create_area(10).translate_xyz(
    partLocation.x, partLocation.y + 1,  partLocation.z + 1).rotate_xyz(-25, 0, 0)


Render().set_camera(camera)
# Render().renderImage(f"./{part.name}.png")
