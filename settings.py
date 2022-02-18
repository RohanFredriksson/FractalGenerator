import json
import copy

# Default Settings - Change Here
default_settings = {
    'x': -0.75,
    'y': 0,
    'zoom': 1,
    'width': 1920,
    'height': 1080,
    'iterations': 64,
    'fractal':'mandelbrot',
    'color':{
        'map':'grayscale',
        'type':{
            'name':'wave',
            'frequency':3
        }
    }
}

def add_missing_keys(current_dict, default_dict):

    # If the variable is not a dictionary, make it one.
    if type(current_dict) != dict:
        current_dict = {}

    for key in default_dict:

        # If the key is in the default dictionary, and not in the current dictionary, add it.
        if key not in current_dict:
            current_dict[key] = default_dict[key]

        # If the key is in the current dictionary and is a dictionary, check it.
        elif type(key) == dict:
            add_missing_keys(current_dict[key], default_dict[key])

# Set up user settings.
settings = copy.deepcopy(default_settings)

try:

    # Try and read the settings from the file.
    with open('settings.json') as settings_file:
        file_settings = json.load(settings_file)

    # Add any missing keys.
    add_missing_keys(file_settings, default_settings)

    settings = file_settings

except (OSError, json.JSONDecodeError) as e:

    # If the file cannot be found, or is an invalid JSON file, rewrite it with default settings.
    with open("settings.json", "w") as settings_file:
        json.dump(default_settings, settings_file)

def save():
    
    # Write the settings to the file.
    with open("settings.json", "w") as settings_file:
        json.dump(settings, settings_file)

