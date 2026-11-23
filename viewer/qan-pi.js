// QAN PI parametric geometry core for the browser observer.
// Radians are the canonical unit; degree conversion is explicit.
export const PI = Math.PI;
export const TAU = 2 * PI;
export const degToRad = degrees => degrees * PI / 180;
export const radToDeg = radians => radians * 180 / PI;

export function polar(radius, angle, y = 0, center = [0, 0, 0]) {
  return [center[0] + radius * Math.cos(angle), center[1] + y, center[2] + radius * Math.sin(angle)];
}

export function ringPoints(radius, segments = 360, y = 0, center = [0, 0, 0]) {
  if (!(radius > 0) || !Number.isInteger(segments) || segments < 3) throw new Error("Invalid QAN PI ring parameters");
  const points = Array.from({ length: segments }, (_, i) => polar(radius, TAU * i / segments, y, center));
  points.push(points[0].slice());
  return points;
}

export function helixPoints(radius, pitch, turns = 1, segmentsPerTurn = 64, center = [0, 0, 0]) {
  if (!(radius > 0) || pitch === 0 || !(turns > 0) || segmentsPerTurn < 3) throw new Error("Invalid QAN PI helix parameters");
  const count = Math.max(2, Math.ceil(segmentsPerTurn * turns));
  return Array.from({ length: count + 1 }, (_, i) => polar(radius, TAU * turns * i / count, pitch * turns * i / count, center));
}
