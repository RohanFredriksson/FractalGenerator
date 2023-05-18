
from multiprocessing import Process, Queue
from PIL import Image, ImageOps
import numpy

import mandelbrot

def generate_image(position: tuple[float, float], zoom: float, iterations: int, resolution: tuple[float: float], num_processes: int = 8):

    # Find the maximum and minimum coordinates of the image we are generating.
    x = position[0]
    y = position[1]
    width = resolution[0]
    height = resolution[1]
    units_per_pixel = 5 / (zoom * width)
    real_min = x - (width / 2) * units_per_pixel
    real_max = x + (width / 2) * units_per_pixel
    complex_min = y - (height / 2) * units_per_pixel
    complex_max = y + (height / 2) * units_per_pixel

    # To generate the image, we will generate slices of the image in parallel then combine them together.
    # Create child processes and delegate the tasks to the children.
    processes = []
    slices = Queue()
    width_total = 0
    for i in range(num_processes - 1):

        current_width = width // num_processes
        width_total = width_total + current_width

        # Create the current slice.
        p = Process(target=generate_slice,args=(
                current_width, 
                height, 
                real_min + i * current_width * units_per_pixel, 
                complex_min, 
                real_min + (i+1) * current_width * units_per_pixel,
                complex_max, 
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
            real_min + width_total * units_per_pixel, 
            complex_min, 
            real_max, 
            complex_max, 
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
    image = Image.new('L',(width,height))
    width_total = 0
    for slice in slice_list:
        image.paste(slice,(width_total,0))
        width_total = width_total + slice.size[0]

    # Return the completed image.
    return image

def generate_slice(width, height, real_min, complex_min, real_max, complex_max, iterations, slice_number, queue):

    # Calculate the delta values
    real_delta = (real_max - real_min) / width
    complex_delta = (complex_max - complex_min) / height

    # Create an image to store the slice
    img = numpy.zeros((height,width), numpy.uint8)

    # Compute the slice
    for i in range(width):
        for j in range(height):
            real = real_min + i * real_delta
            complex = complex_max - j * complex_delta
            img[j,i] = 255 * mandelbrot.compute(real, complex, iterations)

    # Store the 2D array in the image object and return it to the queue.
    img = Image.fromarray(img,'L')
    queue.put((slice_number,img))

def main():

    # Generate each frame.
    frames = []
    durations = []
    for iterations in range(1, 65):
        
        # Generate a grayscale image using multiprocessing.
        image = generate_image((0, 0), 1, iterations, (1920, 1080))

        # Apply post processing to the image. 
        # Could be the application of a color map or whatever.
        image = ImageOps.colorize(image, 'black', 'magenta')

        # Add the frame to the frames list.
        frames.append(image)
        durations.append(1)
    
    # Save the frames into a video. Here is an example of how to save it as a GIF.
    frames[0].save('iterations.gif', format="GIF", save_all=True, append_images=frames[1:], duration=durations, loop=0)

if __name__ == '__main__':
    main()