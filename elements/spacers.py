from dataclasses import dataclass, field
import math
from parameters import parameters
from drawing import GeometryError

@dataclass(frozen=True)
class SpacerStructureFromFixedElementAndVariableSpacing:

    totalLength: float
    elementLength: float
    targetSpacing: float
    minimalSpacing: float = 0
    fixedElementIsOnEdges: bool = True

    spacingCount: int = field(init=False)
    elementCount: int = field(init=False)
    spacingLength: float = field(init=False)

    def __post_init__(self):

        minimalExtremeElement = self.elementLength if self.fixedElementIsOnEdges else self.minimalSpacing
        neededLength = self.elementLength + self.minimalSpacing + minimalExtremeElement
        impossible = self.totalLength < neededLength
        if impossible :
            raise GeometryError(
                f"Impossible SpacerStructure "
                f"(totalLength={self.totalLength}, "
                f"neededLength={neededLength})"
            )

        extremeElement = self.elementLength if self.fixedElementIsOnEdges else self.targetSpacing
        countRaw = (self.totalLength - extremeElement) / (self.elementLength + self.targetSpacing)
        countHigh = math.ceil(countRaw)
        countLow = max(math.floor(countRaw), 1)
        extraElement = 1 if self.fixedElementIsOnEdges else 0
        extraSpacing = 0 if self.fixedElementIsOnEdges else 1
        spacingShort = (self.totalLength - (countHigh + extraElement) * self.elementLength) / (countHigh + extraSpacing)
        spacingLong = (self.totalLength - (countLow + extraElement) * self.elementLength) / (countLow + extraSpacing)

        useLongSpacings =  spacingShort < self.minimalSpacing or spacingLong - self.targetSpacing < self.targetSpacing - spacingShort
    
        if useLongSpacings :
            count = countLow
            spacing = spacingLong
        else :
            count = countHigh
            spacing = spacingShort

        object.__setattr__(self, "spacingCount", count + extraSpacing)
        object.__setattr__(self, "elementCount", count + extraElement)
        object.__setattr__(self, "spacingLength", spacing)


@dataclass(frozen=True)
class HoleSpacerFromTenonSpacer:

    tenonSpacerStructure: SpacerStructureFromFixedElementAndVariableSpacing

    spacingCount: int = field(init=False)
    elementCount: int = field(init=False)
    spacingLength: float = field(init=False)
    spacingLengthOnSides: float = field(init=False)
    elementLength: float = field(init=False)
    totalLength: float = field(init=False)

    def __post_init__(self, parameters=parameters):
        totalLength = self.tenonSpacerStructure.totalLength - (
            0 if self.tenonSpacerStructure.fixedElementIsOnEdges else 2 * parameters.cutWidth
        )
        spacingLength = self.tenonSpacerStructure.spacingLength + 2 * parameters.cutWidth
        elementLength = self.tenonSpacerStructure.elementLength - 2 * parameters.cutWidth
        spacingLengthOnSides = 0 if self.tenonSpacerStructure.fixedElementIsOnEdges else spacingLength - parameters.cutWidth

        object.__setattr__(self, "spacingCount", self.tenonSpacerStructure.spacingCount)
        object.__setattr__(self, "elementCount", self.tenonSpacerStructure.elementCount)
        object.__setattr__(self, "spacingLength", spacingLength)
        object.__setattr__(self, "spacingLengthOnSides", spacingLengthOnSides)
        object.__setattr__(self, "elementLength", elementLength)
        object.__setattr__(self, "totalLength", totalLength)

def sliderSpacer(slideOnLength: bool, parameters=parameters) -> SpacerStructureFromFixedElementAndVariableSpacing:
    totalLength = parameters.fullLength if slideOnLength else parameters.fullHeight
    totalLength -= 4 * parameters.structuralWoodThickness + 2 * parameters.coverWoodThickness + 2 * parameters.clearanceMargin + parameters.frictionMargin
    return SpacerStructureFromFixedElementAndVariableSpacing(
        totalLength=totalLength,
        elementLength=parameters.tenonWidth,
        targetSpacing=parameters.tenonSpacerTarget,
        minimalSpacing=parameters.tenonSpacerMinimalLength,
        fixedElementIsOnEdges=True
    )

def innerBoxBottomSpacer(parameters=parameters) -> SpacerStructureFromFixedElementAndVariableSpacing:
    return SpacerStructureFromFixedElementAndVariableSpacing(
        totalLength=parameters.fullLength - 2 * (parameters.coverWoodThickness + 4 * parameters.structuralWoodThickness + parameters.frictionMargin + parameters.clearanceMargin),
        elementLength=parameters.tenonWidth,
        targetSpacing=parameters.tenonSpacerTarget,
        minimalSpacing=parameters.tenonSpacerMinimalLength,
        fixedElementIsOnEdges=False
    )

def innerBoxSideSpacer(parameters=parameters) -> SpacerStructureFromFixedElementAndVariableSpacing:
    return SpacerStructureFromFixedElementAndVariableSpacing(
        totalLength=parameters.fullHeight - 2 * (parameters.coverWoodThickness + 3 * parameters.structuralWoodThickness + parameters.frictionMargin + parameters.clearanceMargin),
        elementLength=parameters.tenonWidth,
        targetSpacing=parameters.tenonSpacerTarget,
        minimalSpacing=parameters.tenonSpacerMinimalLength,
        fixedElementIsOnEdges=True
    )

@dataclass (frozen=True)
class SpacerStructureFromVariableElement:

    totalLength: float
    targetElementLength: float
    minimalElementLength: float
    elementCountIsEven: bool

    elementLength: float = field(init=False)
    elementCount: int = field(init=False)

    def __post_init__(self):
        countRaw = self.totalLength / self.targetElementLength
        oneIfOdd = 0 if self.elementCountIsEven else 1
        countLow = math.floor((countRaw + oneIfOdd) / 2) * 2 - oneIfOdd
        countHigh = math.ceil((countRaw + oneIfOdd) / 2) * 2 - oneIfOdd
        lengthLong = self.totalLength / countLow
        lengthShort = self.totalLength / countHigh
        
        useLongElements = lengthShort < self.minimalElementLength or lengthLong - self.targetElementLength < self.targetElementLength - lengthShort

        if useLongElements :
            count = countLow
            length = lengthLong
        else :
            count = countHigh
            length = lengthShort
        
        object.__setattr__(self, "elementCount", count)
        object.__setattr__(self, "elementLength", length)

def innerBoxJunctionSpacer(parameters=parameters):
    return SpacerStructureFromVariableElement(
        totalLength = parameters.fullWidth - 2 * (parameters.coverWoodThickness + parameters.structuralWoodThickness),
        targetElementLength = parameters.tenonWidth,
        minimalElementLength = parameters.tenonSpacerMinimalLength,
        elementCountIsEven = False
    )