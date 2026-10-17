from parameters import parameters
from elements.spacers import sliderSpacer
from elements.tenons import tenon
from pieces.piece import Piece
from drawing import Line

def _trace_slider(plateSlidesToMaxLength: bool, slideOnLength: bool, parameters=parameters) -> Line:
    slider_spacer = sliderSpacer(slideOnLength)
    spacingCount = slider_spacer.spacingCount
    spacingLength = slider_spacer.spacingLength
    sliderLength = slider_spacer.totalLength
    sliderWidth = parameters.sliderWidth
    if plateSlidesToMaxLength:
        stopperLength = parameters.sliderStopperMinimalLength
    else:
        stopperLength = (
            sliderLength
            - parameters.coverWoodThickness
            - 3 * parameters.structuralWoodThickness
            - parameters.clearanceMargin
            - parameters.frictionMargin
        )
    backLength = 0 if plateSlidesToMaxLength else parameters.structuralWoodThickness
    frontLength = sliderLength - backLength - stopperLength
    stopperWidth = parameters.sliderStopperWidth
    tenonLine = tenon(False, True)
    spacingLine = Line.movesFromOrigin((-spacingLength, 0))
    slider = Line.movesFromOrigin(
        (backLength, 0),
        (0, -stopperWidth),
        (stopperLength, 0),
        (0, stopperWidth),
        (frontLength, 0),
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

def _build_slider(plateSlidesToMaxLength: bool, slideOnLength: bool, parameters=parameters) -> Piece:
    return Piece(
        traceCuts=None,
        innerCuts=None,
        outerCuts=_trace_slider(
            plateSlidesToMaxLength=plateSlidesToMaxLength,
            slideOnLength=slideOnLength,
            parameters=parameters
            )
        )

def buildTopSlider(parameters=parameters) -> Piece:
    return _build_slider(
        plateSlidesToMaxLength=True,
        slideOnLength=True,
        parameters=parameters
    )

def buildBotSlider(parameters=parameters) -> Piece:
    return _build_slider(
        plateSlidesToMaxLength=False,
        slideOnLength=True,
        parameters=parameters
    )

def buildSideSlider(parameters=parameters) -> Piece:
    return _build_slider(
        plateSlidesToMaxLength=False,
        slideOnLength=False,
        parameters=parameters
    )