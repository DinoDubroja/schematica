"""Small, explicit search vocabulary; agents may also supply structured filters."""
import copy
import re

from core import ValidationError

FIELDS = {"family", "style", "variant", "terms", "size", "stroke", "ids"}
STYLES = {"european": "eu", "europe": "eu", "iec": "eu", "eu": "eu",
          "american": "us", "ansi": "us", "us": "us"}
VARIANTS = {"normal": "fixed", "standard": "fixed", "fixed": "fixed",
            "variable": "variable", "adjustable": "variable", "rheostat": "variable",
            "trimmer": "trimmer", "potentiometer": "potentiometer", "ntc": "ntc",
            "ptc": "ptc", "thermistor": "thermistor", "nonlinear": "nonlinear",
            "photoresistor": "photo"}
FAMILIES = {"resistor": "resistors", "resistors": "resistors",
            "capacitor": "capacitors", "capacitors": "capacitors",
            "inductor": "inductors", "inductors": "inductors",
            "opamp": "amplifiers", "amplifier": "amplifiers", "amplifiers": "amplifiers"}
FILLER = set("show me the a an of ones one only instead symbols symbol you have please use with stroke size designs design all browse whole library dev thicker thinner larger smaller medium thick thin small large".split())


def interpret(query="", previous=None, filters=None):
    if not isinstance(query, str) or len(query) > 2000:
        raise ValidationError("Search must be text of at most 2000 characters")
    words = re.findall(r"[a-z0-9-]+", query.lower().replace("op-amp", "opamp"))
    result = copy.deepcopy(previous or {})
    if any(w in words for w in ("browse", "whole")) or query.lower().strip() in ("all", "browse all"):
        result = {}
    styles = [STYLES[w] for w in words if w in STYLES]
    variants = [VARIANTS[w] for w in words if w in VARIANTS]
    families = [FAMILIES[w] for w in words if w in FAMILIES]
    if families:
        if result.get("family") != families[-1]:
            for key in ("variant", "style", "terms", "ids"):
                result.pop(key, None)
        result["family"] = families[-1]
    if styles:
        result["style"] = styles[-1]
    if variants:
        result["variant"] = variants[-1]
        result.pop("terms", None)
        result.pop("ids", None)
    for key, values in (("size", ("small", "medium", "large")), ("stroke", ("thin", "medium", "thick"))):
        aliases = {"thicker": "thick", "thinner": "thin"} if key == "stroke" else {"larger": "large", "smaller": "small"}
        choices = [aliases.get(w, w) for w in words if w in values or w in aliases]
        if choices:
            result[key] = choices[-1]
    terms = [w for w in words if w not in FILLER | STYLES.keys() | VARIANTS.keys() | FAMILIES.keys()]
    if terms:
        result["terms"] = terms
    if filters is not None:
        if not isinstance(filters, dict) or set(filters) - FIELDS:
            raise ValidationError("Unknown search filter")
        for key, value in filters.items():
            if value is None:
                result.pop(key, None)
            else:
                result[key] = value
    for key in ("terms", "ids"):
        if key in result and (not isinstance(result[key], list) or any(not isinstance(s, str) for s in result[key])):
            raise ValidationError(f"{key} must be a list of strings")
    for key in ("family", "style", "variant", "size", "stroke"):
        if key in result and not isinstance(result[key], str):
            raise ValidationError(f"{key} must be text")
    for key, values in (("size", {"small", "medium", "large"}), ("stroke", {"thin", "medium", "thick"}), ("style", {"eu", "us"})):
        if key in result and result[key] not in values:
            raise ValidationError(f"Unknown {key}")
    return result


def matches(symbol, filters):
    sid = symbol["id"]
    if "ids" in filters and sid not in filters["ids"]:
        return False
    family = filters.get("family")
    if family:
        types = symbol.get("types", [])
        inferred = {"resistors": "resistor", "capacitors": "capacitor", "inductors": "inductor", "amplifiers": "active"}.get(family)
        if symbol.get("family") != family and inferred not in types:
            return False
    style = filters.get("style")
    if style and not (sid.endswith("-" + style) or symbol.get("drawing", {}).get("body") == style):
        return False
    variant = filters.get("variant")
    actual = symbol.get("drawing", {}).get("variant", symbol.get("attributes", {}).get("variant"))
    if variant == "fixed":
        if symbol.get("recipe") not in ("resistor-eu", "resistor-us") and actual != "fixed":
            return False
    elif variant and actual != variant:
        return False
    text = " ".join([sid, symbol["name"], symbol["description"], *symbol.get("keywords", []), *symbol.get("types", [])]).lower()
    return all(word.lower() in text for word in filters.get("terms", []))
