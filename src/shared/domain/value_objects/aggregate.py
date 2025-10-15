from abc import abstractmethod

from sindripy.value_objects import Aggregate as AggregateRoot


class Aggregate(AggregateRoot):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
