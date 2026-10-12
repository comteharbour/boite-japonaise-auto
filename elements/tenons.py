from drawing import Rectangle, Line
from parameters import parameters

def tenon(xStartLeft: bool, yStartUp: bool, parameters=parameters) -> Line:
    h = parameters.structuralWoodThickness - parameters.tenonLengthMargin
    w = parameters.tenonWidth
    b = parameters.tenonBevelHeight
    flipX = 1 if xStartLeft else -1
    flipY = 1 if yStartUp else -1
    return Line.movesFromOrigin(
        (0, flipY*(h-b)),
        (flipX*b, flipY*b),
        (flipX*(w-2*b),0),
        (flipX*b, -flipY*b),
        (0, -flipY*(h-b))
    )

def tenonHole(horizontal: bool, parameters=parameters):
    width = parameters.tenonWidth - 2 * parameters.cutWidth
    height = parameters.structuralWoodThickness
    if horizontal: return Rectangle.fromCoords(width, height)
    else: return Rectangle.fromCoords(height, width)
