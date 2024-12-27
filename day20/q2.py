from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum

SOURCE = Path("input.txt")


class Pulse(Enum):
    LOW = False
    HIGH = True

    def flipped(self):
        if self == Pulse.LOW:
            return Pulse.HIGH
        else:
            return Pulse.LOW


class Module(ABC):
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets

    @abstractmethod
    def process(self, pulse, source):
        pass


class Broadcast(Module):
    def process(self, pulse, source):
        return [(target, pulse, self.name) for target in self.targets]

    def __repr__(self):
        return f"Broadcast({self.targets})"


class Flipflop(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.status = Pulse.LOW

    def process(self, pulse, source):
        if pulse == Pulse.HIGH:
            return []
        self.status = self.status.flipped()
        return [(target, self.status, self.name) for target in self.targets]

    def __repr__(self):
        return f"Flipflop({self.status}, {self.targets})"


class Conjunction(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.last = {}
        self.key_order = None

    def process(self, pulse, source):
        self.last[source] = pulse
        # print(f"I am {self.name} and my state is: {self.last}")
        if all([val.value for val in self.last.values()]):
            new_pulse = Pulse.LOW
        else:
            new_pulse = Pulse.HIGH
        send = [(target, new_pulse, self.name) for target in self.targets]
        return send

    def init_source(self, source):
        self.last[source] = Pulse.LOW

    def __repr__(self):
        return f"Conjunction({self.last}, {self.targets})"

def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()

    modules = {}
    for line in lines:
        name, targets = line.split(" -> ")
        targets = targets.split(", ")
        if name == "broadcaster":
            modules[name] = Broadcast(name, targets)
        elif name[0] == "%":
            modules[name[1:]] = Flipflop(name[1:], targets)
        elif name[0] == "&":
            modules[name[1:]] = Conjunction(name[1:], targets)

    for module in modules.values():
        for target in module.targets:
            if target in modules and isinstance(modules[target], Conjunction):
                modules[target].init_source(module.name)

    iteration = 0
    delivered = False
    while not delivered:
        iteration += 1
        messages = [("broadcaster", Pulse.LOW, "button")]
        count_low, count_high = 1, 0
        while messages:
            target, pulse, source = messages.pop(0)
            if target not in modules:
                continue
            if pulse == Pulse.LOW and target == "rx":
                delivered = True
                break
            new_messages = modules[target].process(pulse, source)
            low = sum([pulse == Pulse.LOW for _, pulse, _ in new_messages])
            count_low += low
            count_high += len(new_messages) - low
            messages.extend(new_messages)
        iteration += 1

    print(iteration)


if __name__ == "__main__":
    main()
