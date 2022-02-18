from color import *
import math

class ColorMap:

    def __init__(self):
        self.colors = {}

    def add_color(self,position: float, color: Color):
        
        # Clamp the position
        position = min(position, 1)
        position = max(position, 0)
        
        self.colors[position] = color

    def get_color(self, position: float, colortype: dict):

        # If there are no colors, return the black color.
        if len(self.colors) == 0:
            return Color(0,0,0)

        # If there is only one color in the map, take that one.
        if len(self.colors) == 1:
            return self.colors[self.colors.keys()[0]]

        # Clamp the position
        position = min(position, 1)
        position = max(position, 0)

        # Change the position depending on the color type
        if colortype['name'] == 'wave':

            # Get the frequency
            frequency = 1
            if 'frequency' in colortype:
                if type(colortype['frequency']) == int or type(colortype['frequency']) == float:
                    frequency = colortype['frequency']

            # Get the new position
            position = math.sin(frequency * math.pi * position) ** 2

        # If the color is in the map return it, else we have to interpolate.
        if (position in self.colors):
            return self.colors[position]

        # Get a list of all keys.
        keys = list(self.colors.keys())

        x = min(keys) # Largest key less than the position.
        y = max(keys) # Smallest key greater than the position.

        for key in keys:
            if key < position and key > x:
                x = key
            elif key > position and key < y:
                y = key

        # Get the colors associated with the positions.
        x_color = self.colors[x]
        y_color = self.colors[y]

        # Calculate the gradient for each channel between the two points.
        r_gradient = (y_color.r - x_color.r) / (y - x)
        g_gradient = (y_color.g - x_color.g) / (y - x)
        b_gradient = (y_color.b - x_color.b) / (y - x)
        
        # Calculate the interpolated values for the new color.
        r_new = round(x_color.r + r_gradient * (position - x))
        g_new = round(x_color.g + g_gradient * (position - x))
        b_new = round(x_color.b + b_gradient * (position - x))

        return Color(r_new, g_new, b_new)