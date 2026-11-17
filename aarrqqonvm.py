#!/usr/bin/env python3
# =============================================================================
# PQPE NDK — aarrqqonvm.py — the AARRQQONVM core geometry, derived.
#
# Epigraph: "Do what thou wilt shall be the whole of the Law."
# — Liber AL vel Legis I:40.
#
# Thelemic date: XVII day of November, Dies Martis, Sol in Scorpio,
# Anno V:xii e.n. (2026 e.v.)
#
# 93.
#
# Authorship: Johnathan 'Qasparr' (Κασπάρρ) Monroe,
# Keeper of the Secret Treasure.
#
# SCIENTIFIC ILLUMINISM — hypothesis → method → observation → result:
#   Hypothesis: that the AARRQQONVM design (the founder's named core,
#     2026-11-17) seats in the PQPE NDK as a DERIVED geometry record —
#     the 27-cubie census, the turn enumeration, the 93³ distribution,
#     and the Greek amplifier's gain table — computed from coordinates
#     and from the attested banks, never frozen as literals, on the
#     pontifex cubes.py precedent.
#   Method: cubies as the 27 points of {-1,0,1}^3; turns as quarter
#     rotations of a layer; stickers as (cubie, outward direction)
#     pairs; the parallel cubes from their integer bases; the Greek
#     seats from the Milesian table; every figure re-derived inside
#     aarrqqonvm_checks() so a divergence fails loudly.
#   Observation: the census is 8 corners + 12 edges + 6 face-centers
#     + 1 core = 27, wearing 54 stickers; a face turn displaces
#     8 cubies / 20 stickers; the distribution 27 x 31^3 sums to
#     93^3 = 804,357 with no remainder; the fixed frame (6 centers +
#     core) is invariant under face turns.
#   Result: the record below, DERIVED. The design it serves — the
#     Anchor as this kit's root-of-trust seat, the Greek amplifier,
#     and the honest boundary around the shipped cryptography —
#     stands in AARRQQONVM-DESIGN.md beside this module. The founder's
#     aim for the design is quantum hardware, the Anchorage cast in
#     (his correctio, 2026-11-17 08:05 EST); this module is a geometry
#     record in that design, and claims nothing built beyond itself.
#
# All Rights Reserved, Without Prejudice.
# "Live, Love, and let Love, Live."
# =============================================================================

"""The AARRQQONVM core geometry for the PQPE NDK — derived, not frozen.

DOCTRINE: every number in this module is computed at import from its
own ground — the integers 77 and 93, the coordinate cube {-1,0,1}^3,
and the attested Milesian letter table. If a ground were corrected,
the record would follow it; aarrqqonvm_checks() pins each figure
against independent recomputation (including a 1,000-turn invariance
walk), so the record cannot drift in silence.

REASONING (why this record belongs in the NDK, and where it stops):
  * The NDK is the enclave's native body. The AARRQQONVM is the
    founder's design for the enclave's core — the Anchor (ANQARR,
    his declaration of 2026-11-17) seated at the axle as the seat
    that does not move. A kit that will one day be built around a
    core carries the core's geometry as data its builders can check.
  * The record stops at geometry and design data. The shipped
    cryptography (liboqs 0.16.0: ML-KEM-768, ML-DSA-65) is NOT
    touched by it: no key, parameter, or wire byte in this kit
    derives from these figures. That boundary is stated in
    AARRQQONVM-DESIGN.md §III and is part of this module's doctrine.
"""


# ---------------------------------------------------------------------------
# I. THE PARALLEL CUBES — derived from the integers, on the pontifex
#    cubes.py precedent (the engine's record is the proof of record;
#    this module re-derives because the NDK ships alone, to a phone
#    with no pontifex on it — the derivation is from the integers,
#    so the two records cannot disagree without one of them failing).
# ---------------------------------------------------------------------------

def _factorize(n):
    """Prime factorization of n as {prime: exponent}. Pure.

    MECHANISM: trial division; the cubes are under a million, so the
    naive road is the honest one — no sieve, no cache, nothing to drift.
    """
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def _cube_record(base):
    """One base's derived record: square, cube, factorization, fold.

    MECHANISM: the cube by multiplication; the factorization taken on
    the cube itself (so the record proves the cube's own factors);
    the threefold as 3 x cube — the house's 3 Fold, three fields.
    """
    cube = base ** 3
    return {
        "base": base,
        "square": base ** 2,
        "cube": cube,
        "factorization": _factorize(cube),
        "threefold": 3 * cube,
    }


