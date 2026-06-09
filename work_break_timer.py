#!/usr/bin/env python3
"""
Terminal work/break timer.

Default rhythm:
  - 50 minutes of focused work
  - 10 minutes of break
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Phase:
    kind: str
    minutes: float
    cycle: int

    @property
    def seconds(self) -> int:
        return max(1, round(self.minutes * 60))

    @property
    def title(self) -> str:
        if self.kind == "work":
            return f"Cycle {self.cycle}: work"
        return f"Cycle {self.cycle}: break"


def positive_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not a number") from exc

    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")

    return parsed


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer") from exc

    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")

    return parsed


def format_duration(seconds: int) -> str:
    seconds = max(0, seconds)
    minutes, remaining_seconds = divmod(seconds, 60)
    hours, remaining_minutes = divmod(minutes, 60)

    if hours:
        return f"{hours}:{remaining_minutes:02d}:{remaining_seconds:02d}"

    return f"{remaining_minutes:02d}:{remaining_seconds:02d}"


def build_schedule(work_minutes: float, break_minutes: float, cycles: int) -> list[Phase]:
    phases: list[Phase] = []

    for cycle in range(1, cycles + 1):
        phases.append(Phase(kind="work", minutes=work_minutes, cycle=cycle))
        phases.append(Phase(kind="break", minutes=break_minutes, cycle=cycle))

    return phases


def iter_schedule(work_minutes: float, break_minutes: float, cycles: int | None) -> Iterable[Phase]:
    if cycles is not None:
        yield from build_schedule(work_minutes, break_minutes, cycles)
        return

    cycle = 1
    while True:
        yield Phase(kind="work", minutes=work_minutes, cycle=cycle)
        yield Phase(kind="break", minutes=break_minutes, cycle=cycle)
        cycle += 1


def notify(title: str, message: str) -> None:
    notify_send = shutil.which("notify-send")
    if not notify_send:
        return

    subprocess.run(
        [notify_send, title, message],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def print_schedule(phases: Iterable[Phase]) -> None:
    for phase in phases:
        print(f"{phase.title}: {phase.minutes:g} minutes")


def run_phase(phase: Phase, *, bell: bool, desktop_notify: bool) -> None:
    if desktop_notify:
        notify(phase.title, f"Started: {phase.minutes:g} minutes")

    print(f"\n{phase.title} started ({phase.minutes:g} minutes).")
    end_time = time.monotonic() + phase.seconds

    while True:
        remaining = round(end_time - time.monotonic())
        if remaining <= 0:
            break

        print(f"\r{phase.title}: {format_duration(remaining)} remaining", end="", flush=True)
        time.sleep(min(1, remaining))

    print(f"\r{phase.title}: done.{' ' * 20}")

    if bell:
        print("\a", end="", flush=True)

    if desktop_notify:
        notify(phase.title, "Done")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a terminal timer for alternating work and break blocks.",
    )
    parser.add_argument("--work", type=positive_float, default=50.0, metavar="MINUTES")
    parser.add_argument("--break", dest="break_minutes", type=positive_float, default=10.0, metavar="MINUTES")
    parser.add_argument("--cycles", type=positive_int, default=1, help="number of work/break cycles")
    parser.add_argument("--repeat", action="store_true", help="repeat cycles until Ctrl+C")
    parser.add_argument("--no-bell", action="store_true", help="do not play the terminal bell")
    parser.add_argument("--notify", action="store_true", help="send desktop notifications via notify-send if available")
    parser.add_argument("--dry-run", action="store_true", help="print the schedule and exit")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    cycles = None if args.repeat else args.cycles
    phases = iter_schedule(args.work, args.break_minutes, cycles)

    if args.dry_run:
        if args.repeat:
            print("Repeat mode: work/break cycles will continue until Ctrl+C.")
            print_schedule(build_schedule(args.work, args.break_minutes, 1))
        else:
            print_schedule(phases)
        return 0

    try:
        for phase in phases:
            run_phase(phase, bell=not args.no_bell, desktop_notify=args.notify)
    except KeyboardInterrupt:
        print("\nTimer stopped.")
        return 130

    print("\nAll cycles completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
