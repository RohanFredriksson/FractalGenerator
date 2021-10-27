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

    def to_rgb_channel_list(self):
        return [self.r,self.g,self.b]