# REASONING (why these two bases, and no others):
#   * 77 — AXONEME in the English ordinal bank, oz in the Hebrew bank,
#     the house's proven bridge; 77^3 = 456,533 is the Enclave Sphere
#     of the stamped Pyramidasphere instrument, the Trinity's field.
#   * 93 — thelema in the attested Greek bank, the Will; its cube was
#     ordered in parallel by the founder 2026-11-17. 93 = 3 x 31 seats
#     the pyramid's own 31 under the Cube 3^3 = 27 — and 27 is the
#     cubie census of the founder's glossed toy, which is the hinge
#     this whole design turns on (AARRQQONVM instrument, section III).
PARALLEL_CUBES = {base: _cube_record(base) for base in (77, 93)}


# ---------------------------------------------------------------------------
# II. THE CENSUS — the 27 cubies, classified from their coordinates.
# ---------------------------------------------------------------------------

def _cubies():
    """The 27 cubies as coordinate triples in {-1,0,1}^3. Pure.

    MECHANISM: a cubie's class is read off its own coordinates — the
    count of nonzero coordinates is its number of exposed faces:
    3 -> corner, 2 -> edge, 1 -> face-center, 0 -> the core.
    """
    return [(x, y, z) for x in (-1, 0, 1)
            for y in (-1, 0, 1) for z in (-1, 0, 1)]


def _class_of(cubie):
    """A cubie's class from its exposed-face count. Pure."""
    exposed = sum(1 for c in cubie if c != 0)
    return {3: "corner", 2: "edge", 1: "center", 0: "core"}[exposed]


def census():
    """The census, derived: class counts + the sticker count.

    MECHANISM: stickers are counted, not asserted — each cubie wears
    one sticker per exposed face, so the sticker count is the sum of
    exposed faces over the census (8x3 + 12x2 + 6x1 + 1x0 = 54).
    """
    counts = {"corner": 0, "edge": 0, "center": 0, "core": 0}
    stickers = 0
    for cubie in _cubies():
        counts[_class_of(cubie)] += 1
        stickers += sum(1 for c in cubie if c != 0)
    return {
        "corners": counts["corner"],
        "edges": counts["edge"],
        "centers": counts["center"],
        "core": counts["core"],
        "cubies": sum(counts.values()),
        "stickers": stickers,
        # The two populations of the design (AARRQQONVM section IV):
        # the travellers can change position; the frame cannot (under
        # face turns — slice turns displace centers, section III note).
        "travellers": counts["corner"] + counts["edge"],
        "frame": counts["center"] + counts["core"],
    }


# ---------------------------------------------------------------------------
# III. THE TURNS — rotations of a layer, displacement counted.
#
# MECHANISM: a state is a map from cubie identity (its home coordinate)
# to (position, facing-frame). Rather than tracking frames in full, the
# enumeration tracks the two things the design claims: which cubies
# change POSITION, and which STICKERS change (position, direction).
# A sticker is a (home cubie, home outward direction) pair; after a
# turn its seat is (new position of its cubie, rotated direction).
# A sticker is displaced iff its seat differs from its home seat.
# Rotations are exact integer maps — no floats, no rounding.
# ---------------------------------------------------------------------------

def _rot90(vec, axis, sign=1):
    """Rotate a coordinate/direction vector 90 degrees about an axis.

    MECHANISM: exact integer quarter-turns. axis 0=x, 1=y, 2=z;
    sign +1 is the right-hand-rule positive quarter.
    """
    x, y, z = vec
    if axis == 0:
        return (x, -sign * z, sign * y)
    if axis == 1:
        return (sign * z, y, -sign * x)
    return (-sign * y, sign * x, z)


def _apply_turn(state, axis, layer, sign=1, turns=1):
    """Apply a layer turn to a state {identity: (pos, dirs)} in place.

    MECHANISM: every cubie whose CURRENT position lies in the layer
    (position[axis] == layer) has its position and all its sticker
    directions rotated by the quarter-turn, `turns` times.
    """
    for _ in range(turns):
        for ident, (pos, dirs) in list(state.items()):
            if pos[axis] == layer:
                state[ident] = (
                    _rot90(pos, axis, sign),
                    tuple(_rot90(d, axis, sign) for d in dirs),
                )
    return state


