from dataclasses import dataclass
import math
from parameters import parameters

@dataclass (frozen=True)
class FakeCutDimensions:

    @property
    def height(self) -> float:
        return parameters.coverWoodThickness + parameters.structuralWoodThickness

    @property
    def passesCount(self) -> int:
        return math.ceil(self.height / parameters.traceCutWidth)
        
    @property
    def initialEdgeDistance(self) -> float:
        return (
            self.height
            - parameters.traceCutWidth * self.passesCount
            + parameters.traceCutWidth / 2
        )