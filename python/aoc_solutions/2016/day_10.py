from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Union

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()
CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))


class Output:
    def __init__(self, number: int) -> None:
        self.number = number
        self.values: List[int] = []

    def __str__(self) -> str:
        return f"Output: {self.number}, Current values: {self.values}"

    __repr__ = __str__

    def __format__(self, _: str) -> str:
        return self.__str__()


class Bot:
    def __init__(self, number: int) -> None:
        self.number = number
        self.lower: Union["Bot", Output, None] = None
        self.higher: Union["Bot", Output, None] = None
        self.stack: List[int] = []

    def __str__(self) -> str:
        lower = f", Lower: {self.lower.number}" if isinstance(self.lower, Bot) else ""
        higher = f", Higher: {self.higher.number}" if isinstance(self.higher, Bot) else ""
        return f"Bot: {self.number}, Current stack: {self.stack}{lower}{higher}"

    __repr__ = __str__

    def __format__(self, _: str) -> str:
        return self.__str__()


def _parse_input(raw: str) -> tuple[Dict[int, Bot], Dict[int, Output]]:
    bots: Dict[int, Bot] = {}
    outputs: Dict[int, Output] = {}

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("bot"):
            # bot 2 gives low to bot 1 and high to output 0
            _, bot_n, _, _, _, low_dest, bot_low_n, _, _, _, high_dest, bot_high_n = line.split(" ")
            bot_n_i = int(bot_n)
            bot_low_i = int(bot_low_n)
            bot_high_i = int(bot_high_n)

            if bot_n_i not in bots:
                bots[bot_n_i] = Bot(bot_n_i)

            # low
            if low_dest == "bot":
                if bot_low_i not in bots:
                    bots[bot_low_i] = Bot(bot_low_i)
                bots[bot_n_i].lower = bots[bot_low_i]
            elif low_dest == "output":
                if bot_low_i not in outputs:
                    outputs[bot_low_i] = Output(bot_low_i)
                bots[bot_n_i].lower = outputs[bot_low_i]

            # high
            if high_dest == "bot":
                if bot_high_i not in bots:
                    bots[bot_high_i] = Bot(bot_high_i)
                bots[bot_n_i].higher = bots[bot_high_i]
            elif high_dest == "output":
                if bot_high_i not in outputs:
                    outputs[bot_high_i] = Output(bot_high_i)
                bots[bot_n_i].higher = outputs[bot_high_i]

        elif line.startswith("value"):
            # value 5 goes to bot 2
            _, value, _, _, _, bot_n = line.split(" ")
            v = int(value)
            bot_n_i = int(bot_n)
            if bot_n_i not in bots:
                bots[bot_n_i] = Bot(bot_n_i)
            bots[bot_n_i].stack.append(v)
            bots[bot_n_i].stack.sort()

    return bots, outputs


def solve_1(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    bots, outputs = _parse_input(inputs_1)

    target = [17, 61]  # in ordine!

    while True:
        for n, bot in bots.items():
            if len(bot.stack) == 2:
                if bot.stack == target:
                    return n

                low_val = bot.stack.pop(0)
                high_val = bot.stack.pop(0)

                if isinstance(bot.lower, Bot):
                    bot.lower.stack.append(low_val)
                    bot.lower.stack.sort()
                elif isinstance(bot.lower, Output):
                    bot.lower.values.append(low_val)

                if isinstance(bot.higher, Bot):
                    bot.higher.stack.append(high_val)
                    bot.higher.stack.sort()
                elif isinstance(bot.higher, Output):
                    bot.higher.values.append(high_val)


def solve_2(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    bots, outputs = _parse_input(inputs_1)

    while True:
        for _, bot in bots.items():
            if len(bot.stack) == 2:
                low_val = bot.stack.pop(0)
                high_val = bot.stack.pop(0)

                if isinstance(bot.lower, Bot):
                    bot.lower.stack.append(low_val)
                    bot.lower.stack.sort()
                elif isinstance(bot.lower, Output):
                    bot.lower.values.append(low_val)

                if isinstance(bot.higher, Bot):
                    bot.higher.stack.append(high_val)
                    bot.higher.stack.sort()
                elif isinstance(bot.higher, Output):
                    bot.higher.values.append(high_val)

        if (
            0 in outputs
            and 1 in outputs
            and 2 in outputs
            and len(outputs[0].values) >= 1
            and len(outputs[1].values) >= 1
            and len(outputs[2].values) >= 1
        ):
            return outputs[0].values[0] * outputs[1].values[0] * outputs[2].values[0]


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
