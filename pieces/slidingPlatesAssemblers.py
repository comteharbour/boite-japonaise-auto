from enum import Enum
from parameters import parameters
from drawing import Line
from .piece import Piece
from elements.tenons import tenon

def _build_sliding_plates_assembler(isBig: bool, parameters=parameters) -> Piece:
    w = parameters.fullWidth - 4 * (parameters.structuralWoodThickness + parameters.frictionMargin) - 2 * (parameters.coverWoodThickness + parameters.holeEdgeMargin + parameters.tenonWidth) + parameters.cutWidth
    if not(isBig): w -= parameters.asymetricAssemblerReduction
    h = parameters.structuralWoodThickness + parameters.frictionMargin + parameters.cutWidth
    line = tenon(xStartLeft=True, yStartUp=False).concat(
        Line.movesFromOrigin((w,0))
    ).concat(
        tenon(xStartLeft=True, yStartUp=False)
    ).concat(
        Line.movesFromOrigin((0,h))
    ).concat(
        tenon(xStartLeft=False, yStartUp=True)
    ).concat(
        Line.movesFromOrigin((-w,0))
    ).concat(
        tenon(xStartLeft=False, yStartUp=True)
    ).setClose(True)

    return Piece(
        traceCuts=None,
        innerCuts=None,
        outerCuts=line
    ).placeUpLeftAtOrigin()

def buildSmallSlidingPlatesAssembler(parameters=parameters) -> Piece:
    return _build_sliding_plates_assembler(isBig=False, parameters=parameters)

def buildBigSlidingPlatesAssembler(parameters=parameters) -> Piece:
    return _build_sliding_plates_assembler(isBig=True, parameters=parameters)