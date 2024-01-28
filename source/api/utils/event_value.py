from typing import Generic, TypeVar, Callable

T = TypeVar('T')

class EventValue(Generic[T]):
    """
    A class to represent a value that can be subscribed to.

    This class is used to create values that can be subscribed to. When the value is changed, all subscribers are notified.

    Attributes:
        value (T): The value.
        events (list[Callable[[T], None]]): The list of events that are called when the value is changed.

    Methods:
        __init__(self, initial_value: T = None)
        subscribe(self, event: Callable[[T], None])
        unsubscribe(self, event: Callable[[T], None])
        set_value(self, new_value: T)
        get_value(self) -> T
        _notify_all(self)
    """

    def __init__(self, initial_value: T = None) -> None:
        """
        Initializes an EventValue with the given initial value.

        Arguments:
            initial_value (T): The initial value of the EventValue.
        """
        self.value: T = initial_value
        self.events: list[Callable[[T], None]] = []

    def subscribe(self, event: Callable[[T], None]) -> None:
        """
        Subscribes to the EventValue.

        Arguments:
            event (Callable): The function to call when the value is changed.

        Returns:
            None
        """
        self.events.append(event)

    def unsubscribe(self, event: Callable[[T], None]) -> None:
        """
        Unsubscribes from the EventValue.

        Arguments:
            event (Callable): The function to unsubscribe.

        Returns:
            None
        """
        self.events.remove(event)

    def set_value(self, new_value: T) -> None:
        """
        Sets the value of the EventValue.

        Arguments:
            new_value (T): The new value of the EventValue.

        Returns:
            None
        """

        if self.value == new_value:
            return
        self.value = new_value
        self._notify_all()

    def get_value(self) -> T:
        """
        Returns the value of the EventValue.

        Returns:
            T: The value of the EventValue.
        """
        return self.value

    def _notify_all(self) -> None:
        """
        Notifies all subscribers of the EventValue.

        Returns:
            None
        """
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