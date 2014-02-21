from PIL import Image
import sys

# How many rows to skip between rows that will be analyzed
#  Sample_res in range ~50-100 works for many images.
sample_res = 1

# Open image, store data
shredded_image = Image.open('TokyoPanoramaShredded.png')
shredded_image = Image.open('sample.jpg')
shredded_data = shredded_image.getdata()
image_width, image_height = shredded_image.size

#  Returns a list of pixel data, length=image_height/sample_res
def get_column(column_index):
	pixel_data = []
	for row_index in range (image_height/sample_res):
		pixel_data.append(shredded_data[row_index*sample_res*image_width + column_index]) 
	return pixel_data

# Store all pixel data in a list of columns, since that is how we will
#  be dealing with it.
columns = []
for column_index in range(0,image_width):
	columns.append(get_column(column_index))

# Compares two columns.  Returns the total of absolute differences
#  between rgb values.
def compare_columns(index_a, index_b):
	diff = 0
	for row_index in range (image_height/sample_res):
		for rgb_index in range(3):
			diff +=abs(columns[index_a][row_index][rgb_index] - columns[index_b][row_index][rgb_index])
	return diff

# Find the first pair of columns that have diff >= 2*diff(col_0, col_1)
#  Will fail if first two strips are correctly matched.
#  (will return 2*strip_width)
def get_strip_width():
	diff_0_1 = compare_columns(0,1)
	for column_index in range(0,image_width):
		if compare_columns(column_index, column_index+1) >= 2*diff_0_1:
			strip_width = column_index+1
			return strip_width
			
strip_width = get_strip_width()

# Compares the right col of one strip against left col of second strip.
def compare_right_left(right_strip_index, left_strip_index):
	right_col_index = (right_strip_index+1) * strip_width - 1
	left_col_index = left_strip_index * strip_width
	return compare_columns(right_col_index, left_col_index)

# Compare right of first strip to left of each successive strip.
#  Match pairs with lowest difference sums.
#  max(min_diffs) can be used to find right edge of image.
matches = {}
min_diffs = []
for base_strip_index in range (0,image_width/strip_width):
	diffs = []
	for candidate_strip_index in range (0,image_width/strip_width):
		if base_strip_index == candidate_strip_index:
			diffs.append(999999)
		else:
			diffs.append(compare_right_left(base_strip_index, candidate_strip_index))
			
	matches[base_strip_index] = diffs.index(min(diffs))
	min_diffs.append(min(diffs))

# Run through matches.  If a matching pair has a vertical region with
#  every pixel different from its corresponding pixel by threshold amount,
#  then left of pair is right edge of image.
# This may also be used to resolve conflicts in duplicate matches.
def check_edges(index_a, index_b):
	threshold = 30
	consecutive_above_threshold = max_consecutive_above_threshold = 0
	right_col_index = (index_a+1) * strip_width - 1
	left_col_index = index_b * strip_width
	for row_index in range (image_height/sample_res):
		diff = 0
		for rgb_index in range(3):
			diff += abs(columns[right_col_index][row_index][rgb_index] - columns[left_col_index][row_index][rgb_index])
		if diff > threshold:
			consecutive_above_threshold += 1
			if consecutive_above_threshold > max_consecutive_above_threshold:
				max_consecutive_above_threshold = consecutive_above_threshold
		else:
			consecutive_above_threshold = 0
	return max_consecutive_above_threshold

# Find right edge.  This is the left strip in matched pair with
#  greatest 'edginess', determined by check_edges.
edginess = []
for key in matches:
	edginess.append(check_edges(key, matches[key]))
right_strip_index = edginess.index(max(edginess))

# Put strips in order.  Seed list with leftmost strip in shredded image.
strip_order = [0]
while len(strip_order) < image_width/strip_width:
	# Work from first shredded strip to right edge of image
	if strip_order[-1] != right_strip_index:
		strip_order.append(matches[strip_order[-1]])
	else:
		# Work from first shredded strip to left edge
		for left_strip, right_strip in matches.items():
			if right_strip == strip_order[0]:
				strip_order.insert(0, left_strip)
				break


# Create unshredded image
unshredded_image = Image.new("RGBA", shredded_image.size)
for loop_index, strip_index in enumerate(strip_order):
	source_strip_box = (strip_index*strip_width, 0, (strip_index+1)*strip_width, image_height)
	source_strip = shredded_image.crop(source_strip_box)
	destination_point = (loop_index*strip_width, 0)
	unshredded_image.paste(source_strip, destination_point)

file_name = 'TokyoPanoramaUnshredded.jpg'
file_name = 'sample_unshredded.jpg'
unshredded_image.save(file_name, 'JPEG')
