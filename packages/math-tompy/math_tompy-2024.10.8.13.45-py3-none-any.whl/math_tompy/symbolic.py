from dataclasses import dataclass
from decimal import Decimal
from math import inf
from typing import Callable, Self, Optional, Any

import sympy as sp

from ..math_tompy.exceptions import EmptyListError


@dataclass
class Calculation:
    operation: Callable
    value0: Self | Decimal
    value1: Self | Decimal

    def result(self):
        value0: Calculation | Decimal = self.value0
        value1: Calculation | Decimal = self.value1

        if isinstance(value0, Calculation):
            value0 = value0.result()
        if isinstance(value1, Calculation):
            value1 = value1.result()

        return self.operation(value0, value1)


def expr_to_calc(expression: sp.S) -> Calculation:
    calculation: Calculation | None = None
    operation: Optional[Callable] = None
    value0: Calculation | Decimal | None = None
    value1: Calculation | Decimal | None = None

    if len(expression.args) == 0:
        if isinstance(expression, sp.Rational | sp.Integer | sp.core.numbers.Half):
            operation = Decimal.__truediv__
            value0 = Decimal(expression.p)
            value1 = Decimal(expression.q)
        elif isinstance(expression, sp.Float):
            operation = Decimal.__add__
            value0 = Decimal(float(expression.num))
            value1 = Decimal(0)
        else:
            raise TypeError(f"Expression type '{type(expression)}' not yet supported.")
    else:
        if isinstance(expression, sp.Mul):
            operation = Decimal.__mul__
        elif isinstance(expression, sp.Pow):
            operation = Decimal.__pow__
        elif isinstance(expression, sp.Expr):
            if isinstance(expression.args[0], sp.Expr):
                calculation = expr_to_calc(expression=expression.args[0])
            elif isinstance(expression.args[0], int):
                calculation = Calculation(Decimal.__add__, value0=expression.args[0], value1=Decimal(0))
        else:
            raise TypeError(f"Expression type '{type(expression)}' not yet supported.")

        if calculation is None:
            value0 = expr_to_calc(expression=expression.args[0])
            value1 = expr_to_calc(expression=expression.args[1])

    if calculation is None and operation is not None and value0 is not None and value1 is not None:
        calculation = Calculation(operation=operation, value0=value0, value1=value1)
    else:
        raise ValueError(f"Unexpected values of operation '{operation}', value0 '{value0}', and value1 '{value1}'.")

    return calculation


def bounding_box(points: list[sp.Point2D]) -> tuple[sp.Point2D, float, float]:
    # Calculates axis-oriented bounding box for point cloud
    # Outputs bottom-left point, height, and width
    if len(points) == 0:
        raise EmptyListError(f"Input list is empty.")

    x_min = inf
    x_max = -inf
    y_min = inf
    y_max = -inf

    for point in points:
        x = point.x
        y = point.y

        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y

    point = sp.Point2D(x_min, y_min)
    width = x_max - x_min
    height = y_max - y_min
    return point, width, height


def middle(points: list[sp.Point2D]) -> sp.Point2D:
    point, width, height = bounding_box(points=points)

    x = point.x + (width / 2)
    y = point.y + (height / 2)

    point: sp.Point2D = sp.Point2D(x, y)

    return point


def centroid(points: list[sp.Point2D]) -> sp.Point2D:
    point_amount: int = len(points)

    xs = [point.x for point in points]
    ys = [point.y for point in points]

    x = sum(xs) / point_amount
    y = sum(ys) / point_amount

    point: sp.Point2D = sp.Point2D(x, y)

    return point


def along_line(start: sp.Point2D, end: sp.Point2D, fraction: float) -> sp.Point2D:
    x_difference = end.x - start.x
    y_difference = end.y - start.y

    x_modified = x_difference * fraction
    y_modified = y_difference * fraction

    x = start.x + x_modified
    y = start.y + y_modified

    point: sp.Point2D = sp.Point2D(x, y)

    return point


def distance(position0: sp.Point2D, position1: sp.Point2D) -> Any:
    distance_ = position0.distance(other=position1)
    return distance_
