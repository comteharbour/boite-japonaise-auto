from dataclasses import dataclass
from parameters import parameters
from .piece import Piece
from elements.tenons import tenonHole
from elements.spacers import sliderSpacer, innerBoxSideSpacer, innerBoxBottomSpacer, HoleSpacerFromTenonSpacer
from drawing import Rectangle, Point, Group

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