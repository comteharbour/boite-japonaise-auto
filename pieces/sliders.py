from parameters import parameters
from elements.spacers import sliderSpacer
from elements.tenons import tenon
from pieces.piece import Piece
from drawing import Line

def _trace_slider(slideOnLength: bool, parameters=parameters) -> Line:
    slider_spacer = sliderSpacer(slideOnLength)
    spacingCount = slider_spacer.spacingCount
    spacingLength = slider_spacer.spacingLength
    sliderLength = slider_spacer.totalLength
    sliderWidth = parameters.sliderWidth
    stopperLength = parameters.sliderStopperLength
    stopperWidth = parameters.sliderStopperWidth
    tenonLine = tenon(False, True)
    spacingLine = Line.movesFromOrigin((-spacingLength, 0))
    slider = Line.movesFromOrigin((stopperLength, 0), (0, stopperWidth), (sliderLength - stopperLength, 0), (0, sliderWidth))
    slider = slider.concat(tenonLine)
    for _ in range(spacingCount):
        slider = slider.concat(
            spacingLine
        ).concat(
            tenonLine
        )
    slider = slider.setClose(True)
    return slider

def _build_slider(slideOnLength: bool, parameters=parameters) -> Piece:
    return Piece(
        traceCuts=None,
        innerCuts=None,
        outerCuts=_trace_slider(
            slideOnLength=slideOnLength,
            parameters=parameters
            )
        )

def buildLengthSlider(parameters=parameters) -> Piece:
    return _build_slider(
        slideOnLength=True,
        parameters=parameters
    )

def buildHeightSlider(parameters=parameters) -> Piece:
    return _build_slider(
        slideOnLength=False,
        parameters=parameters
    )