from pathlib import Path
from dataclasses import dataclass
from typing import List

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


def check_acceptance(workflows, part):
    current_workflow = "in"
    while current_workflow not in ["A", "R"]:
        for rule in workflows[current_workflow].rules:
            if rule.lower and part[rule.variable] < rule.value:
                current_workflow = rule.workflow
                break
            elif not rule.lower and part[rule.variable] > rule.value:
                current_workflow = rule.workflow
                break
        else:
            current_workflow = workflows[current_workflow].default
    return current_workflow


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()

    workflows, parts = read_data(lines)
    total = 0
    for part in parts:
        if check_acceptance(workflows, part) == "A":
            total += sum(part)
    print(total)


if __name__ == "__main__":
    main()
