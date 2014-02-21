# Ice Worm Counter
#
# Take in an image of ice worms on snow, and count the worms.

# Strategies:
#  Sum rgb, look for connected areas below certain level.
#  Convert to grayscale, look for brightness values below certain level.
#  Increase contrast before running algorithm?
#   Probably not needed.


from PIL import Image
import sys

# Parameters
# sample_res: How many rows to skip between samples
sample_res = 1

# Open image, store data.
raw_image = Image.open('raw_images/ice_worms_1_high_contrast.jpg')
raw_image = Image.open('raw_images/ice_worms_1.jpg')
image_data = raw_image.getdata()
image_width, image_height = raw_image.size


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


def make_color_histogram():
    # Make bins
    num_bins = 20
    bin_size = (3*255)/num_bins
    # Where does each bin end?
    bin_ends = [x*bin_size for x in range(num_bins)]
    # Initialize bins.
    bins = [0 for bin in range(0,num_bins+1)]

    # Make a histogram of color values.
    for row in rows:
        for pixel in row:
            sum_rgb = sum(pixel)
            # Place this pixel in a bin.
            #  Bin number is round(sum_rgb/bin_size)
            bin_number = int(round(sum_rgb/bin_size))
            bins[bin_number] += 1

    print bins


make_color_histogram()
