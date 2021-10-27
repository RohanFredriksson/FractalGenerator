import json
from colour import *
from colourmap import *

class ColourMaps:

    def __init__(self):
        self.maps = {}

        # Read all the colour maps from the json file.
        json_file = open('colourmaps.json')
        colourmapsJSON = json.load(json_file)

        # Parse the json into a map of colour map objects
        for colourmapJSON in colourmapsJSON:

            new_colourmap = ColourMap()
            
            # Add all the colours to the current colour map.
            for point in colourmapJSON['points']:   
                new_colourmap.add_colour(point['position'],Colour(point['colour']['r'],point['colour']['g'],point['colour']['b']))

            self.maps[colourmapJSON['name']] = new_colourmap

    def get_colour_map(self, name: str):

        # Try and get the colour map from the map
        c = self.maps[name]

        # If the map doesn't exist, return an empty colour map.
        if c == None:
            return ColourMap()

        return c

maps = ColourMaps()