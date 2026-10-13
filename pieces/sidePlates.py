from dataclasses import dataclass
from parameters import parameters
from .piece import Piece
from elements.tenons import tenonHole
from elements.spacers import sliderSpacer, innerBoxSideSpacer, innerBoxBottomSpacer, HoleSpacerFromTenonSpacer
from elements.fakeCuts import FakeCutDimensions
from drawing import Rectangle, Line, Point, Group

@dataclass (frozen=True)
class SidePlateBuilder:

    @property
    def _slider_length_spacer(self) -> HoleSpacerFromTenonSpacer:
        return HoleSpacerFromTenonSpacer(
            sliderSpacer(True, parameters)
        )

    @property
    def _slider_height_spacer(self) -> HoleSpacerFromTenonSpacer:
        return HoleSpacerFromTenonSpacer(
            sliderSpacer(False, parameters)
        )

    @property
    def _inner_box_side_spacer(self) -> HoleSpacerFromTenonSpacer:
        return HoleSpacerFromTenonSpacer(
            innerBoxSideSpacer(parameters)
        )

    @property
    def _inner_box_bottom_spacer(self) -> HoleSpacerFromTenonSpacer:
        return HoleSpacerFromTenonSpacer(
            innerBoxBottomSpacer(parameters)
        )

    @property
    def _slider_length_origin(self) -> Point:
        return Point(
            (
                parameters.coverWoodThickness
                + 3 * parameters.structuralWoodThickness
                + parameters.clearanceMargin
                + parameters.frictionMargin
                + parameters.cutWidth
            ),(
                parameters.coverWoodThickness
                + parameters.structuralWoodThickness
            )
        )

    @property
    def _slider_height_origin(self) -> Point:
        return Point(
            (
                parameters.coverWoodThickness
                + parameters.structuralWoodThickness
            ),
            (
                parameters.coverWoodThickness
                + parameters.structuralWoodThickness
                + parameters.clearanceMargin
                + parameters.cutWidth
            )
        )

    @property
    def _inner_box_side_origin(self) -> Point:
        return Point(
            (
                parameters.coverWoodThickness
                + 3 * parameters.structuralWoodThickness
                + parameters.clearanceMargin
                + parameters.frictionMargin
            ),
            (
                parameters.coverWoodThickness
                + 3 * parameters.structuralWoodThickness
                + parameters.clearanceMargin
                + parameters.frictionMargin
                + parameters.cutWidth
            )
        )
    
    @property
    def _inner_box_bottom_origin(self) -> Point:
        return Point(
            (
                parameters.coverWoodThickness
                + 4 * parameters.structuralWoodThickness
                + parameters.clearanceMargin
                + parameters.frictionMargin
            ),
            (
                parameters.fullHeight
                - (
                    parameters.coverWoodThickness
                    + 4 * parameters.structuralWoodThickness
                    + parameters.clearanceMargin
                    + parameters.frictionMargin
                    + parameters.cutWidth
                )
            )
        )

    @property
    def _outer_cut(self) -> Rectangle:
        return Rectangle(parameters.fullLength, parameters.fullHeight)

    def _slider_length_holes(self, isTopSlider: bool, parameters=parameters) -> tuple[Rectangle, ...]:
        spacer = self._slider_length_spacer
        translation = Point(spacer.spacingLength + spacer.elementLength, 0) 
        count = spacer.elementCount
        hole = tenonHole(True, parameters)
        holes = []
        for n in range(count):
            newHole = hole + translation * n + self._slider_length_origin
            if not isTopSlider:
                newHole = newHole.rotate180(
                    self._outer_cut.boundingBox.center
                )
            holes.append(newHole)
        return tuple(holes)

    def _slider_height_holes(self, isLeftSlider: bool, parameters=parameters) -> tuple[Rectangle, ...]:
        spacer = self._slider_height_spacer
        translation = Point(0, spacer.spacingLength + spacer.elementLength) 
        count = spacer.elementCount
        hole = tenonHole(False, parameters)
        holes = []
        for n in range(count):
            newHole = hole + translation * n + self._slider_height_origin
            if not isLeftSlider:
                newHole = newHole.rotate180(
                    self._outer_cut.boundingBox.center
                )
            holes.append(newHole)
        return tuple(holes)

    def _inner_box_side_holes(self, isLeftSide: bool, parameters=parameters) -> tuple[Rectangle, ...]:
        spacer = self._inner_box_side_spacer
        translation = Point(0, spacer.spacingLength + spacer.elementLength) 
        count = spacer.elementCount
        hole = tenonHole(False, parameters)
        holes = []
        for n in range(count):
            newHole = hole + translation * n + self._inner_box_side_origin
            if not isLeftSide:
                newHole = newHole.flipHorizontal(
                    self._outer_cut.boundingBox.center.x
                )
            holes.append(newHole)
        return tuple(holes)

    def _inner_box_bottom_holes(self, parameters=parameters) -> tuple[Rectangle, ...]:
        spacer = self._inner_box_bottom_spacer
        translation = Point(spacer.spacingLength + spacer.elementLength, 0)
        origin = self._inner_box_bottom_origin + Point(spacer.spacingLengthOnSides, 0)
        count = spacer.elementCount
        hole = tenonHole(True, parameters)
        holes = []
        for n in range(count):
            newHole = hole + translation * n + origin
            holes.append(newHole)
        return tuple(holes)
    
    def _inner_cuts(self, parameters=parameters) -> Group:
        return Group(
            self._slider_length_holes(True, parameters)
            + self._slider_length_holes(False, parameters)
            + self._slider_height_holes(True, parameters)
            + self._slider_height_holes(False, parameters)
            + self._inner_box_side_holes(True, parameters)
            + self._inner_box_side_holes(False, parameters)
            + self._inner_box_bottom_holes(parameters)
        )

    def _outer_cuts(self, parameters=parameters) -> Rectangle:
        return self._outer_cut
        
    def build(self, parameters=parameters):
        return Piece(
            traceCuts=None,
            innerCuts=self._inner_cuts(parameters),
            outerCuts=self._outer_cuts(parameters)
        )

@dataclass (frozen=True)
class SidePlateCoverBuilder:

    @property
    def _width(self) -> float:
        return parameters.fullLength - 2 * parameters.coverPadding

    @property
    def _height(self) -> float:
        return parameters.fullHeight - 2 * parameters.coverPadding

    def _outer_cuts(self) -> Rectangle:
        return Rectangle(self._width, self._height)

    @property
    def fakeCutsDimentions(self) -> FakeCutDimensions:
        return FakeCutDimensions()
    
    def _4corners(self, n: int, count: int) -> tuple:
        initialDistance = self.fakeCutsDimentions.initialEdgeDistance
        traceWidth = parameters.traceCutWidth
        left = initialDistance + n * traceWidth
        right = self._width - initialDistance - n * traceWidth
        up = initialDistance + n * traceWidth
        down = self._height - initialDistance - n * traceWidth

        return (
            (right, up),
            (right, down),
            (left, down),
            (left, up + (0 if n == count - 1 else traceWidth))
        )

    def _fake_cuts(self) -> Line:
        count = self.fakeCutsDimentions.passesCount
        corners = ((0, self.fakeCutsDimentions.initialEdgeDistance),)
        for n in range(count):
            corners += self._4corners(n, count)
        
        return Line.fromCoords(*corners)

    def build(self) -> Piece:
        return Piece(
            traceCuts=self._fake_cuts(),
            innerCuts=None,
            outerCuts=self._outer_cuts()
        )    
