from abc import ABC, abstractmethod

from pygame import Surface


class UIElementBase(ABC):
    def __init__(self, screen: Surface, rel_x: float, rel_y: float, width: int, height: int):
        """
        Initializes a new instance of the UIElementBase class.

        This method sets the screen where the UI element will be displayed and its relative position and size.

        Parameters:
            screen (Surface): The screen where the UI element will be displayed.
            rel_x (int): The x-coordinate of the UI element relative to the size of the screen.
            rel_y (int): The y-coordinate of the UI element relative to the size of the screen.
            width (int): The width of the UI element.
            height (int): The height of the UI element.
        """
        self.screen: Surface = screen
        self._rel_x: float = rel_x
        self._x = int(self.screen.get_width() * self._rel_x)
        self._rel_y: float = rel_y
        self._y = int(self.screen.get_height() * self._rel_y)
        self._width: int = width
        self._height: int = height

    @abstractmethod
    def update_events(self, pygame_events) -> None:
        """
        Updates the UI element.

        This method must be overridden in derived classes.
        
        Parameters:
            pygame_events (list): A list of pygame events occurred in the last frame.
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """
        Draws the UI element.

        This method must be overridden in derived classes.
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

        Parameters:
            rel_x (float): The x-coordinate of the new position relative to the size of the screen.
            rel_y (float): The y-coordinate of the new position relative to the size of the screen.
        """
        self._rel_x = rel_x
        self._rel_y = rel_y
        self._x = int(self.screen.get_width() * self._rel_x)
        self._y = int(self.screen.get_height() * self._rel_y)


    """ 
    getters
    """

    def get_rel_x(self) -> float:
        """
        Gets the x-coordinate of the UI element relative to the size of the screen.

        Returns:
            The x-coordinate of the UI element relative to the size of the screen.
        """
        return self._rel_x
    
    def get_rel_y(self) -> float:
        """
        Gets the y-coordinate of the UI element relative to the size of the screen.

        Returns:
            The y-coordinate of the UI element relative to the size of the screen.
        """
        return self._rel_y
    
    def get_x(self) -> int:
        """
        Gets the x-coordinate of the UI element.

        Returns:
            The x-coordinate of the UI element.
        """
        return self._x
    
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