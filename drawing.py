from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum
from typing import Self

class GeometryError(Exception):
    pass

def group(elements: list[str]) -> str:
    children = "\n".join(elements)
    return f"""<g>
            {children}
        </g>"""

def generate_svg(elements):
    children = "\n".join(elements)
    return f"""<svg
            xmlns="http://www.w3.org/2000/svg"
            width="720mm"
            height="430mm"
            viewBox="0 0 720 430"
        >
        {children}
        </svg>"""

class LaserType(Enum):
    TRACE = "trace"
    INNERCUT = "innerCut"
    OUTERCUT = "outerCut"

def style(laserType: LaserType):
    match laserType:
        case LaserType.TRACE:
            return """fill="none"
                stroke-width="1"
                stroke="#000000" """
        case LaserType.INNERCUT:
            return """fill="none"
                stroke-width="0.2"
                stroke="#FF0000" """
        case LaserType.OUTERCUT:
            return """fill="none"
                stroke-width="0.2"
                stroke="#0000FF" """
    return

@dataclass (frozen=True)
class Point:
    x: float
    y: float

    def __add__(self, otherPoint: Self) -> Self:
        return Point(self.x + otherPoint.x, self.y + otherPoint.y)

    def __mul__(self, scalar: float) -> Self:
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Self:
        return self * scalar

    def __sub__(self, otherPoint: Self) -> Self:
        return self + (-1 * otherPoint)
    
    def rotate90xtoy(self, pivot: Self) -> Self:
        return Point(pivot.x - (self.y - pivot.y), pivot.y + (self.x - pivot.x))

    def rotate180(self, pivot: Self) -> Self:
        return Point(2 * pivot.x - self.x, 2 * pivot.y - self.y)

    def rotate90ytox(self, pivot: Self) -> Self:
        return Point(pivot.x + (self.y - pivot.y), pivot.y - (self.x - pivot.x))
    
    def flipHorizontal(self, xVerticalMirror=0) -> Self :
        return Point(2 * xVerticalMirror - self.x, self.y)
    
    def flipVertical(self, yHorizontalMirror=0) -> Self :
        return Point(self.x, 2 * yHorizontalMirror - self.y)

@dataclass(frozen=True)
class BoundingBox:
    xMin: float
    yMin: float
    xMax: float
    yMax: float

    @property
    def width(self):
        return self.xMax - self.xMin
    
    @property
    def height(self):
        return self.yMax - self.yMin
    
    @property
    def center(self):
        return Point(
            (self.xMin + self.xMax) / 2,
            (self.yMin + self.yMax) / 2
        )

    @property
    def upLeft(self):
        return Point(self.xMin, self.yMin)

    @property
    def downLeft(self):
        return Point(self.xMin, self.yMax)
    
    @property
    def downRight(self):
        return Point(self.xMax, self.yMax)

    @property
    def upRight(self):
        return Point(self.xMax, self.yMin)

class SVGObject (ABC):
    @abstractmethod
    def __add__ (self, vector: Point) -> Self:
        pass

    @abstractmethod
    def __sub__ (self, vector: Point) -> Self:
        pass

    @abstractmethod
    def rotate90xtoy (self, pivot: Point) -> Self:
        pass

    @abstractmethod
    def rotate180 (self, pivot: Point) -> Self:
        pass

    @abstractmethod
    def rotate90ytox (self, pivot: Point) -> Self:
        pass

    @abstractmethod
    def flipHorizontal (self, xVerticalMirror: float) -> Self:
        pass

    @abstractmethod
    def flipVertical (self, yHorizontalMirror: float) -> Self:
        pass

    @property
    @abstractmethod
    def boundingBox (self) -> BoundingBox:
        pass

    def placeUpLeftAtOrigin(self) -> Self:
        return self - self.boundingBox.upLeft

    def placeUpLeftAtPoint(self, point: Point) -> Self:
        return self.placeUpLeftAtOrigin() + point

    @abstractmethod
    def getSVG(self, laserType: LaserType):
        pass

