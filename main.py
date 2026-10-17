from parameters import parameters
from drawing import group, generate_svg, GeometryError
from pieces import (
    SidePlateBuilder,
    SidePlateCoverBuilder,
    InnerBoxBuilder,
    SlidingPlateBuilder,
    PlateType,
    buildBigSlidingPlatesAssembler,
    buildSmallSlidingPlatesAssembler,
    buildTopSlider,
    buildBotSlider,
    buildSideSlider
)

outerPlate1 = SlidingPlateBuilder(1, PlateType.OUTER).build()
outerPlate2 = SlidingPlateBuilder(2, PlateType.OUTER).build().moveRightTo(outerPlate1)
outerPlate3 = SlidingPlateBuilder(3, PlateType.OUTER).build().moveRightTo(outerPlate1).moveBelow(outerPlate2)
outerPlate4 = SlidingPlateBuilder(4, PlateType.OUTER).build().moveBelow(outerPlate1)

innerPlate2 = SlidingPlateBuilder(2, PlateType.INNER).build().moveBelow(outerPlate4)
innerPlate3 = SlidingPlateBuilder(3, PlateType.INNER).build().placeUpLeftAtShape(innerPlate2).moveBelow(innerPlate2)
innerPlate1 = SlidingPlateBuilder(1, PlateType.INNER).build().placeUpLeftAtShape(innerPlate2).moveRightTo(innerPlate2)
innerPlate4 = SlidingPlateBuilder(4, PlateType.INNER).build().placeUpLeftAtShape(innerPlate1).moveBelow(innerPlate1)

midPlate1 = SlidingPlateBuilder(1, PlateType.MID).build().moveRightTo(outerPlate2)
midPlate2 = SlidingPlateBuilder(2, PlateType.MID).build().placeUpLeftAtShape(midPlate1).moveBelow(midPlate1)
midPlate3 = SlidingPlateBuilder(3, PlateType.MID).build().placeUpLeftAtShape(midPlate1).moveBelow(midPlate2)
midPlate4 = SlidingPlateBuilder(4, PlateType.MID).build().placeUpLeftAtShape(midPlate1).moveBelow(midPlate3)

innerSlidingPlates = [
    SlidingPlateBuilder(n, PlateType.INNER).build() for n in range(1, 5)
]

sidePlate = SidePlateBuilder().build().rotate90xtoy().placeUpLeftAtShape(midPlate1).moveRightTo(midPlate1)
sidePlate1 = sidePlate
sidePlate2 = sidePlate.flipVertical().moveBelow(sidePlate1)

innerBox = InnerBoxBuilder().build().placeUpLeftAtOrigin().moveRightTo(sidePlate1)

assembler = buildBigSlidingPlatesAssembler().moveRightTo(innerBox)
assembler1 = assembler
assembler2 = assembler.moveBelow(assembler1)
assembler3 = assembler.moveBelow(assembler2)
assembler4 = assembler.moveBelow(assembler3)
assembler5 = assembler.moveBelow(assembler4)
assembler6 = assembler.moveBelow(assembler5)
assembler7 = assembler.moveBelow(assembler6)
assembler8 = buildSmallSlidingPlatesAssembler().moveRightTo(innerBox).moveBelow(assembler7)

sliderTop1 = buildTopSlider().rotate90xtoy().placeUpLeftAtShape(innerBox).moveBelow(innerBox)
sliderTop2 = sliderTop1.moveRightTo(sliderTop1).flipHorizontal()
sliderBot1 = buildBotSlider().rotate90xtoy().placeUpLeftAtShape(sliderTop2).moveRightTo(sliderTop2)
sliderBot2 = sliderBot1.moveRightTo(sliderBot1).flipHorizontal()

sliderSide = buildSideSlider().placeUpLeftAtShape(sidePlate2).moveBelow(sidePlate2)
sliderSide1 = sliderSide.flipVertical()
sliderSide2 = sliderSide.moveBelow(sliderSide1)
sliderSide3 = sliderSide.moveBelow(sliderSide2).flipVertical()
sliderSide4 = sliderSide.moveBelow(sliderSide3)

slideCover1 = SlidingPlateBuilder(1, PlateType.COVER).build().placeUpLeftAtShape(innerPlate3).moveBelow(innerPlate3)
slideCover3 = SlidingPlateBuilder(3, PlateType.COVER).build().placeUpLeftAtShape(slideCover1).moveRightTo(slideCover1)
slideCover2 = SlidingPlateBuilder(2, PlateType.COVER).build().placeUpLeftAtShape(slideCover3).moveBelow(slideCover3)
slideCover4 = SlidingPlateBuilder(4, PlateType.COVER).build().placeUpLeftAtShape(slideCover1).moveBelow(slideCover1)

sidePlateCover = SidePlateCoverBuilder().build().placeUpLeftAtShape(slideCover3).moveRightTo(slideCover3)
sidePlateCover1 = sidePlateCover
sidePlateCover2 = sidePlateCover.moveBelow(sidePlateCover1)

try:
    svg = generate_svg(
        (
            outerPlate1.getSVG(),
            outerPlate2.getSVG(),
            outerPlate3.getSVG(),
            outerPlate4.getSVG(),
            innerPlate1.getSVG(),
            innerPlate2.getSVG(),
            innerPlate3.getSVG(),
            innerPlate4.getSVG(),
            midPlate1.getSVG(),
            midPlate2.getSVG(),
            midPlate3.getSVG(),
            midPlate4.getSVG(),
            sidePlate1.getSVG(),
            sidePlate2.getSVG(),
            innerBox.getSVG(),
            assembler1.getSVG(),
            assembler2.getSVG(),
            assembler3.getSVG(),
            assembler4.getSVG(),
            assembler5.getSVG(),
            assembler6.getSVG(),
            assembler7.getSVG(),
            assembler8.getSVG(),
            sliderTop1.getSVG(),
            sliderTop2.getSVG(),
            sliderBot1.getSVG(),
            sliderBot2.getSVG(),
            sliderSide1.getSVG(),
            sliderSide2.getSVG(),
            sliderSide3.getSVG(),
            sliderSide4.getSVG(),
            slideCover1.getSVG(),
            slideCover2.getSVG(),
            slideCover3.getSVG(),
            slideCover4.getSVG(),
            sidePlateCover1.getSVG(),
            sidePlateCover2.getSVG()
        )
    )
except GeometryError as error:
    print(error)


with open("boite.svg", "w") as f:
    f.write(svg)
