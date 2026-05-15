from dataclasses import dataclass

from model.order import Order


@dataclass
class Edge:
    order1: Order
    order2: Order
    peso: float

    def __hash__(self):
        return hash((self.order1, self.order2))

    def __eq__(self, other):
        return self.order1 == other.order1 and self.order2 == other.order2