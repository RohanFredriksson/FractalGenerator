import sys
import numpy
from PIL import Image

import mandelbrot
from greyscale import * 

def main():
    
    args = sys.argv
    if len(args) < 7:
        print("Not enough arguments provided.\nExample usage: python3 main.py width height iterations r_max c_max r_min c_min [filename]")
        return

    width = 0
    height = 0
    iterations = 0
    r_max = 0.0
    c_max = 0.0
    r_min = 0.0
    c_min = 0.0

    try:
        width = int(args[1])
        height = int(args[2])
        iterations = int(args[3])

        r_max = float(args[4])
        c_max = float(args[5])

        r_min = float(args[6])
        c_min = float(args[7])
    except:
        print("Error: One of the numeric arguments is not numerical.")
        return

    filename = "fractal.png"
    if len(args) > 8:
        filename = args[8]

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