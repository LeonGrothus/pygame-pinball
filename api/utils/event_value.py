from typing import Generic, TypeVar, Callable

T = TypeVar('T')

class EventValue(Generic[T]):
    def __init__(self, initial_value: T = None):
        self.value: T = initial_value
        self.events: list[Callable[[T], None]] = []

    def subscribe(self, event: Callable[[T], None]):
        self.events.append(event)

    def unsubscribe(self, event: Callable[[T], None]):
        self.events.remove(event)

    def set_value(self, new_value: T):
        if self.value == new_value:
            return
        self.value = new_value
        self.notify_all()

    def get_value(self) -> T:
        return self.value

    def notify_all(self):
        for event in self.events:
            event(self.value)

    # # Operator overloading for convenience #

    # def __add__(self, other):
    #     if isinstance(other, EventValue):
    #         return self.value + other.value
    #     else:
    #         return self.value + other

    # def __sub__(self, other):
    #     if isinstance(other, EventValue):
    #         return self.value - other.value
    #     else:
    #         return self.value - other

    # def __lt__(self, other):
    #     if isinstance(other, EventValue):
    #         return self.value < other.value
    #     else:
    #         return self.value < other

    # def __mul__(self, other):
    #     if isinstance(other, EventValue):
    #         return self.value * other.value
    #     else:
    #         return self.value * other

    # def __truediv__(self, other):
    #     if isinstance(other, EventValue):
    #         return self.value / other.value
    #     else:
    #         return self.value / other

    # def __gt__(self, other):
    #     if isinstance(other, EventValue):
    #         return self.value > other.value
    #     else:
    #         return self.value > other

    # def __le__(self, other):
    #     if isinstance(other, EventValue):
    #         return self.value <= other.value
    #     else:
    #         return self.value <= other