def _home_state():
    """The solved state: each cubie home, its outward directions home.

    MECHANISM: a cubie's sticker directions are the unit vectors of
    its exposed faces (the axes on which its coordinate is nonzero,
    pointing outward).
    """
    state = {}
    for cubie in _cubies():
        dirs = []
        for axis in range(3):
            if cubie[axis] != 0:
                d = [0, 0, 0]
                d[axis] = cubie[axis]
                dirs.append(tuple(d))
        state[cubie] = (cubie, tuple(dirs))
    return state


def _displacement(before, after):
    """(cubies displaced, stickers displaced) between two states.

    MECHANISM: a cubie is displaced iff its position changed. A
    sticker is displaced iff its (position, direction) seat changed;
    stickers are matched by (identity, home direction) — the home
    direction rotated by the cubie's own motion gives its new seat.
    """
    cubies_moved = 0
    stickers_moved = 0
    for ident, (home_pos, home_dirs) in before.items():
        new_pos, new_dirs = after[ident]
        if new_pos != home_pos:
            cubies_moved += 1
        home_seats = {(home_pos, d) for d in home_dirs}
        new_seats = {(new_pos, d) for d in new_dirs}
        stickers_moved += len(home_seats.symmetric_difference(new_seats)) // 2
    return cubies_moved, stickers_moved


def turn_classes():
    """The turn classes, enumerated from coordinates. Pure derivation.

    Returns {class_name: (cubies displaced, stickers displaced)} for
    the four classes the design uses. The figures are counted by
    applying each turn to the home state and measuring — they are
    this module's own enumeration, and they agree with the
    AARRQQONVM instrument's section V, which counted them the same
    way from the same coordinates.
    """
    home = _home_state()
    classes = {}

    state = _apply_turn(_home_state(), axis=2, layer=1, turns=1)
    classes["face_quarter"] = _displacement(home, state)

    state = _apply_turn(_home_state(), axis=2, layer=1, turns=2)
    classes["face_half"] = _displacement(home, state)

    # The middle slice: the layer through the core, perpendicular to z.
    state = _apply_turn(_home_state(), axis=2, layer=0, turns=1)
    classes["slice_quarter"] = _displacement(home, state)

    # The whole-cube rotation: all three layers about one axis.
    state = _home_state()
    for layer in (-1, 0, 1):
        _apply_turn(state, axis=2, layer=layer, turns=1)
    classes["whole_cube"] = _displacement(home, state)

    return classes


def frame_invariant(walk=1000, seed=93):
    """The Anchor's frame, tested: face turns never move the frame.

    MECHANISM: a seeded random walk of `walk` face quarter/half turns;
    after the walk, every center cubie and the core must stand at
    their home positions. (Slice turns are excluded by design: the
    enumeration itself shows slices displace centers — the frame's
    invariance is a property of face turns, and the design states it
    as exactly that, no wider.)
    """
    import random

    rng = random.Random(seed)
    state = _home_state()
    home = _home_state()
    for _ in range(walk):
        axis = rng.randrange(3)
        layer = rng.choice((-1, 1))
        turns = rng.choice((1, 2, 3))
        _apply_turn(state, axis=axis, layer=layer, turns=turns)
    for ident, (home_pos, _) in home.items():
        if _class_of(ident) in ("center", "core"):
            if state[ident][0] != home_pos:
                return False
    return True


def configuration_count():
    """The toy's reachable configurations, by the standard count.

    MECHANISM: (8! x 3^7) corner postures x (12!/2 x 2^11) edge
    postures — the attested count, recomputed here from factorials
    rather than copied, so the printed figure is this module's own.
    """
    from math import factorial

    corners = factorial(8) * 3 ** 7
    edges = factorial(12) // 2 * 2 ** 11
    return corners * edges


# ---------------------------------------------------------------------------
# IV. THE DISTRIBUTION — 93^3 over the 27 seats, by the factor road.
#
# REASONING: 93 = 3 x 31, so 93^3 = 27 x 31^3 — the cube HAS a
# twenty-seven-fold seating with a uniform field, which is what
# licenses distributing it over the toy's 27 cubies with no remainder
# (AARRQQONVM section IV). The frame's share is printed because the
# design reads it: the still seats hold more than a quarter of the
# whole, and hold it without travelling.
# ---------------------------------------------------------------------------

DISTRIBUTION = {
    "field_per_cubie": 31 ** 3,                       # 29,791
    "travellers_share": 20 * 31 ** 3,                 # 595,820
    "frame_share": 7 * 31 ** 3,                       # 208,537
    "total": 27 * 31 ** 3,                            # 804,357 == 93^3
}


