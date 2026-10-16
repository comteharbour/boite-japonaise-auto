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
    gapBetweenPiecesOnCuttingPlate: float
    coverPadding: float

# plywood 1.6mm
parameters = Parameters(
    fullLength=50,
    fullWidth=30,
    fullHeight=30,
    structuralWoodThickness=1.6,
    coverWoodThickness=0.6,
    tenonWidth=4,
    tenonBevelHeight=0.4,
    tenonLengthMargin=0,
    tenonSpacerTarget=6,
    tenonSpacerMinimalLength=3,
    frictionMargin=0.2,
    clearanceMargin=1,
    holeEdgeMargin=3,
    cutWidth=0.2,
    arrowLength=10,
    traceFiguresWidth=3,
    traceCutWidth=1,
    gapBetweenPiecesOnCuttingPlate=1,
    coverPadding=0
)

MDF3MMparameters = Parameters(
    fullLength=50,
    fullWidth=50,
    fullHeight=50,
    structuralWoodThickness=3,
    coverWoodThickness=1,
    tenonWidth=6,
    tenonBevelHeight=1,
    tenonLengthMargin=0.1,
    tenonSpacerTarget=4,
    tenonSpacerMinimalLength=3,
    frictionMargin=0.2,
    clearanceMargin=1,
    holeEdgeMargin=3,
    cutWidth=0.2,
    arrowLength=10,
    traceFiguresWidth=3,
    traceCutWidth=1,
    gapBetweenPiecesOnCuttingPlate=1,
    coverPadding=0.1
)

baseParameters = Parameters(
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
    gapBetweenPiecesOnCuttingPlate=1,
    coverPadding=0.1
)
