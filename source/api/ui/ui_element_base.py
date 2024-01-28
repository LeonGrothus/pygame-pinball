from abc import ABC, abstractmethod

from pygame import Surface


class UIElementBase(ABC):
    """
    A class to represent a UI element. A UI element is an element in the UI. A UI element can be updated and drawn.
    This is the base class for all UI elements.

    Attributes:
        screen (Surface): The screen where the UI element will be displayed.
        _rel_pos (tuple): The position of the UI element relative to the size of the screen.
        _rel_pos_self (tuple): The position of the UI element relative to its own size.
        _width (int): The width of the UI element.
        _height (int): The height of the UI element.
        _x (int): The x-coordinate of the UI element.
        _y (int): The y-coordinate of the UI element.

    Methods:
        __init__(self, screen: Surface, rel_pos: tuple[float, float], width: int, height: int, rel_pos_self: tuple[float, float] = (0, 0))
        update_events(self, pygame_events)
        draw(self)
        contains(self, x: int, y: int)
        move_to_rel(self, rel_x: float, rel_y: float)
        get_rel_pos(self)
        get_rel_pos_self(self)
        get_y(self)
        get_width(self)
        get_height(self)
    """

    def __init__(self, screen: Surface, rel_pos: tuple[float, float], width: int, height: int, rel_pos_self: tuple[float, float] = (0, 0)) -> None:
        """
        Initializes a new instance of the UIElementBase class.

        This method sets the screen where the UI element will be displayed and its relative position and size.

        Arguments:
            screen (Surface): The screen where the UI element will be displayed.
            rel_pos (tuple): The position of the UI element relative to the size of the screen.
            width (int): The width of the UI element.
            height (int): The height of the UI element.
            rel_pos_self (tuple): The position of the UI element relative to its own size.
        """
        self.screen: Surface = screen
        self._rel_pos: tuple[float, float] = rel_pos
        self._rel_pos_self: tuple[float, float] = rel_pos_self
        self._width: int = width
        self._height: int = height
        self._x = int(self.screen.get_width() * self._rel_pos[0]) - int(self._width * self._rel_pos_self[0])
        self._y = int(self.screen.get_height() * self._rel_pos[1]) - int(self._height * self._rel_pos_self[1])

    @abstractmethod
    def update_events(self, pygame_events) -> None:
        """
        Updates the UI element.

        This method must be overridden in derived classes.

        Arguments:
            pygame_events (list): A list of pygame events occurred in the last frame.
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """
        Draws the UI element.

        This method must be overridden in derived classes.

        Arguments:
            None

        Returns:
            None
        """
        pass

    def contains(self, x: int, y: int) -> bool:
        """
        Checks if the UI element contains the given point.

        Parameters:
            x (int): The x-coordinate of the point.
            y (int): The y-coordinate of the point.

        Returns:
            True if the UI element contains the given point, False otherwise.
        """
        return self._x <= x <= self._x + self._width and self._y <= y <= self._y + self._height

    def move_to_rel(self, rel_x: float, rel_y: float) -> None:
        """
        Moves the UI element to the given relative position.

        Arguments:
            rel_x (float): The x-coordinate of the new position relative to the size of the screen.
            rel_y (float): The y-coordinate of the new position relative to the size of the screen.
        """
        self._rel_x = rel_x
        self._rel_y = rel_y
        self._x = int(self.screen.get_width() * self._rel_x)
        self._y = int(self.screen.get_height() * self._rel_y)

    ### Getters ###

    def get_rel_pos(self) -> tuple:
        """
        Gets the position of the UI element relative to the size of the screen.

        Returns:
            The position of the UI element relative to the size of the screen.
        """
        return self._rel_pos
    
    def get_rel_pos_self(self) -> tuple:
        """
        Gets the position of the UI element relative to its own size.

        Returns:
            The position of the UI element relative to its own size.
        """
        return self._rel_pos_self

    def get_y(self) -> int:
        """
        Gets the y-coordinate of the UI element.

        Returns:
            The y-coordinate of the UI element.
        """
        return self._y

    def get_width(self) -> int:
        """
        Gets the width of the UI element.

        Returns:
            The width of the UI element.
        """
        return self._width

    def get_height(self) -> int:
        """
        Gets the height of the UI element.

        Returns:
            The height of the UI element.
        """
        return self._height
