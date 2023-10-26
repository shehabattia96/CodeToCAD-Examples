from codetocad import *


def create_bold(headThickness, headWidth, boltRadius, boltLength, boltNumberOfTurns) -> Part:

    head = Sketch("head").create_polygon(
        number_of_sides=6,
        length=headWidth,
        width=headWidth
    ).extrude(headThickness)

    bolt = Part("bolt").create_cylinder(radius=boltRadius, height=boltLength)

    bolt_spiral = Sketch("boltSpiral").create_spiral(
        number_of_turns=boltNumberOfTurns,
        height=boltLength,
        radius=boltRadius
    ).sweep(Sketch("boltSpiralWidth").create_circle("0.4mm")).remesh("decimate", 6)

    Joint(bolt.get_landmark("top"), bolt_spiral.get_landmark(
        "top")).limit_location_xyz(0, 0, 0)

    bolt.subtract(bolt_spiral)

    Joint(head.get_landmark("bottom"), bolt.get_landmark(
        "top")).limit_location_xyz(0, 0, 0)

    return bolt.union(head)


if __name__ == "__main__":
    bolt = create_bold(
        headThickness="2mm",
        headWidth="5mm",
        boltRadius="5/2mm",
        boltLength="3cm",
        boltNumberOfTurns=20
    )

    bolt.export("bolt.stl")
