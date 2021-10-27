class Colour:

    def __init__(self, r: int,g: int, b: int):

        if r < 0:
            r = 0
        elif r > 255:
            r = 255

        if g < 0:
            g = 0
        elif g > 255:
            g = 255

        if b < 0:
            b = 0
        elif b > 255:
            b = 255

        self.r = r
        self.g = g
        self.b = b

    def to_colour_list(self):
        return [self.r,self.g,self.b]

class ColourMap:

    def __init__(self):
        self.colours = {}

    def add_colour(self,position: float, colour: Colour):
        
        if position < 0.0:
            position = 0.0
        elif position > 1.0:
            position = 1.0
        
        self.colours[position] = colour

    def get_colour(self,position):

        # If there are no colours, return the black colour.
        if len(self.colours) == 0:
            return Colour(0,0,0)

        # If there is only one colour in the map, take that one.
        if len(self.colours) == 1:
            return self.colours[self.colours.keys()[0]]

        # If the colour is in the map return it, else we have to interpolate.
        if (position in self.colours):
            return self.colours[position]

        # Get a list of all keys.
        keys = list(self.colours.keys())

        x = min(keys) # Largest key less than the position.
        y = max(keys) # Smallest key greater than the position.

        for key in keys:
            if key < position and key > x:
                x = key
            elif key > position and key < y:
                y = key

        # Get the colours associated with the positions.
        x_colour = self.colours[x]
        y_colour = self.colours[y]

        # Calculate the gradient for each channel between the two points.
        r_gradient = (y_colour.r - x_colour.r) / (y - x)
        g_gradient = (y_colour.g - x_colour.g) / (y - x)
        b_gradient = (y_colour.b - x_colour.b) / (y - x)
        
        # Calculate the interpolated values for the new colour.
        r_new = round(x_colour.r + r_gradient * (position - x))
        g_new = round(x_colour.g + g_gradient * (position - x))
        b_new = round(x_colour.b + b_gradient * (position - x))

        return Colour(r_new, g_new, b_new)