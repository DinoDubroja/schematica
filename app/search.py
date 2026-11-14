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
            "diode": "diodes", "diodes": "diodes",
            "inductor": "inductors", "inductors": "inductors",
            "opamp": "amplifiers", "amplifier": "amplifiers", "amplifiers": "amplifiers",
            "transistor": "transistors", "transistors": "transistors",
            "logic": "logic", "analog": "analog"}
for family in ("inductors-and-transformers", "sources-and-grounds", "switches-and-relays",
               "connections-and-instruments", "protection-and-resonators"):
    FAMILIES[family] = family
TERMS = {"grounds": "ground", "sources": "source", "switches": "switch",
         "relays": "relay", "transformers": "transformer", "fuses": "fuse"}
FILLER = set("show me the a an of ones one only instead symbols symbol you have please use with stroke size designs design all browse whole library dev thicker thinner larger smaller medium thick thin small large".split())


def interpret(query="", previous=None, filters=None):
    if not isinstance(query, str) or len(query) > 2000:
        raise ValidationError("Search must be text of at most 2000 characters")
    normalized = query.lower().replace("op-amp", "opamp")
    for family in FAMILIES:
        if "-" in family:
            normalized = re.sub(r"\b" + re.escape(family.replace("-", " ")) + r"\b", family, normalized)
    words = re.findall(r"[a-z0-9-]+", normalized)
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
    terms = [TERMS.get(w, w) for w in words if w not in FILLER | STYLES.keys() | VARIANTS.keys() | FAMILIES.keys()]
    if terms:
        if not families and not styles and not variants:
            # A new subject must not remain trapped in the previous family.
            for key in ("family", "variant", "style", "ids"):
                result.pop(key, None)
        result["terms"] = terms
    if filters is not None:
        if not isinstance(filters, dict) or set(filters) - FIELDS:
            raise ValidationError("Unknown search filter")
        for key, value in filters.items():
            if value is None:
                result.pop(key, None)
            else:
                # Hosts may supply the same singular family names they use in
                # natural language. Do not let that override a valid query with
                # a filter that silently hides the whole family.
                if key == "family" and isinstance(value, str):
                    value = value.strip().lower()
                    value = FAMILIES.get(value, value)
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
    # Batch family tags are umbrella labels, not evidence that each member is
    # every named type (for example a source is not necessarily a ground).
    family_tag = symbol.get("family", "")
    umbrella = {family_tag, family_tag.replace("-", " "), family_tag.replace("-and-", " ").replace("-", " ")}
    tags = [tag for tag in [*symbol.get("keywords", []), *symbol.get("types", [])] if tag.lower() not in umbrella]
    text = " ".join([sid, symbol["name"], symbol["description"], *tags]).lower()
    return all(word.lower() in text for word in filters.get("terms", []))
