from pathlib import Path
from dataclasses import dataclass
from typing import List
from copy import deepcopy
from math import prod

SOURCE = Path("input.txt")


@dataclass
class Rule:
    variable: int
    lower: bool
    value: int
    workflow: str


@dataclass
class Workflow:
    rules: List[Rule]
    default: str


@dataclass
class VariableRange:
    lower: int
    upper: int


@dataclass
class PartRange:
    workflow: str
    ranges: List[VariableRange]

    def is_valid(self):
        return all([rng.upper > rng.lower for rng in self.ranges])


variable_idx = {
    "x": 0,
    "m": 1,
    "a": 2,
    "s": 3
}


def read_data(lines):
    workflows = {}
    while lines[0] != "":
        line = lines.pop(0)
        name, commands = line[:-1].split("{")
        commands = commands.split(",")
        rules = []
        for command in commands[:-1]:
            condition, new_workflow = command.split(":")
            if ">" in condition:
                split_val = ">"
                lower = False
            else:
                split_val = "<"
                lower = True
            variable, value = condition.split(split_val)
            rules.append(Rule(variable_idx[variable], lower, int(value), new_workflow))
        workflows[name] = Workflow(rules, commands[-1])
    lines.pop(0)

    parts = []
    for line in lines:
        variables = line[1:-1].split(",")
        values = [0] * len(variable_idx)
        for variable in variables:
            name, value = variable.split("=")
            values[variable_idx[name]] = int(value)
        parts.append(values)

    return workflows, parts


def split_range(rng, rule):
    in_range, out_range = deepcopy(rng), deepcopy(rng)
    in_range.workflow = rule.workflow
    if rule.lower:
        in_range.ranges[rule.variable].upper = rule.value - 1
        out_range.ranges[rule.variable].lower = rule.value
    else:
        in_range.ranges[rule.variable].lower = rule.value + 1
        out_range.ranges[rule.variable].upper = rule.value
    return in_range, out_range


def get_accepted_ranges(workflows, ranges):
    accept_ranges, reject_ranges = [], []
    while ranges:
        rng = ranges.pop(0)

        if rng.workflow == "A":
            accept_ranges.append(rng)
            continue
        elif rng.workflow == "R":
            reject_ranges.append(rng)
            continue

        workflow = workflows[rng.workflow]
        for rule in workflow.rules:
            new_range, rng = split_range(rng, rule)
            if new_range.is_valid():
                ranges.append(new_range)
            if not rng.is_valid():
                break
        else:
            rng.workflow = workflow.default
            ranges.append(rng)
    return accept_ranges, reject_ranges


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()

    workflows, parts = read_data(lines)
    accept_ranges, reject_ranges = get_accepted_ranges(
        workflows, [PartRange("in", [
            VariableRange(1, 4000),
            VariableRange(1, 4000),
            VariableRange(1, 4000),
            VariableRange(1, 4000)
        ])]
    )
    print(accept_ranges)
    total_accept = sum([
        prod([var.upper - var.lower + 1 for var in var_range.ranges])
        for var_range in accept_ranges
    ])
    total_reject = sum([
        prod([var.upper - var.lower + 1 for var in var_range.ranges])
        for var_range in reject_ranges
    ])
    print(f"Accepted: {total_accept:20,}")
    print(f"Rejected: {total_reject:20,}")
    print(f"Total   : {total_accept+total_reject:20,}")


if __name__ == "__main__":
    main()
