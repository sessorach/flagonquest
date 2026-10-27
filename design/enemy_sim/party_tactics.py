"""Party tactics (2026-10-27): how the whole party plays, as one switch.

Per the designer: the sim should be able to switch the party between
playing cautious, staying at max range, diving in and so on without a
script doing it by hand. Each PC's own Play Style (sample_pcs.csv) is
the default; a preset here hands out styles by role instead, and can set
the party's targeting and a few tunables too.

Roles, worked out from the built character: "support" (a healer),
"ranged" (a weapon with a range stat), "front" (Medium or Heavy armor,
or a shield) and "melee" (the rest). Styles are play_styles.py's:
Diver, Skirmisher, Back-liner, Kiter, Holder, Guardian. Targeting is
tactics.PARTY_TARGETING's: "table" (the default: focus fire, done
imperfectly), "threat" (perfect focus fire), "wounded" (finish the
weakest) or "closest".

Presets combine with "+", later ones winning: "max range+focus fire".

    import party_tactics
    party_tactics.use("cautious")      # every fight from here on
    party_tactics.use(None)            # back to each PC's own Play Style

or `-t "cautious"` on calibrate.py, compare_builds.py and the sweep
studies, and tactics_compare.py to run a party under every preset.
"""
import tactics
import tunables as T

ROLES = ("front", "melee", "ranged", "support")

PRESETS = {
    # Each PC by its own Play Style column.
    "as built": {},
    # Everyone goes in for the best target they can reach.
    "all in": {"styles": dict.fromkeys(ROLES, "Diver"), "tunables": {"RECKLESS_CHANCE": 0.0}},
    # Nobody dives: melee works the edges, shooters and healers hang back,
    # and nobody gets reckless.
    "cautious": {"styles": {"front": "Skirmisher", "melee": "Skirmisher", "ranged": "Back-liner",
                            "support": "Back-liner"},
                 "tunables": {"RECKLESS_CHANCE": 0.0}},
    # Shooters stay at the edge of their reach and back off from anything
    # that closes in; the rest play as built.
    "max range": {"styles": {"ranged": "Kiter", "support": "Back-liner"}},
    # The front holds and lets the enemy come; everyone else hangs back.
    "hold the line": {"styles": {"front": "Holder", "melee": "Holder", "ranged": "Back-liner",
                                 "support": "Back-liner"}},
    # Front-liners stick to the frailest ally who hangs back and fight
    # whatever's on them.
    "bodyguard": {"styles": {"front": "Guardian", "melee": "Guardian"}},
    # Targeting only.
    "focus fire": {"targeting": "threat"},
    "nearest first": {"targeting": "closest"},
    "finish the weakest": {"targeting": "wounded"},
}

_SAVED = {}


def _parts(spec):
    names = [p.strip() for p in (spec or "").split("+") if p.strip()]
    unknown = [n for n in names if n not in PRESETS]
    if unknown:
        raise KeyError(f"unknown party tactic(s) {unknown}; known: {sorted(PRESETS)}")
    return [PRESETS[n] for n in names]


def use(spec):
    """Turns a preset (or "a+b") on for every fight from here on, or None
    to go back to each PC's own Play Style. Puts back whatever the last
    preset changed first."""
    for (where, key), value in _SAVED.items():
        setattr(where, key, value)
    _SAVED.clear()
    T.PARTY_TACTIC = spec or None
    for part in _parts(spec):
        for key, value in part.get("tunables", {}).items():
            _SAVED.setdefault((T, key), getattr(T, key))
            setattr(T, key, value)
        if "targeting" in part:
            _SAVED.setdefault((tactics, "PARTY_TARGETING"), tactics.PARTY_TARGETING)
            tactics.PARTY_TARGETING = part["targeting"]


def role(attack_range, armor, has_shield, support):
    if support:
        return "support"
    if attack_range and attack_range > T.MELEE_RANGE:
        return "ranged"
    if armor in ("Medium", "Heavy") or has_shield:
        return "front"
    return "melee"


def style_for(role_name, own_style):
    """The Play Style this PC gets under the active preset: its own unless
    a preset names one for its role."""
    style = own_style
    for part in _parts(T.PARTY_TACTIC):
        style = part.get("styles", {}).get(role_name, style)
    return style
