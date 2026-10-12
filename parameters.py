from dataclasses import dataclass

@dataclass
class Parameters:
    fullLength: float
    fullWidth: float
    fullHeight: float
    structuralWoodThickness: float
    coverWoodThickness: float
    tenonWidth: float
    tenonBevelHeight: float
    tenonLengthMargin: float
    tenonSpacerTarget: float
    tenonSpacerMinimalLength: float
    frictionMargin: float
    clearanceMargin: float
    holeEdgeMargin: float
    cutWidth: float
    arrowLength: float
    traceFiguresWidth: float
    traceCutWidth: float
    gapBetweenPieces: float
    coverPadding: float

smallParameters = Parameters(
    fullLength=50,
    fullWidth=50,
    fullHeight=50,
    structuralWoodThickness=3,
    coverWoodThickness=1,
    tenonWidth=4,
    tenonBevelHeight=1,
    tenonLengthMargin=0.2,
    tenonSpacerTarget=4,
    tenonSpacerMinimalLength=3,
    frictionMargin=0.2,
    clearanceMargin=1,
    holeEdgeMargin=3,
    cutWidth=0.2,
    arrowLength=3,
    traceFiguresWidth=3,
    traceCutWidth=1,
    gapBetweenPieces=1,
    coverPadding=0.1
)

parameters = Parameters(
    fullLength=76.8,
    fullWidth=51.6,
    fullHeight=50.6,
    structuralWoodThickness=3.8,
    coverWoodThickness=1,
    tenonWidth=8,
    tenonBevelHeight=1,
    tenonLengthMargin=0.4,
    tenonSpacerTarget=8,
    tenonSpacerMinimalLength=4,
    frictionMargin=0.2,
    clearanceMargin=1,
    holeEdgeMargin=3,
    cutWidth=0.2,
    arrowLength=20,
    traceFiguresWidth=4,
    traceCutWidth=1,
    gapBetweenPieces=1,
    coverPadding=0.1
)
