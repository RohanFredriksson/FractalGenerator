import sys
import numpy
from PIL import Image

import mandelbrot
from greyscale import * 

def main():
    
    args = sys.argv
    if len(args) < 7:
        print("Not enough arguments provided.\n\nUsage:   python3 main.py x y zoom width height iterations [filename]\nExample: python3 main.py -0.75 0 1 1920 1080 64\n")
        return

    x = 0
    y = 0
    zoom = 0
    width = 0
    height = 0
    iterations = 0

    try:
        x = float(args[1])
        y = float(args[2])
        zoom = float(args[3])
        width = int(args[4])
        height = int(args[5])
        iterations = int(args[6])
    except:
        print("Error: One of the numeric arguments is not numerical.")
        return

    filename = "fractal.png"
    if len(args) > 7:
        filename = args[7]

    units_per_pixel = 5 / (zoom * width)

    r_max = x + (width / 2) * units_per_pixel
    c_max = y + (height / 2) * units_per_pixel

    r_min = x - (width / 2) * units_per_pixel
    c_min = y - (height / 2) * units_per_pixel

    r_delta = (r_max - r_min) / width
    c_delta = (c_max - c_min) / height

    img = numpy.zeros((height,width,3), numpy.uint8)

    for i in range(width):
        for j in range(height):

            r = r_min + i * r_delta
            c = c_max - j * c_delta

            img[j,i] = greyscale.get_colour(mandelbrot.compute(r,c,iterations)).to_colour_list()

    img = Image.fromarray(img,'RGB')
    img.save(filename)
    img.show()

if __name__ == '__main__':
    main()