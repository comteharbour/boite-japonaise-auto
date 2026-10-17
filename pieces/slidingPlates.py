from enum import Enum
from dataclasses import dataclass
from parameters import parameters
from elements.tenons import tenonHole
from elements.fakeCuts import FakeCutDimensions
from drawing import Point, Rectangle, Line, Circle, GeometryError, Group, SVGObject
from .piece import Piece

def _arrowTraceCentered(parameters=parameters) -> Group:
    l = parameters.arrowLength
    w = parameters.traceFiguresWidth

    back = Line.fromCoords((-w/2, -l/2), (w/2, -l/2))
    body = Line.fromCoords((0, -l/2), (0, l/2))
    head = Line.fromCoords((-w/2, l/2 - w), (0, l/2), (w/2, l/2 - w))

    return Group((back, body, head))

def _squareTraceCentered(parameters=parameters) -> Rectangle:
    w = parameters.traceFiguresWidth
    return Rectangle.fromCoords(w, w, -w/2, -w/2)

def _circleTraceCentered(parameters=parameters) -> Circle:
    w = parameters.traceFiguresWidth
    return Circle.fromCoords(w/2)

class PlateType(Enum):
    OUTER = "outer"
    MID = "mid"
    INNER = "inner"
    COVER = "cover"

@dataclass (frozen=True)
class SlidingPlateBuilder:
    plateNumber: int
    plateType: PlateType

    @property
    def _widthReductionForSliders(self) -> float:
        return parameters.sliderWidth + parameters.sliderStopperWidth + parameters.frictionMargin

    @property
    def _heightReductionForOuterPlateThickness(self) -> float:
        return parameters.coverWoodThickness + parameters.structuralWoodThickness + parameters.clearanceMargin

    @property
    def _heightReductionForMidPlateThickness(self) -> float:
        return parameters.structuralWoodThickness + parameters.frictionMargin

    @property
    def _heightReductionForInnerPlateThickness(self) -> float:
        return parameters.holeEdgeMargin + parameters.cutWidth / 2

    @property
    def _baseHeight(self) -> float:
        match self.plateNumber:
            case 1: return parameters.fullLength
            case 2: return parameters.fullHeight - (parameters.coverWoodThickness + parameters.structuralWoodThickness)
            case 3: return parameters.fullLength - (parameters.coverWoodThickness + parameters.structuralWoodThickness)
            case 4: return parameters.fullHeight - 2 * (parameters.coverWoodThickness + parameters.structuralWoodThickness)

    @property
    def _heightDifference(self) -> float:
        match self.plateType:
            case PlateType.OUTER: return 0
            case PlateType.MID: return self._heightReductionForOuterPlateThickness
            case PlateType.INNER: return self._heightReductionForOuterPlateThickness + self._heightReductionForMidPlateThickness
            case PlateType.COVER: return parameters.coverPadding

    @property
    def _heightDownCorrection(self) -> float:
        if self.plateNumber == 1:
            return parameters.coverWoodThickness + parameters.structuralWoodThickness
        return 0

    @property
    def _baseWidth(self) -> float:
        return parameters.fullWidth - 2 * (parameters.coverWoodThickness + parameters.structuralWoodThickness + parameters.frictionMargin)

    @property
    def _widthDifference(self) -> float:
        match self.plateType:
            case PlateType.OUTER: return 0
            case PlateType.MID: return self._widthReductionForSliders
            case PlateType.INNER: return 0
            case PlateType.COVER: return parameters.coverPadding

    @property
    def _plateWidth(self) -> float:
        return self._baseWidth - 2 * self._widthDifference
    
    @property
    def _plateHeight(self) -> float:
        return self._baseHeight - 2 * self._heightDifference

    def _largeWidthHole(self, parameters=parameters) -> Rectangle:
        width = (
            self._plateWidth
            - 2 * parameters.holeEdgeMargin
        )
        height = parameters.structuralWoodThickness
        shape = Rectangle.fromCoords(width, height)
        return shape

    def _smallWidthHole(self, parameters=parameters) -> Rectangle:
        width = (
            self._plateWidth
            - 2 * parameters.holeEdgeMargin
            - parameters.asymetricAssemblerReduction
        )
        height = parameters.structuralWoodThickness
        shape = Rectangle.fromCoords(width, height)
        return shape

    def __post_init__(self):
        holeBoundingBox = tenonHole(
            horizontal=True,
            parameters=parameters
        ).boundingBox
        widthBetweenHoles = (
            self._xHoleTranslation(False, True)
            - self._xHoleTranslation(False, False)
            - holeBoundingBox.width
        )
        lengthHeightBetweenHoles = (
            self._yHoleTranslation(True)
            - self._yHoleTranslation(False)
            - holeBoundingBox.height
        )
        minimalSpaceBetweenHoles = parameters.holeEdgeMargin

        notEnoughSpaceBetweenHoles = (
            (
                (
                    self.plateType == PlateType.INNER
                    or
                    self.plateType == PlateType.OUTER
                )
                and
                widthBetweenHoles < minimalSpaceBetweenHoles
            )
            or
            lengthHeightBetweenHoles < minimalSpaceBetweenHoles
        )

        if(notEnoughSpaceBetweenHoles):
            raise GeometryError(
                f"Impossible sliding plate structure "
                f"(width between holes = {widthBetweenHoles}, "
                f"length or height between holes = {lengthHeightBetweenHoles}, "
                f"minimal space between holes = {minimalSpaceBetweenHoles}) "
            )



    def _xHoleTranslation(self, bigSide: bool, rightHole: bool) -> Point:
        translation = self._widthReductionForSliders + parameters.holeEdgeMargin
        if self.plateType == PlateType.MID: translation += parameters.sliderStopperWidth
        if not(bigSide): translation += parameters.asymetricAssemblerReduction / 2
        if rightHole: translation = self._baseWidth - (translation + parameters.tenonWidth - 2 * parameters.cutWidth)
        return translation

    def _yHoleTranslation(self, bigSide: bool) -> Point:
        translation = self._heightReductionForOuterPlateThickness + self._heightReductionForMidPlateThickness + self._heightReductionForInnerPlateThickness
        if bigSide: translation = self._baseHeight - (translation + parameters.structuralWoodThickness + self._heightDownCorrection)
        if self.plateNumber == 3 and bigSide: translation -= parameters.lengthSlidingPlateAsymetricOffset
        return translation
    
    def _shortHoles(self) -> Group:
        upLeft = tenonHole(horizontal=True) + (Point(self._xHoleTranslation(False, False), self._yHoleTranslation(False)))
        upRight = tenonHole(horizontal=True) + (Point(self._xHoleTranslation(False, True), self._yHoleTranslation(False)))
        downLeft = tenonHole(horizontal=True) + (Point(self._xHoleTranslation(True, False), self._yHoleTranslation(True)))
        downRight = tenonHole(horizontal=True) + (Point(self._xHoleTranslation(True, True), self._yHoleTranslation(True)))
        return Group((upLeft, upRight, downLeft, downRight))

    def _longHoles(self) -> Group:
        upLeft = self._smallWidthHole() + (Point(self._xHoleTranslation(False, False), self._yHoleTranslation(False)))
        downLeft = self._largeWidthHole() + (Point(self._xHoleTranslation(True, False), self._yHoleTranslation(True)))
        return Group((upLeft, downLeft))

    def _traceValidation(self):
        if self.plateNumber == 1 and self.plateType == PlateType.INNER:
            lengthFromHighestFigureToLowestFigure = (
                4 * parameters.traceFiguresWidth
                + parameters.arrowLength
            )

            plateHeight = self._plateHeight - self._heightDownCorrection
            figureIsOutOfPlate = lengthFromHighestFigureToLowestFigure > plateHeight 
            if figureIsOutOfPlate:
                raise GeometryError(
                    f"Figure traced out of plate "
                    f"(length from highest figure to lowest figure = {lengthFromHighestFigureToLowestFigure}, "
                    f"plate height = {plateHeight})"
                )

    def _traceStructuralWood(self) -> SVGObject | None:
        bigPlateWidth = self._baseWidth
        bigPlateHeight = self._baseHeight
        if self.plateNumber == 1:
            bigPlateHeight -= self._heightDownCorrection

        if not(self.plateType == PlateType.INNER): return None

        originToCenter = Point(bigPlateWidth/2, bigPlateHeight/2)
        centerToSideFigure = Point(
            0,
            (
                parameters.arrowLength / 2
                + 1.5 * parameters.traceFiguresWidth
            )
        )
        
        match self.plateNumber:
            case 1:
                circle = _circleTraceCentered() + originToCenter - centerToSideFigure
                arrow = _arrowTraceCentered() + originToCenter
                square = _squareTraceCentered() + originToCenter + centerToSideFigure
                return Group((circle, arrow, square))
            case 2: return _circleTraceCentered() + originToCenter
            case 3: return None
            case 4: return _squareTraceCentered() + originToCenter

    def _traceCoverWood(self) -> Group | None:

        if self.plateNumber == 4: return None

        dimensions = FakeCutDimensions()
        width = self._plateWidth - 2 * parameters.coverPadding
        fakeCutStrokes = []
        for n in range(dimensions.passesCount):
            if n % 2 == 0:
                x1 = 0
                x2 = width
            else:
                x1 = width
                x2 = 0

            y = dimensions.initialEdgeDistance + parameters.traceCutWidth * n

            fakeCutStrokes.append(
                Line.fromCoords((x1, y), (x2, y))
                + Point(self._widthDifference, self._heightDifference)
            )
        fakeCut = Group(tuple(fakeCutStrokes))
        if self.plateNumber > 1 : return fakeCut

        lowerFakeCut = fakeCut.flipVertical(yHorizontalMirror=self._plateHeight / 2)
        return Group((fakeCut, lowerFakeCut))
        
    
    def _traceCuts(self) -> Group | None:
        self._traceValidation()
        if self.plateType == PlateType.COVER: return self._traceCoverWood() 
        else: return self._traceStructuralWood()

    def _innerCuts(self) -> Group | None:
        if self.plateType == PlateType.COVER: return None
        if self.plateType == PlateType.MID: return self._longHoles()
        return self._shortHoles()

    def _outerCuts(self) -> SVGObject:
        width = self._plateWidth
        height = self._plateHeight

        if (
            (
                self.plateType == PlateType.INNER
                or self.plateType == PlateType.MID
            )
            and self.plateNumber == 1
        ):
            height -= self._heightDownCorrection

        if self.plateType == PlateType.COVER:
            width -= 2 * parameters.coverPadding
            height -= 2 * parameters.coverPadding

        if self.plateType == PlateType.MID:
            outerCut = Line.movesFromOrigin(
                (width + 2 * parameters.sliderStopperWidth, 0),
                (0, parameters.slidingPlatesStopperLength),
                (-parameters.sliderStopperWidth, 0),
                (0, height - parameters.slidingPlatesStopperLength),
                (-width, 0),
                (0, -height + parameters.slidingPlatesStopperLength),
                (-parameters.sliderStopperWidth, 0)
            ).setClose(True)
            if self.plateNumber <= 2:
                outerCut -= Point(0, parameters.clearanceMargin)
            else:
                outerCut += Point(0, parameters.clearanceMargin)
        else:
            outerCut = Rectangle.fromCoords(width, height)
        return outerCut + Point(self._widthDifference, self._heightDifference)

    def build(self):
        return Piece(
            traceCuts=self._traceCuts(),
            innerCuts=self._innerCuts(),
            outerCuts=self._outerCuts()
        ).placeUpLeftAtOrigin()