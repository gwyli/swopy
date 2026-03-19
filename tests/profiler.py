# ruff: noqa: T201
"""Profiler for swopy numeral system conversions.

Each system is profiled independently using Arabic as the source, across a
spread of integer values valid for that system. This avoids the measurement
noise of chaining systems together.

Usage:
    python tests/profiler.py
    python tests/profiler.py --system roman.Standard
    python tests/profiler.py --iterations 2000 --top 30
"""

import argparse
import contextlib
import cProfile
import math
import pstats
import time
from typing import Any

import swopy
from swopy.system import System

_SAMPLE_SIZE = 20
_LARGE_CAP = 10_000


def _sample_values(
    system: type[System[Any, Any]], size: int = _SAMPLE_SIZE
) -> list[int]:
    """Return up to ``size`` evenly-spaced integer values valid for ``system``.

    Values are always positive integers so they are valid Arabic inputs. For
    systems with an unbounded maximum the range is capped at ``_LARGE_CAP``.
    """
    minimum = system.minimum
    maximum = system.maximum

    lo = max(1, math.ceil(float(minimum)) if math.isfinite(float(minimum)) else 1)
    hi = min(_LARGE_CAP, int(maximum)) if math.isfinite(float(maximum)) else _LARGE_CAP
    hi = max(hi, lo)

    count = min(size, hi - lo + 1)
    if count <= 1:
        return [lo]
    step = max(1, (hi - lo) // (count - 1))
    return list(range(lo, hi + 1, step))[:size]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile swopy conversions (Arabic -> system).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--system",
        metavar="NAME",
        help="Profile only this system (e.g. roman.Standard).",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1000,
        metavar="N",
        help="swop() calls per value per system.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=30,
        metavar="N",
        help="Number of functions to show in cProfile output.",
    )
    return parser.parse_args()


def _run_timing(
    systems: dict[str, type[System[Any, Any]]],
    arabic: type[System[Any, Any]],
    iterations: int,
) -> list[tuple[str, float, int]]:
    """Return per-system ``(name, elapsed_s, total_calls)``, slowest first."""
    results: list[tuple[str, float, int]] = []
    for name, system in systems.items():
        values = _sample_values(system)

        # Warm up to avoid cold-cache bias
        for v in values[:3]:
            with contextlib.suppress(Exception):
                swopy.swop(v, arabic, system)

        start = time.perf_counter()
        for _ in range(iterations):
            for v in values:
                with contextlib.suppress(Exception):
                    swopy.swop(v, arabic, system)
        elapsed = time.perf_counter() - start

        results.append((name, elapsed, iterations * len(values)))

    return sorted(results, key=lambda r: r[1], reverse=True)


def main() -> None:
    args = _parse_args()
    all_systems = swopy.get_all_systems()
    arabic = swopy.systems.hindu_arabic.Arabic

    if args.system:
        if args.system not in all_systems:
            available = "\n  ".join(sorted(all_systems))
            print(f"Unknown system '{args.system}'. Available:\n  {available}")
            return
        systems: dict[str, type[System[Any, Any]]] = {
            args.system: all_systems[args.system]
        }
    else:
        systems = all_systems

    print(
        f"Profiling {len(systems)} system(s), "
        f"{args.iterations} iterations x {_SAMPLE_SIZE} values each\n"
    )

    # Per-system wall-clock timing table
    timing = _run_timing(systems, arabic, args.iterations)
    col = 36
    header = f"{'System':<{col}} {'Total (s)':>10} {'Calls':>10} {'us/call':>10}"
    rule = "-" * len(header)
    print(header)
    print(rule)
    for name, elapsed, calls in timing:
        us = elapsed / calls * 1_000_000
        print(f"{name:<{col}} {elapsed:>10.3f} {calls:>10,} {us:>10.2f}")
    print(rule)
    total_s = sum(e for _, e, _ in timing)
    total_c = sum(c for _, _, c in timing)
    print(f"{'Total':<{col}} {total_s:>10.3f} {total_c:>10,}\n")

    # cProfile for function-level detail
    print(f"cProfile top {args.top} functions by tottime:")
    print(rule)

    def _workload() -> None:
        for _, system in systems.items():
            values = _sample_values(system)
            for _ in range(args.iterations):
                for v in values:
                    swopy.swop(v, arabic, system)

    with cProfile.Profile() as pr:
        _workload()

    pstats.Stats(pr).sort_stats("tottime").print_stats(args.top)


if __name__ == "__main__":
    main()
