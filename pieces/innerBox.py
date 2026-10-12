from dataclasses import dataclass
from parameters import parameters
from .piece import Piece
from elements.spacers import innerBoxBottomSpacer, innerBoxSideSpacer, innerBoxJunctionSpacer
from elements.tenons import tenon
from drawing import Line, Point, Group

def separationAtOriginGoingDown(parameters=parameters) -> Line:
    innerSpacer = innerBoxJunctionSpacer(parameters)
    width = innerSpacer.elementLength
    height = parameters.structuralWoodThickness
    count = innerSpacer.elementCount
    moves = []
    for n in range(count - 1):
        orientedHeight = height if n%2 == 0 else -height
        moves.extend([(width,0), (0, orientedHeight)])
    moves.append((width, 0))

    return Line.movesFromOrigin(*moves)

@dataclass (frozen=True)
class InnerBoxBuilder:

    @property
    def _down_spacer(self, parameters=parameters):
        return innerBoxBottomSpacer(parameters)

    @property
    def _side_spacer(self, parameters=parameters):
        return innerBoxSideSpacer(parameters)

    def _innerCuts(self, parameters=parameters) -> Group:
        separationAtOrigin = separationAtOriginGoingDown(parameters)
        topTranslationY = self._side_spacer.totalLength
        bottomTranslationY = self._side_spacer.totalLength + self._down_spacer.totalLength
        topSeparation = separationAtOrigin.flipVertical(0) + Point(0, topTranslationY)
        bottomSeparation = separationAtOrigin + Point(0, bottomTranslationY)

        return Group((topSeparation, bottomSeparation))

    def _side_tenon_path_left_down_from_origin(self, parameters=parameters) -> Line:
        tenonLine = tenon(True, True, parameters).rotate90xtoy(Point(0, 0))
        spacingLine = Line.movesFromOrigin((0, self._side_spacer.spacingLength))
        sideLine = tenonLine
        for _ in range(self._side_spacer.spacingCount):
            sideLine = sideLine.concat(
                spacingLine
            ).concat(
                tenonLine
            )
        return sideLine

    def _bottom_tenon_path_left_down_from_origin(self, parameters=parameters) -> Line:
            tenonLine = tenon(True, True, parameters).rotate90xtoy(Point(0, 0))
            spacingLine = Line.movesFromOrigin((0, self._down_spacer.spacingLength))
            sideLine = spacingLine
            for _ in range(self._down_spacer.elementCount):
                sideLine = sideLine.concat(
                    tenonLine
                ).concat(
                    spacingLine
                )
            return sideLine

    def _outerCuts(self, parameters=parameters) -> Line:
        sideTenonPath = self._side_tenon_path_left_down_from_origin(parameters)
        bottomTenonPath = self._bottom_tenon_path_left_down_from_origin(parameters)
        innerBowWidth = parameters.fullWidth - 2 * (parameters.coverWoodThickness + parameters.structuralWoodThickness)
        outerCut = sideTenonPath.concat(
            bottomTenonPath
        ).concat(
            sideTenonPath
        ).concat(
            Line.movesFromOrigin((innerBowWidth, 0))
        ).concat(
            sideTenonPath.rotate180(Point(0, 0))
        ).concat(
            bottomTenonPath.rotate180(Point(0, 0))
        ).concat(
            sideTenonPath.rotate180(Point(0, 0))
        ).setClose(True)

        return outerCut

    def build(self, parameters=parameters) -> Piece:
        return Piece(
            traceCuts=None,
            innerCuts=self._innerCuts(parameters),
            outerCuts=self._outerCuts(parameters)
        ).placeUpLeftAtOrigin()