@dataclass (frozen=True)
class Group (SVGObject):
    children: tuple[SVGObject, ...]

    def __post_init__(self):
        if not self.children:
            raise GeometryError(
                "Empty group is forbidden"
            )

    def __add__(self, vector) -> Self:
        return Group(
            tuple(obj + vector for obj in self.children)
        )

    def __sub__(self, vector) -> Self:
        return Group(
            tuple(obj - vector for obj in self.children)
        )

    def rotate90xtoy(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return Group(
            tuple(obj.rotate90xtoy(pivot) for obj in self.children)
        )
    
    def rotate180(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return Group(
            tuple(obj.rotate180(pivot) for obj in self.children)
        )
    
    def rotate90ytox(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return Group(
            tuple(obj.rotate90ytox(pivot) for obj in self.children)
        )
    
    def flipHorizontal(self, xVerticalMirror: float | None = None) -> Self:
        if xVerticalMirror is None: xVerticalMirror = self.boundingBox.center.x
        return Group(
            tuple(obj.flipHorizontal(xVerticalMirror) for obj in self.children)
        )
    
    def flipVertical(self, yHorizontalMirror: float | None = None) -> Self:
        if yHorizontalMirror is None: yHorizontalMirror = self.boundingBox.center.y
        return Group(
            tuple(obj.flipVertical(yHorizontalMirror) for obj in self.children)
        )

    @property
    def boundingBox(self) -> BoundingBox:
        return BoundingBox(
            xMin=min(child.boundingBox.xMin for child in self.children),
            yMin=min(child.boundingBox.yMin for child in self.children),
            xMax=max(child.boundingBox.xMax for child in self.children),
            yMax=max(child.boundingBox.yMax for child in self.children)
        )

    def placeUpLeftAtShape(self, shape: SVGObject) -> Self:
        return self.placeUpLeftAtOrigin() + shape.boundingBox.upLeft

    def getSVG(self, laserType: LaserType):
        return group((
            child.getSVG(laserType)
            for child in self.children
        ))

@dataclass (frozen=True)
class PolyLine:
    points: tuple[Point, ...]

    def __iter__(self):
        return iter(self.points)
        
    def __getitem__(self, index):
        return self.points[index]
        
    def __len__(self):
        return len(self.points)

    @property
    def pivot(self) -> Point:
        return self.points[0]

    @property
    def boundingBox(self) -> BoundingBox:
        xs = [point.x for point in self.points]
        ys = [point.y for point in self.points]

        return BoundingBox(
            min(xs),
            min(ys),
            max(xs),
            max(ys)
        )
         

    def __add__(self, vector: Point) -> Self:
        return PolyLine(
            tuple(
                point + vector
                for point in self.points
            )
        )

    def __sub__(self, vector: Point) -> Self:
        return PolyLine(
            tuple(
                point - vector
                for point in self.points
            )
        )

    def rotate90xtoy (self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return PolyLine(
            tuple(
                point.rotate90xtoy(pivot)
                for point in self.points
            )
        )

    def rotate180 (self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return PolyLine(
            tuple(
                point.rotate180(pivot)
                for point in self.points
            )
        )

    def rotate90ytox (self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return PolyLine(
            tuple(
                point.rotate90ytox(pivot)
                for point in self.points
            )
        )

    def flipHorizontal (self, xVerticalMirror: float | None = None) -> Self:
            if xVerticalMirror is None: xVerticalMirror = self.boundingBox.center.x
            return PolyLine(
                tuple(
                    point.flipHorizontal(xVerticalMirror)
                    for point in self.points
                )
            )

    def flipVertical (self, yHorizontalMirror: float | None = None) -> Self:
        if yHorizontalMirror is None: yHorizontalMirror = self.boundingBox.center.y
        return PolyLine(
            tuple(
                point.flipVertical(yHorizontalMirror)
                for point in self.points
            )
        )

@dataclass (frozen=True)
class Line (SVGObject):
    polyLine: PolyLine
    close: bool = False

    @classmethod
    def fromCoords(cls, *coords):
        return cls(
            PolyLine(
                tuple(
                    Point(x, y)
                    for x, y in coords
                )
            )
        )

    @classmethod
    def movesFromOrigin(cls, *moves):
        points = [Point(0,0)]
        for dx, dy in moves:
            points.append(
            points[-1] + Point(dx, dy)
        )
        
        return cls(
            PolyLine(
                tuple(points)
            ),
        )

    def concat(self, otherLine: Self) -> Self:
        lastSelfPoint = self.polyLine.points[-1]
        firstOtherPoint = otherLine.polyLine.points[0]
        translation = lastSelfPoint - firstOtherPoint
        otherLineAtEnd = otherLine + translation
        return Line(
            PolyLine(
                self.polyLine.points[:-1] + otherLineAtEnd.polyLine.points
            )
        )

    def setClose(self, close: bool) -> Self:
        return Line(
            self.polyLine,
            close
        )

    @property
    def boundingBox(self) -> BoundingBox:
        return self.polyLine.boundingBox
    
    def __add__(self, vector: Point) -> Self:
        return Line(
            self.polyLine + vector,
            self.close
        )

    def __sub__(self, vector: Point) -> Self:
            return Line(
                self.polyLine - vector,
                self.close
            )

    def rotate90xtoy(self, pivot: Point | None = None) -> Self:
        return Line(
            self.polyLine.rotate90xtoy(pivot),
            self.close
        )

    def rotate180(self, pivot: Point | None = None) -> Self:
            return Line(
                self.polyLine.rotate180(pivot),
                self.close
            )

    def rotate90ytox(self, pivot: Point | None = None) -> Self:
            return Line(
                self.polyLine.rotate90ytox(pivot),
                self.close
            )

    def flipHorizontal(self, xVerticalMirror: float | None = None) -> Self:
            return Line(
                self.polyLine.flipHorizontal(xVerticalMirror),
                self.close
            )

    def flipVertical(self, yHorizontalMirror: float | None = None) -> Self:
        return Line(
            self.polyLine.flipVertical(yHorizontalMirror),
            self.close
        )

    def getSVG(self, laserType: LaserType):
        if len(self.polyLine) < 2: return ""
        
        d = f"M {self.polyLine[0].x} {self.polyLine[0].y}"
        for point in self.polyLine[1:]:
            d += f" L {point.x} {point.y}"
        
        if self.close:
            d += " Z"
        
        path = f"""<path
                d="{d}"
                {style(laserType)}
            />"""
        
        return path

@dataclass (frozen=True)
class Rectangle (SVGObject):
    width: float
    height: float
    origin: Point = Point(0, 0)
    rx: float = 0
    ry: float = 0

    @classmethod
    def fromCoords(
        cls,
        width: float,
        height: float,
        originX: float = 0,
        originY: float = 0,
        rx: float = 0,
        ry: float = 0
    ):
        return cls(
            width,
            height,
            Point(originX, originY),
            rx,
            ry
        )

    @property
    def boundingBox(self) -> BoundingBox:
        return BoundingBox(
            self.origin.x,
            self.origin.y,
            self.origin.x + self.width,
            self.origin.y + self.height
        )
    
    def __add__(self, vector: Point) -> Self:
        return Rectangle(
            self.width,
            self.height,
            self.origin + vector,
            self.rx,
            self.ry
        )

    def __sub__(self, vector: Point) -> Self:
            return Rectangle(
                self.width,
                self.height,
                self.origin - vector,
                self.rx,
                self.ry
            )
    
    def rotate90xtoy(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return Rectangle(
            width=self.height,
            height=self.width,
            origin=self.origin.rotate90xtoy(pivot) - Point(self.height, 0),
            rx=self.ry,
            ry=self.rx
        )

    def rotate180(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return Rectangle(
            width=self.width,
            height=self.height,
            origin=self.origin.rotate180(pivot) - Point(self.width, self.height),
            rx=self.rx,
            ry=self.ry
        )

    def rotate90ytox(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return Rectangle(
            width=self.height,
            height=self.width,
            origin=self.origin.rotate90ytox(pivot) - Point(0, self.width),
            rx=self.ry,
            ry=self.rx
        )

    def flipHorizontal(self, xVerticalMirror: float | None = None) -> Self:
        if xVerticalMirror is None: xVerticalMirror = self.boundingBox.center.x
        ox = 2 * xVerticalMirror - (self.origin.x + self.width)
        oy = self.origin.y
        return Rectangle(
            self.width,
            self.height,
            Point(ox, oy),
            self.rx,
            self.ry
        )

    def flipVertical(self, yHorizontalMirror: float | None = None) -> Self:
        if yHorizontalMirror is None: yHorizontalMirror = self.boundingBox.center.y
        ox = self.origin.x
        oy = 2 * yHorizontalMirror - (self.origin.y + self.height)
        return Rectangle(
            self.width,
            self.height,
            Point(ox, oy),
            self.rx,
            self.ry
        )

    def getSVG(self, laserType: LaserType):
        return f"""<rect
                width="{self.width}"
                height="{self.height}"
                x="{self.origin.x}"
                y="{self.origin.y}"
                rx="{self.rx}"
                ry="{self.ry}"
                {style(laserType)}
            />"""

@dataclass (frozen=True)
class Circle (SVGObject):
    radius: float
    center: Point

    @classmethod
    def fromCoords(
        cls,
        radius: float,
        centerX: float = 0,
        centerY: float = 0
    ):
        return cls(
            radius,
            Point(centerX, centerY)
        )

    @property
    def boundingBox(self):
        return BoundingBox(
            self.center.x - self.radius,
            self.center.y - self.radius,
            self.center.x + self.radius,
            self.center.y + self.radius
        )
        
    def __add__(self, vector: Point) -> Self:
        return Circle(
            self.radius,
            self.center + vector
        )

    def __sub__(self, vector: Point) -> Self:
            return Circle(
                self.radius,
                self.center - vector
            )

    def rotate90xtoy(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return Circle(
            self.radius,
            self.center.rotate90xtoy(pivot)
        )

    def rotate180(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return Circle(
            self.radius,
            self.center.rotate180(pivot)
        )

    def rotate90ytox(self, pivot: Point | None = None) -> Self:
        if pivot is None: pivot = self.boundingBox.center
        return Circle(
            self.radius,
            self.center.rotate90ytox(pivot)
        )

    def flipHorizontal(self, xVerticalMirror: float | None = None) -> Self:
        if xVerticalMirror is None: xVerticalMirror = self.boundingBox.center.x
        return Circle(
            self.radius,
            self.center.flipHorizontal(xVerticalMirror)
        )

    def flipVertical(self, yHorizontalMirror: float | None = None) -> Self:
        if yHorizontalMirror is None: yHorizontalMirror = self.boundingBox.center.y
        return Circle(
            self.radius,
            self.center.flipVertical(yHorizontalMirror)
        )
    
    def getSVG(self, laserType: LaserType):
        return f"""<circle
                r="{self.radius}"
                cx="{self.center.x}"
                cy="{self.center.y}"
                {style(laserType)}
            />"""
