""" GridStack

This script contains a class that represents a multi-layered grid. This
can be used in a painting application. This multilayered grid provides
functionality to write on different layers, merge them and move them.
"""

from copy import deepcopy


class GridStack:
    """Class to represent a multilayered paint application

    Attributes
    ----------
    __max_layers - int
        the maximum layers possible in the grid stack
    __num_layers - int
        the number of layers in the grid stack
    __rows = rows - int
        the number of row in every grid of the grid stack
    __columns - int
        the number of columns in every grid of the grid stack
    __bg_color - int
        the background color of the grids
    __visible_grid_stack - list
        the grid stack shown in the interface
    __empty_grid - list
        an empty grid to show an invisible layer
    __grid_stack - list
        the grid stack having layers that were made invisible

    Methods
    -------
    get_grid_stack_layer(layer)
        Returns the grid stack array
    get_num_layers()
        Returns the number of layers currently in the grid stack
    get_max_num_layers()
        Returns the maximum number of layers possible in the grid stack\
    init_grid()
        Initialize a 2-dimensional grid representing one layer of the grid stack
    toggle_layer_invisibility(index)
        Toggle the invisibility of the specified layer
    add_layer()
        Add a layer to the end of the grid stack
    delete_layer(index)
        Delete the specified layer from the grid stack
    merge_layer(index_1, index_2)
        Merge the two specified layers
    swap_layers(index_1, index_2)
        Swap the two specified layers
    show_merged_stack_view():
        Shows how the grid stack would look if viewed from above
    """

    def __init__(self, rows, columns, background_color):
        self.__num_layers = 0
        self.__max_layers = 5  # the maximum number of layers the grid stack can have at any time
        self.__rows = rows
        self.__columns = columns
        self.__bg_color = background_color

        self.__visible_grid_stack = []
        self.__empty_grid = [[background_color] * columns for _ in range(rows)]
        self.__grid_stack = [self.__empty_grid for _ in range(self.__max_layers)]

        # creating a layer in the grid stack
        self.add_layer()

    def get_grid_stack_layer(self, layer):
        """Returns the grid stack array

        Parameter
        ---------
        layer - int
            the index of the layer to return

        Returns
        -------
        list
            3-dimensional list representing the grid stack
        """

        return self.__visible_grid_stack[layer]

    def get_num_layers(self):
        """Returns the number of layers currently in the grid stack

        Returns
        -------
        int
            the number of layers
        """

        return self.__num_layers

    def get_max_num_layers(self):
        """Returns the maximum number of layers possible in the grid stack

        Returns
        -------
        int
            the maximum number of layers
        """

        return self.__max_layers

    def init_grid(self):
        """Initialize a 2-dimensional grid representing one layer of the grid stack

        Return
        ------
        list
            the 2-dimensional grid
        """

        # making the grid by looping over rows and columns
        grid = [[self.__bg_color] * self.__columns for _ in range(self.__rows)]

        return grid

    def toggle_layer_invisibility(self, index):
        """Toggle the invisibility of the specified layer

        Parameters
        ----------
        index - int
            the index of the layer whose invisibility is to be toggled
        """

        # swap the layer in the grid stack and the visible grid stack
        temp = self.__visible_grid_stack[index]
        self.__visible_grid_stack[index] = self.__grid_stack[index]
        self.__grid_stack[index] = temp

    def add_layer(self):
        """Add a layer to the end of the grid stack"""

        # initialize a grid
        grid = self.init_grid()

        # add initialized layer to stack
        self.__visible_grid_stack.append(grid)

        # increment the number of layers
        self.__num_layers += 1

    def delete_layer(self, index):
        """Delete the specified layer from the grid stack

        Parameters
        ----------
        index - int
            the index of the layer to delete
        """

        # delete the layer
        self.__visible_grid_stack.pop(index)

        # decrementing the number of layers
        self.__num_layers -= 1

    def merge_layer(self, index_1, index_2):
        """Merge the two specified layers

        Parameters
        ----------
        index_1 - int
            the index of the first layer
        index_2 - int
            the index of the second layer
        """

        # making sure index_1 is the smaller index so that layers that were added
        # first show their value on conflicting grid cells
        index_swapped = False
        if index_1 > index_2:

            # swapping the index
            index_swapped = True
            temp = index_1
            index_1 = index_2
            index_2 = temp

        # using smaller names for the two layers to merge
        layer_1 = self.__visible_grid_stack[index_1]
        layer_2 = self.__visible_grid_stack[index_2]

        # looping over both layers
        for i in range(self.__rows):
            for j in range(self.__columns):

                # copying cells of layer 2 on layer 1 where only layer 2 has contents
                if layer_1[i][j] == self.__bg_color and layer_2[i][j] != self.__bg_color:
                    layer_1[i][j] = layer_2[i][j]

        # deleting layer 2
        if index_swapped:
            self.delete_layer(index_1)
        else:
            self.delete_layer(index_2)

    def swap_layers(self, index_1, index_2):
        """Swap the two specified layers

        Parameters
        ----------
        index_1 - int
            the index of the first layer
        index_2 - int
            the index of the second layer
        """

        # swapping the positions of the layers in the grid stack
        temp = self.__visible_grid_stack[index_1]
        self.__visible_grid_stack[index_1] = self.__visible_grid_stack[index_2]
        self.__visible_grid_stack[index_2] = temp

    def show_merged_stack_view(self):
        """Shows how the grid stack would look if viewed from above

        Returns
        -------
        list
            the two-dimensional list representing the stack view
        """

        # making a copy of the top layer
        stack_view = deepcopy(self.__visible_grid_stack[0])

        # looping through all the cells in a grid:
        for i in range(self.__rows):
            for j in range(self.__columns):

                # looping through the layers in the grid
                for layer in self.__visible_grid_stack:

                    # adding cell to stack view if cell is not empty
                    if layer[i][j] != self.__bg_color:
                        stack_view[i][j] = layer[i][j]
                        break

        return stack_view
