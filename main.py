import numpy
from PIL import Image
from multiprocessing import Process, Queue

import mandelbrot
import colormaps as ColorMaps
import settings as Settings

num_processes = 16
processes = []
slices = Queue()

def main():

    maps = ColorMaps.load()
    settings = Settings.load()

    x = settings['x']
    y = settings['y']
    zoom = settings['zoom']
    width = settings['width']
    height = settings['height']
    iterations = settings['iterations']
    fractal = settings['fractal']
    map_name = settings['color']['map']
    map_colortype = settings['color']['type']
    filename = 'fractal.png'

    # Get the color map object specified by the user.
    c_map = maps.get_color_map(map_name)

    # Compute necessary values
    units_per_pixel = 5 / (zoom * width)

    r_max = x + (width / 2) * units_per_pixel
    c_max = y + (height / 2) * units_per_pixel

    r_min = x - (width / 2) * units_per_pixel
    c_min = y - (height / 2) * units_per_pixel

    width_total = 0
    for i in range(num_processes - 1):

        current_width = width // num_processes
        width_total = width_total + current_width

        # Create the current slice.
        p = Process(target=generate_slice,args=(
                current_width, 
                height, 
                r_min + i * current_width * units_per_pixel, 
                c_min, 
                r_min + (i+1) * current_width * units_per_pixel,
                c_max, 
                c_map, 
                map_colortype,
                iterations, 
                i,
                slices
            )
        )
        processes.append(p)
        p.start()

    # Create the last slice. The last slice might have a different size to the others.
    p = Process(target=generate_slice,args=(
            width - width_total, 
            height, 
            r_min + width_total * units_per_pixel, 
            c_min, 
            r_max, 
            c_max, 
            c_map, 
            map_colortype,
            iterations, 
            num_processes-1,
            slices
        )
    )
    processes.append(p)
    p.start()

    # Get all the slices from the child processes.
    slice_map = {}
    for i in range(num_processes):
        slice = slices.get()
        slice_map[slice[0]] = slice[1]

    # Get a sorted list of keys from the slice map.
    key_list = []
    for key in slice_map.keys():
        key_list.append(key)
    key_list.sort()

    # Create a list of ordered slices.
    slice_list = []
    for key in key_list:
        slice_list.append(slice_map.get(key))

    # Merge the slices
    image = Image.new('RGB',(width,height))
    width_total = 0
    for slice in slice_list:
        image.paste(slice,(width_total,0))
        width_total = width_total + slice.size[0]

    # Save the image
    image.save(filename)

def generate_slice(width, height, r_min, c_min, r_max, c_max, color_map, color_type, iterations, slice_number, queue):
    
    # Calculate the delta values
    r_delta = (r_max - r_min) / width
    c_delta = (c_max - c_min) / height

    # Create an image to store the slice
    img = numpy.zeros((height,width,3), numpy.uint8)

    # Compute the slice
    for i in range(width):
        for j in range(height):

            r = r_min + i * r_delta
            c = c_max - j * c_delta

            img[j,i] = color_map.get_color(mandelbrot.compute(r,c,iterations), color_type).to_rgb_channel_list()
    
    # Store the 2D array in the image object and return it to the queue.
    img = Image.fromarray(img,'RGB')
    queue.put((slice_number,img))

if __name__ == '__main__':
    main()