import json
from color import *
from colormap import *

class ColorMaps:

    def __init__(self):
        self.maps = {}

        # Read all the color maps from the json file.
        json_file = open('colormaps.json')
        colormapsJSON = json.load(json_file)

        # Parse the json into a map of color map objects
        for colormapJSON in colormapsJSON:

            new_colormap = ColorMap()
            
            # Add all the colors to the current color map.
            for point in colormapJSON['points']:   
                new_colormap.add_color(point['position'],Color(point['color']['r'],point['color']['g'],point['color']['b']))

            self.maps[colormapJSON['name']] = new_colormap

    def get_color_map(self, name: str):

        # Try and get the color map from the map
        c = self.maps[name]

        # If the map doesn't exist, return an empty color map.
        if c == None:
            return ColorMap()

        return c

maps = ColorMaps()