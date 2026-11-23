"""QAN PI parametric geometry helpers.

Angles are radians internally. Degree conversion is explicit so geometry
sampling remains deterministic and easy to audit.
"""
from __future__ import annotations
from math import cos, pi, radians, sin

PI = pi
TAU = 2.0 * PI

def deg_to_rad(degrees: float) -> float:
    return radians(degrees)

def rad_to_deg(angle: float) -> float:
    return angle * 180.0 / PI

def polar(radius: float, angle: float, *, y: float = 0.0, center=(0.0, 0.0, 0.0)):
    """Return an X/Y/Z point on an XZ-plane circle."""
    cx, cy, cz = center
    return (cx + radius * cos(angle), cy + y, cz + radius * sin(angle))

def ring_points(radius: float, segments: int = 360, *, y: float = 0.0, center=(0.0, 0.0, 0.0), closed: bool = True):
    """Sample a circular ring using TAU; optionally repeat the first point."""
    if radius <= 0 or segments < 3:
        raise ValueError("radius must be positive and segments must be at least 3")
    points = [polar(radius, TAU * i / segments, y=y, center=center) for i in range(segments)]
    if closed:
        points.append(points[0])
    return points

def helix_points(radius: float, pitch: float, turns: float, segments_per_turn: int = 64, *, center=(0.0, 0.0, 0.0)):
    """Sample a parametric helix for ramps and spiral guideways."""
    if radius <= 0 or pitch == 0 or turns <= 0 or segments_per_turn < 3:
        raise ValueError("radius/turns must be positive, pitch nonzero, and sampling >= 3")
    count = max(2, int(segments_per_turn * turns))
    return [polar(radius, TAU * turns * i / count, y=pitch * turns * i / count, center=center) for i in range(count + 1)]

def circle_circumference(radius: float) -> float:
    if radius < 0:
        raise ValueError("radius cannot be negative")
    return TAU * radius

def circle_area(radius: float) -> float:
    if radius < 0:
        raise ValueError("radius cannot be negative")
    return PI * radius * radius