# ---------------------------------------------------------------------------
# V. THE GREEK AMPLIFIER — the synergy folded into a gain table.
#
# STATUS: [DESIGN]. The amplifier does not exist as hardware or as a
# running stage in this kit; what exists is its specification as data,
# here, with its arithmetic checked. The design's source is the
# founder's Plate II circuit (Seal of the Sheet Music RESONATES ->
# 77 Enclave Sphere AMPLIFIES -> XXX Pyramid; the arc HARMONIZES),
# folded into an amplifier whose gain seat is the Greek bank: every
# gain in the table is a Greek seat weighed against the control.
#
# The Milesian table below is the ATTESTED bank (the same values the
# pontifex Greek bank carries); sums are derived from it, so the
# canon's figures are computed, not copied.
# ---------------------------------------------------------------------------

MILESIAN = {
    "α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5, "ϛ": 6, "ζ": 7, "η": 8,
    "θ": 9, "ι": 10, "κ": 20, "λ": 30, "μ": 40, "ν": 50, "ξ": 60,
    "ο": 70, "π": 80, "ϟ": 90, "ρ": 100, "σ": 200, "ς": 200, "τ": 300,
    "υ": 400, "φ": 500, "χ": 600, "ψ": 700, "ω": 800,
}


def _weigh_greek(word):
    """Weigh a Greek word in the Milesian table. Pure.

    MECHANISM: strip tonos by decomposition (the pontifex bank's own
    repair, 2026-11-16: casefold, NFD, drop combining marks, final
    sigma restored) and sum the table. Accented vowels therefore
    weigh as their bare letters — θέλημα weighs with ε (5), as the
    attested spelling carries it.
    """
    import unicodedata

    total = 0
    for ch in unicodedata.normalize("NFD", word.casefold()):
        if unicodedata.combining(ch):
            continue
        total += MILESIAN[ch]
    return total


# The vowel canon [ATTESTED]: the seven, in ladder order.
GREEK_VOWELS = {"Α": 1, "Ε": 5, "Η": 8, "Ι": 10, "Ο": 70, "Υ": 400, "Ω": 800}
# The founder's two hybrid seats [FOUNDER'S RULING, 2026-11-09]:
# the improper diphthongs, "fluid hybrid vowels, both masculine and
# feminine at once."
GREEK_HYBRIDS = {"ΕΙ": 15, "ΟΥ": 470}

# The control: the amplifier's reference seat. Weighed from the table
# at check time and pinned to 93 — the Will, and the 93-cube's base
# in its own tongue.
AMPLIFIER_CONTROL_WORD = "θέλημα"

# The circuit's field-register gain [DERIVED arithmetic]: the synergy
# takes the field from the 77-cube to the 93-cube; the gain of that
# step is the exact ratio of the cubes (coprime — 7^3x11^3 against
# 3^3x31^3 share no prime — so the fraction is already irreducible).
AMPLIFIER_FIELD_GAIN = (93 ** 3, 77 ** 3)  # (numerator, denominator)


