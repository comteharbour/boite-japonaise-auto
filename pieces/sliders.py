from parameters import parameters
from elements.spacers import sliderSpacer
from elements.tenons import tenon
from pieces.piece import Piece
from drawing import Line

def _trace_slider(plateSlidesOpen: bool, slideOnLength: bool, parameters=parameters) -> Line:
    slider_spacer = sliderSpacer(slideOnLength)
    spacingCount = slider_spacer.spacingCount
    spacingLength = slider_spacer.spacingLength
    sliderLength = slider_spacer.totalLength
    sliderWidth = parameters.sliderWidth
    if plateSlidesOpen:
        stopperSideLength = 0
        openSideLength = (
            parameters.structuralWoodThickness
            + parameters.slidingPlatesStopperLength
        )
    else:
        stopperSideLength = parameters.structuralWoodThickness
        openSideLength = (
            parameters.coverWoodThickness
            + parameters.structuralWoodThickness
            + parameters.frictionMargin
            + parameters.slidingPlatesStopperLength
        )
    stopperLength = (
        sliderLength
        - openSideLength
        - stopperSideLength
    )
    stopperWidth = parameters.sliderStopperWidth
    tenonLine = tenon(False, True)
    spacingLine = Line.movesFromOrigin((-spacingLength, 0))
    slider = Line.movesFromOrigin(
        (stopperSideLength, 0),
        (0, -stopperWidth),
        (stopperLength, 0),
        (0, stopperWidth),
        (openSideLength, 0),
        (0, sliderWidth)
    )
    slider = slider.concat(tenonLine)
    for _ in range(spacingCount):
        slider = slider.concat(
            spacingLine
        ).concat(
            tenonLine
        )
    slider = slider.setClose(True)
    return slider

def _build_slider(plateSlidesOpen: bool, slideOnLength: bool, parameters=parameters) -> Piece:
    return Piece(
        traceCuts=None,
        innerCuts=None,
        outerCuts=_trace_slider(
            plateSlidesOpen=plateSlidesOpen,
            slideOnLength=slideOnLength,
            parameters=parameters
            )
        )

def buildTopSlider(parameters=parameters) -> Piece:
    return _build_slider(
        plateSlidesOpen=True,
        slideOnLength=True,
        parameters=parameters
    )

def buildBotSlider(parameters=parameters) -> Piece:
    return _build_slider(
        plateSlidesOpen=False,
        slideOnLength=True,
        parameters=parameters
    )

def buildSideSlider(parameters=parameters) -> Piece:
    return _build_slider(
        plateSlidesOpen=False,
        slideOnLength=False,
        parameters=parameters
    )