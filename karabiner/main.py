import json
import os
from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel


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


def main(
    name="layer",
    path_out="~/.config/karabiner/assets/complex_modifications/layer.json",
):
    path_out = os.path.expanduser(path_out)
    Path(path_out).parent.mkdir(exist_ok=True, parents=True)
    cmd = "right_command"
    ctrl = "right_control"
    shift = "left_shift"
    option = "left_option"

    rules = [
        Manipulator(
            from_key=Event(key_code="spacebar", modifiers=Modifiers(optional=["any"])),
            to=Event(key_code=shift),
            to_if_alone=Event(key_code="spacebar"),
        ),
    ]

    maps = [
        EasyMap(a=cmd, b=ctrl),  # Affects downstream remaps
        # Arrow keys
        EasyMap(a="n", b="left_arrow", mod_a=[ctrl]),
        EasyMap(a="m", b="down_arrow", mod_a=[ctrl]),
        EasyMap(a="comma", b="up_arrow", mod_a=[ctrl]),
        EasyMap(a="period", b="right_arrow", mod_a=[ctrl]),
        # Vim
        EasyMap(a="h", b="tab", mod_a=[ctrl], mod_b=[shift, ctrl]),
        EasyMap(a="j", b="d", mod_a=[ctrl], mod_b=[ctrl]),
        EasyMap(a="k", b="u", mod_a=[ctrl], mod_b=[ctrl]),
        EasyMap(a="l", b="tab", mod_a=[ctrl], mod_b=[ctrl]),
        # Special Keys
        EasyMap(a="s", b="escape", mod_a=[ctrl], mod_b_optional=["any"]),
        EasyMap(a="d", b="return_or_enter", mod_a=[ctrl], mod_b_optional=["any"]),
        EasyMap(a="f", b="delete_or_backspace", mod_a=[ctrl], mod_b_optional=["any"]),
        EasyMap(a="g", b="tab", mod_a=[ctrl], mod_b_optional=["any"]),
        EasyMap(a="u", b="page_down", mod_a=[ctrl], mod_b=["any"]),
        EasyMap(a="i", b="page_up", mod_a=[ctrl], mod_b=["any"]),
    ]
    rules.extend([m.to_manipulator() for m in maps])

    for m in rules:
        assert m.is_valid
    config = Config(title=name, rules=[Rule(manipulators=rules, description=name)])
    with open(path_out, "w") as f:
        raw = config.dict(by_alias=True)
        raw = remove_none(raw)
        print(raw)
        f.write(json.dumps(raw, indent=2))


if __name__ == "__main__":
    test_manipulator()
    test_remove_none()
    main()