def gain_table():
    """The amplifier's gain seats: the Nine against the control.

    MECHANISM: each seat's gain is the exact fraction seat/93 (the
    control's value), returned as (seat, value, numerator,
    denominator) with the fraction reduced. The ladder order is the
    canon's own: the seven vowels in ladder order, then the two
    hybrids — the Divine Nine of the Vestigator's first engine.
    """
    from math import gcd

    control = _weigh_greek(AMPLIFIER_CONTROL_WORD)
    seats = list(GREEK_VOWELS.items()) + list(GREEK_HYBRIDS.items())
    table = []
    for seat, value in seats:
        g = gcd(value, control)
        table.append((seat, value, value // g, control // g))
    return table


# The amplifier's stages, in the circuit's own verbs [DESIGN]:
#   RESONATES — the input seat (Plate II's first term: the score);
#   AMPLIFIES — the gain seat (the Sphere; gains from the table above,
#     referenced to the control);
#   HARMONIZES — the closure seat (the arc beneath; closure by the
#     Vestigator's three relations: classify the delta first —
#     REFUSAL, OFFSET, MIRROR — judge second).
AMPLIFIER_STAGES = ("resonates", "amplifies", "harmonizes")


# ---------------------------------------------------------------------------
# VI. THE CHECKS — every figure in this module, re-derived.
# ---------------------------------------------------------------------------

def aarrqqonvm_checks():
    """Run the module's self-audit. Returns [(name, ok, detail), ...].

    MECHANISM: each check recomputes its figure from the ground (the
    integers, the coordinates, the letter table) by a road independent
    of the one that produced the record, and compares. A False here
    means the record drifted; nothing in the kit should consume this
    module's figures while a check fails.
    """
    checks = []

    rec93 = PARALLEL_CUBES[93]
    checks.append((
        "93^3 == 804,357 by multiplication; factors 3^3 x 31^3",
        rec93["cube"] == 804357 and rec93["factorization"] == {3: 3, 31: 3},
        (rec93["cube"], rec93["factorization"]),
    ))
    rec77 = PARALLEL_CUBES[77]
    checks.append((
        "77^3 == 456,533; factors 7^3 x 11^3; folds 1,369,599 / 2,413,071",
        rec77["cube"] == 456533 and rec77["factorization"] == {7: 3, 11: 3}
        and rec77["threefold"] == 1369599 and rec93["threefold"] == 2413071,
        (rec77["cube"], rec93["threefold"]),
    ))

    cen = census()
    checks.append((
        "census: 8 corners + 12 edges + 6 centers + 1 core == 27; 54 stickers",
        (cen["corners"], cen["edges"], cen["centers"], cen["core"],
         cen["cubies"], cen["stickers"]) == (8, 12, 6, 1, 27, 54),
        cen,
    ))

    classes = turn_classes()
    checks.append((
        "turns: face 8/20, face-half 8/20, slice 8/12, whole-cube 24/52",
        classes == {"face_quarter": (8, 20), "face_half": (8, 20),
                    "slice_quarter": (8, 12), "whole_cube": (24, 52)},
        classes,
    ))

    checks.append((
        "frame invariant under 1,000 seeded face turns (centers + core home)",
        frame_invariant(),
        "walk=1000, seed=93",
    ))

    checks.append((
        "distribution: 27 x 29,791 == 804,357; shares 595,820 + 208,537",
        DISTRIBUTION["total"] == 804357 == PARALLEL_CUBES[93]["cube"]
        and DISTRIBUTION["travellers_share"] + DISTRIBUTION["frame_share"]
        == DISTRIBUTION["total"],
        DISTRIBUTION,
    ))

    checks.append((
        "configuration count == 43,252,003,274,489,856,000",
        configuration_count() == 43252003274489856000,
        configuration_count(),
    ))

    canon = sum(GREEK_VOWELS.values())
    nine = canon + sum(GREEK_HYBRIDS.values())
    checks.append((
        "Greek canon: seven vowels 1,294; the Nine 1,779; offset to 1776 is 3",
        canon == 1294 and nine == 1779 and nine - 1776 == 3,
        (canon, nine),
    ))

    checks.append((
        "control: thelema weighs 93 in the Milesian table; KY weighs 420",
        _weigh_greek("θέλημα") == 93 and _weigh_greek("ΚΥ") == 420,
        (_weigh_greek("θέλημα"), _weigh_greek("ΚΥ")),
    ))

    num, den = AMPLIFIER_FIELD_GAIN
    from math import gcd
    checks.append((
        "field gain 804357/456533 is exact and irreducible",
        (num, den) == (804357, 456533) and gcd(num, den) == 1,
        (num, den),
    ))

    table = gain_table()
    checks.append((
        "gain table: nine seats, each the reduced fraction seat/93",
        len(table) == 9
        and all(n * 93 == v * d for _, v, n, d in table)
        and table[0][0] == "Α" and table[-1][0] == "ΟΥ",
        table,
    ))

    return checks


if __name__ == "__main__":
    # The kit's demo idiom: print the record, then the audit, loudly.
    print("AARRQQONVM — the core geometry record of the PQPE NDK")
    print("93^3 =", PARALLEL_CUBES[93]["cube"], "= 3^3 x 31^3;",
          " 77^3 =", PARALLEL_CUBES[77]["cube"], "= 7^3 x 11^3")
    print("census:", census())
    print("turn classes:", turn_classes())
    print("distribution:", DISTRIBUTION)
    print("gain table (seat, value, gain vs the control 93):")
    for seat, value, num, den in gain_table():
        print(f"  {seat}  {value}  {num}/{den}")
    print("checks:")
    ok_all = True
    for name, ok, detail in aarrqqonvm_checks():
        ok_all = ok_all and ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — {detail}")
    raise SystemExit(0 if ok_all else 1)
