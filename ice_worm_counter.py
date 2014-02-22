# Ice Worm Counter
#
# Take in an image of ice worms on snow, and count the worms.

# Strategies:
#  Sum rgb, look for connected areas below certain level.
#  Convert to grayscale, look for brightness values below certain level.
#  Increase contrast before running algorithm?
#   Probably not needed.


from PIL import Image
import math

# Parameters
# sample_res: How many rows to skip between samples
sample_res = 1

# Open image, store data.
raw_image = Image.open('raw_images/ice_worms_1_high_contrast.jpg')
#raw_image = Image.open('raw_images/ice_worms_1.jpg')
image_data = raw_image.getdata()
image_width, image_height = raw_image.size

# List of raw sums of pixel data.
raw_sums = []

# Pixels that seem to be part of a worm.
#  This is the indices in the raw_sums list.
#  This list is of variable length.
worm_indices = []


def get_row(row_index):
    # Return a row of pixel data, length = image_width/ sample_res.
    pixel_data = []
    for column_index in range(image_width/sample_res):
        pixel_data.append(image_data[column_index*sample_res + row_index*image_width])
    return pixel_data


# Store all pixel data in a list of rows.
#  This could use a sample rate as well?
rows = []
for row_index in range(0, image_height):
    rows.append(get_row(row_index))


def make_color_histogram(raw_sums, worm_indices):
    # Make bins
    num_bins = 20
    bin_size = (3*255)/num_bins
    # Where does each bin end?
    bin_ends = [x*bin_size for x in range(num_bins)]
    # Initialize bins.
    bins = [0 for bin in range(0,num_bins+1)]

    # Make a histogram of color values.
    pixel_num = 0
    for row in rows:
        for pixel in row:
            sum_rgb = sum(pixel)
            # Place this pixel in a bin.
            #  Bin number is round(sum_rgb/bin_size)
            bin_number = int(round(sum_rgb/bin_size))
            bins[bin_number] += 1

            raw_sums.append(sum_rgb)

            # If this pixel is in the first bin, it's a worm.
            if bin_number == 0:
                worm_indices.append(pixel_num)

            pixel_num += 1


    print bins

    import matplotlib.pyplot as plt
    plt.hist(raw_sums, bins=25)
    plt.title("Pixel values in an ice worm photo")
    plt.xlabel("Sum of rgb values for each pixel")
    plt.ylabel("Number of pixels")
    #plt.show()



make_color_histogram(raw_sums, worm_indices)



print len(raw_sums)
print len(worm_indices)

def draw_red_worms(rows, worm_indices):
    # Redraw the image data, but draw all worm pixels in red.
    red_worms_image = Image.new("RGBA", raw_image.size, (255,255,255,255))

    pixel_num = 0
    num_worm_pixels = 0

    for worm_index in worm_indices:
        # These are the pixels that need to be drawn in red.
        #  worm_index_y = floor (worm_index / image_width)
        #  worm_index_x = remainder
        # Write for py3 math, not dependent on py2 integer div
        worm_index_y = int(math.floor(worm_index/image_width))
        worm_index_x = worm_index % image_width
        red_worms_image.putpixel((worm_index_x, worm_index_y), (255,0,0,255))


    # Would png make better quality?
    red_worms_image.save('results/red_worms.jpg', 'JPEG')

    return 0

    for y, row in enumerate(rows):
        print "Finished row %d of %d." % (y, len(rows))
        for x, pixel in enumerate(row):

            if pixel_num in worm_indices:
                # Place a red pixel.
                #print "Placing worm pixel %d." % num_worm_pixels
                #num_worm_pixels += 1
                red_worms_image.putpixel((x,y), (255,0,0,255))
                #red_worms_image[x,y] = 100
            else:
                # Place original pixel
                #red_worms_image.putpixel((x,y), pixel)
                #red_worms_image.putpixel((x,y), (255,255,255,255))
                pass
            pixel_num += 1

    #red_worms_image.save('/home/ehmatthes/development/projects/ice_worms_counter/results/red_worms.jpg', 'JPEG')
    red_worms_image.save('results/red_worms.jpg', 'JPEG')



draw_red_worms(rows, worm_indices)
