import json
import os
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd
from fire import Fire
from pydantic import BaseModel


class Key(str, Enum):
    # Row 0
    escape: str = "escape"
    bright_down: str = "f14"
    bright_up: str = "f15"
    mute: str = "mute"
    vol_down: str = "volume_decrement"
    vol_up: str = "volume_increment"
    # Row 1
    tilde: str = "grave_accent_and_tilde"
    one: str = "1"
    two: str = "2"
    three: str = "3"
    four: str = "4"
    five: str = "5"
    six: str = "6"
    seven: str = "7"
    eight: str = "8"
    nine: str = "9"
    zero: str = "0"
    hyphen: str = "hyphen"
    equal: str = "equal_sign"
    delete: str = "delete_or_backspace"
    # Row 2
    tab: str = "tab"
    q: str = "q"
    w: str = "w"
    e: str = "e"
    r: str = "r"
    t: str = "t"
    y: str = "y"
    u: str = "u"
    i: str = "i"
    o: str = "o"
    p: str = "p"
    bracket_open: str = "open_bracket"
    bracket_close: str = "close_bracket"
    backslash: str = "backslash"
    # Row 3
    caps: str = "caps_lock"
    a: str = "a"
    s: str = "s"
    d: str = "d"
    f: str = "f"
    g: str = "g"
    h: str = "h"
    j: str = "j"
    k: str = "k"
    l: str = "l"
    semicolon: str = "semicolon"
    quote: str = "quote"
    enter: str = "return_or_enter"
    # Row 4
    shift: str = "left_shift"
    z: str = "z"
    x: str = "x"
    c: str = "c"
    v: str = "v"
    b: str = "b"
    n: str = "n"
    m: str = "m"
    comma: str = "comma"
    period: str = "period"
    slash: str = "slash"
    shift_right: str = "right_shift"
    # Row 5
    fn: str = "fn"
    ctrl: str = "left_control"
    opt: str = "left_option"
    cmd: str = "left_command"
    space: str = "spacebar"
    cmd_right: str = "right_command"
    opt_right: str = "right_option"
    # Arrows
    left: str = "left_arrow"
    right: str = "right_arrow"
    up: str = "up_arrow"
    down: str = "down_arrow"
    page_up: str = "page_up"
    page_down: str = "page_down"
    home: str = "home"
    end: str = "end"

    @classmethod
    def as_dict(cls):
        member: Key
        return {name: member for name, member in cls.__members__.items()}


class Modifiers(BaseModel):
    mandatory: Optional[List[str]]
    optional: Optional[List[str]]


class Variable(BaseModel):
    name: str
    value: int


class Condition(Variable):
    type: str


class Event(BaseModel):
    key_code: Optional[str]
    modifiers: Optional[Union[Modifiers, List[str]]]
    simultaneous: Optional[List]
    set_variable: Optional[Variable]

    @property
    def is_valid(self) -> bool:
        return any([v is not None for v in self.dict().values()])


class Manipulator(BaseModel):
    type: str = "basic"
    from_key: Event
    to: Optional[Event]
    to_if_alone: Optional[Event]
    to_after_key_up: Optional[Event]
    conditions: Optional[List[Condition]]

    class Config:
        fields = dict(from_key="from")
        allow_population_by_field_name = True

    @property
    def is_valid(self):
        return any([v is not None for v in [self.to, self.to_if_alone]])


class Rule(BaseModel):
    description = ""
    manipulators: List[Manipulator]


class Config(BaseModel):
    title: str
    rules: List[Rule]


def test_manipulator():
    m = Manipulator(from_key=Event(key_code="1"), to=Event())
    print(m.json(indent=2, exclude_none=True, by_alias=True))


def remove_none(old: dict):
    if not isinstance(old, dict):
        return old

    new = {}
    for k, v in old.items():
        if isinstance(v, dict):
            new[k] = remove_none(v)
        elif isinstance(v, list):
            new[k] = [remove_none(x) for x in v]
        elif v is not None:
            new[k] = v
    return new


def test_remove_none():
    d = dict(one=None, two=1, three=dict(four=None, five=5))
    print(d)
    print(remove_none(d))


class EasyMap(BaseModel):
    a: str
    b: str
    mod_a: Optional[List[str]]
    mod_b: Optional[List[str]]
    mod_b_optional: Optional[List[str]]

    def to_manipulator(self) -> Manipulator:
        return Manipulator(
            from_key=Event(
                key_code=self.a,
                modifiers=(
                    None
                    if self.mod_a is None
                    else Modifiers(mandatory=self.mod_a, optional=self.mod_b_optional)
                    # else Modifiers(mandatory=self.mod_a, optional=["any"])
                ),
            ),
            to=Event(key_code=self.b, modifiers=self.mod_b),
        )


def write_maps(name: str, maps: List[EasyMap], path_out: Path):
    path_out = os.path.expanduser(path_out)
    Path(path_out).parent.mkdir(exist_ok=True, parents=True)
    rules = [m.to_manipulator() for m in maps]
    for m in rules:
        assert m.is_valid
    config = Config(title=name, rules=[Rule(manipulators=rules, description=name)])

    with open(path_out, "w") as f:
        raw = config.dict(by_alias=True)
        raw = remove_none(raw)
        print(raw)
        f.write(json.dumps(raw, indent=2))


class RawMap(BaseModel):
    a: str
    b: str
    mod_a: str
    mod_b: str

    @classmethod
    def parse_key(cls, text: str) -> Key:
        return Key.as_dict()[text]

    @classmethod
    def parse_modifiers(cls, text: str) -> Optional[List[str]]:
        if len(text) > 0:
            mods = eval(text)
            return [cls.parse_key(text) for text in mods]

    def to_easy_map(self) -> EasyMap:
        return EasyMap(
            a=self.parse_key(self.a),
            b=self.parse_key(self.b),
            mod_a=self.parse_modifiers(self.mod_a),
            mod_b=self.parse_modifiers(self.mod_b),
        )


def main(
    path_in: str = "remap_0.csv",
    name: str = "remap_0",
    path_out: str = "~/.config/karabiner/assets/complex_modifications/layer.json",
):
    df = pd.read_csv(path_in)
    df = df.fillna(value="")
    maps = [RawMap(**r).to_easy_map() for r in df.to_dict(orient="records")]
    write_maps(name, maps, Path(path_out))


if __name__ == "__main__":
    test_manipulator()
    test_remove_none()
    Fire(main)
