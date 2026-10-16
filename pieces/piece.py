from dataclasses import dataclass
from typing import Self
from parameters import parameters
from drawing import SVGObject, LaserType, Point, BoundingBox, Group, group

@dataclass (frozen=True)
class Piece:
    traceCuts: SVGObject | None
    innerCuts: SVGObject | None
    outerCuts: SVGObject | None

    @property
    def allSVGObjects(self) -> Group:
        objects = []
        if not self.traceCuts is None: objects.append(self.traceCuts)
        if not self.innerCuts is None: objects.append(self.innerCuts)
        if not self.outerCuts is None: objects.append(self.outerCuts)
        return Group(tuple(objects))

    @property
    def boundingBox(self) -> BoundingBox:
        return self.allSVGObjects.boundingBox

    def _applyToCuts(self, operation) -> Self:

        traceCuts = (
            None
            if self.traceCuts is None
            else operation(self.traceCuts)
        )

        innerCuts = (
            None
            if self.innerCuts is None
            else operation(self.innerCuts)
        )

        outerCuts = (
            None
            if self.outerCuts is None
            else operation(self.outerCuts)
        )

        return Piece(traceCuts, innerCuts, outerCuts)

    def __add__(self, vector) -> Self:
        return self._applyToCuts(
            lambda cuts: cuts + vector
        )

    def __sub__(self, vector) -> Self:
        return self._applyToCuts(
            lambda cuts: cuts - vector
        )

    def rotate90xtoy(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return self._applyToCuts(
            lambda cuts: cuts.rotate90xtoy(pivot)
        )

    def rotate180(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return self._applyToCuts(
            lambda cuts: cuts.rotate180(pivot)
        )

    def rotate90ytox(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return self._applyToCuts(
            lambda cuts: cuts.rotate90ytox(pivot)
        )

    def flipHorizontal(self, xVerticalMirror: float | None = None) -> Self:
        if xVerticalMirror is None: xVerticalMirror = self.boundingBox.center.x
        return self._applyToCuts(
            lambda cuts: cuts.flipHorizontal(xVerticalMirror)
        )

    def flipVertical(self, yHorizontalMirror: float | None = None) -> Self:
        if yHorizontalMirror is None: yHorizontalMirror = self.boundingBox.center.y
        return self._applyToCuts(
            lambda cuts: cuts.flipVertical(yHorizontalMirror)
        )

    def placeUpLeftAtOrigin(self) -> Self:
        return self - self.boundingBox.upLeft

    def placeUpLeftAtPoint(self, point: Point | None = None) -> Self:
        if point is None: point = Point(0, 0)
        return self.placeUpLeftAtOrigin() + point

    def placeUpLeftAtShape(self, shape: SVGObject) -> Self:
        return self.placeUpLeftAtOrigin() + shape.boundingBox.upLeft

    def moveBelow(self, otherPiece: Self) -> Self:
        newUpLeftCorner = Point(
            x=self.boundingBox.xMin,
            y=otherPiece.boundingBox.yMax + parameters.gapBetweenPiecesOnCuttingPlate
        )
        return self.placeUpLeftAtPoint(newUpLeftCorner)

    def moveRightTo(self, otherPiece: Self) -> Self:
        newUpLeftCorner = Point(
            x=otherPiece.boundingBox.xMax + parameters.gapBetweenPiecesOnCuttingPlate,
            y=self.boundingBox.yMin
        )
        return self.placeUpLeftAtPoint(newUpLeftCorner)

    def getSVG(self):
        traceCutsSVG = "" if self.traceCuts is None else self.traceCuts.getSVG(LaserType.TRACE)
        innerCutsSVG = "" if self.innerCuts is None else self.innerCuts.getSVG(LaserType.INNERCUT)
        outerCutsSVG = "" if self.outerCuts is None else self.outerCuts.getSVG(LaserType.OUTERCUT)
        return group((traceCutsSVG, innerCutsSVG, outerCutsSVG))

