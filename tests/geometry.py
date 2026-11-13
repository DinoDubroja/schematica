"""Compare independently rendered PDF segments with the accepted palette."""
from core import BP_MM


def segments(drawings, center=None):
    lines, widths = [], []
    for drawing in drawings:
        if drawing["type"] != "s":
            continue
        widths.append(drawing["width"] * BP_MM)
        first, last = None, None
        for item in drawing["items"]:
            if item[0] == "l":
                a, b = item[1:3]
                first = first or a
                last = b
                lines.append((tuple(a), tuple(b)))
            elif item[0] == "re":
                rect = item[1]
                points = [rect.tl, rect.tr, rect.br, rect.bl, rect.tl]
                lines.extend((tuple(a), tuple(b)) for a, b in zip(points, points[1:]))
            elif item[0] == "c":
                points = item[1:]
                first = first or points[0]
                last = points[-1]
                lines.append(tuple(tuple(p) for p in points))
            else:
                raise AssertionError(f"Unexpected geometry {item[0]}")
        if drawing.get("closePath") and first and last and first != last:
            lines.append((tuple(last), tuple(first)))
    points = [p for line in lines for p in line]
    if center is None:
        center = ((min(p[0] for p in points)+max(p[0] for p in points))/2,
                  (min(p[1] for p in points)+max(p[1] for p in points))/2)
    normalized = []
    for line in lines:
        points = tuple(((a[0]-center[0])*BP_MM, (a[1]-center[1])*BP_MM) for a in line)
        normalized.append(min(points, tuple(reversed(points))))
    return normalized, widths


def nearest_error(actual, expected):
    assert len(actual) == len(expected), (len(actual), len(expected))
    unmatched = list(expected)
    error = 0
    for line in actual:
        def distance(other):
            if len(line) != len(other):
                return float("inf")
            return max(abs(a-b) for p,q in zip(line, other) for a,b in zip(p,q))
        best = min(unmatched, key=distance)
        error = max(error, distance(best))
        unmatched.remove(best)
    return error
