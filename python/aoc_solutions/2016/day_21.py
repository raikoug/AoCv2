from __future__ import annotations

from pathlib import Path
import sys
from typing import List

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def rotate(in_data: List[str], times: int, direction: str) -> List[str]:
    """Rotate a list of characters left or right."""
    data = list(in_data)
    if not data:
        return data

    times = times % len(data)
    if direction == "r":
        for _ in range(times):
            data = [data.pop(-1)] + data
    elif direction == "l":
        for _ in range(times):
            data = data + [data.pop(0)]
    return data


def solve_1(test_string: str | None = None) -> str:
    raw = GI.input if test_string is None else test_string

    # test is abcde, prod is abcdefgh
    password: List[str] = list("abcdefgh")
    passlen = len(password)

    for line in raw.splitlines():
        if not line:
            continue

        if line.startswith("swap position"):
            # swap position X with position Y
            _, _, X, _, _, Y = line.split(" ")
            X_i, Y_i = int(X), int(Y)
            password[X_i], password[Y_i] = password[Y_i], password[X_i]

        elif line.startswith("swap letter"):
            # swap letter X with letter Y
            _, _, X, _, _, Y = line.split(" ")
            for i in range(passlen):
                if password[i] == X:
                    password[i] = Y
                elif password[i] == Y:
                    password[i] = X

        elif line.startswith("rotate based"):
            # rotate based on position of letter e
            _, _, _, _, _, _, letter = line.split(" ")
            rotation = password.index(letter)
            if rotation >= 4:
                rotation += 2
            else:
                rotation += 1
            password = rotate(password, rotation, "r")

        elif line.startswith("rotate"):
            # rotate right 3 steps / left 3 steps
            _, direction, times, _ = line.split(" ")
            direction_short = direction[0]  # "r" or "l"
            rotation = int(times)
            password = rotate(password, rotation, direction_short)

        elif line.startswith("reverse positions"):
            # reverse positions X through Y (inclusive)
            _, _, X, _, Y = line.split(" ")
            X_i, Y_i = int(X), int(Y) + 1
            password = password[:X_i] + password[X_i:Y_i][::-1] + password[Y_i:]

        elif line.startswith("move position"):
            # move position X to position Y
            _, _, X, _, _, Y = line.split(" ")
            X_i, Y_i = int(X), int(Y)
            letter = password.pop(X_i)
            password.insert(Y_i, letter)

    return "".join(password)


def solve_2(test_string: str | None = None) -> str:
    raw = GI.input if test_string is None else test_string

    # test is abcde, prod is fbgdceah (final scrambled password)
    password: List[str] = list("fbgdceah")
    passlen = len(password)

    for line in reversed(raw.splitlines()):
        if not line:
            continue

        if line.startswith("swap position"):
            # swap position X with position Y  (inverse is itself)
            _, _, X, _, _, Y = line.split(" ")
            X_i, Y_i = int(X), int(Y)
            password[X_i], password[Y_i] = password[Y_i], password[X_i]

        elif line.startswith("swap letter"):
            # swap letter X with letter Y (inverse is itself)
            _, _, X, _, _, Y = line.split(" ")
            for i in range(passlen):
                if password[i] == X:
                    password[i] = Y
                elif password[i] == Y:
                    password[i] = X

        elif line.startswith("rotate based"):
            # invert "rotate based on position of letter X"
            _, _, _, _, _, _, letter = line.split(" ")

            # brute-force: try all left-rotations until re-applying the
            # forward rule would get back the current password
            candidate = list(password)
            while True:
                candidate = rotate(candidate, 1, "l")
                rotation = candidate.index(letter)
                if rotation >= 4:
                    rotation += 2
                else:
                    rotation += 1

                if rotate(candidate, rotation, "r") == password:
                    break
            password = list(candidate)

        elif line.startswith("rotate"):
            # inverse of "rotate left/right N steps" is rotate opposite dir
            _, direction, times, _ = line.split(" ")
            direction_short = direction[0]
            inverse_dir = "r" if direction_short == "l" else "l"
            rotation = int(times)
            password = rotate(password, rotation, inverse_dir)

        elif line.startswith("reverse positions"):
            # reverse positions X through Y  (inverse is itself)
            _, _, X, _, Y = line.split(" ")
            X_i, Y_i = int(X), int(Y) + 1
            password = password[:X_i] + password[X_i:Y_i][::-1] + password[Y_i:]

        elif line.startswith("move position"):
            # inverse: "move position Y to position X"
            _, _, X, _, _, Y = line.split(" ")
            Y_i, X_i = int(X), int(Y)
            letter = password.pop(X_i)
            password.insert(Y_i, letter)

    return "".join(password)


if __name__ == "__main__":
    test = """swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
