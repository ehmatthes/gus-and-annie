from PIL import Image

# How many rows to skip between samples
sample_res = 1

# open image, store data
shredded_image = Image.open('/home/matthese/Desktop/unshredder/TokyoPanoramaShredded.png')
shredded_data = shredded_image.getdata()

image_width, image_height = shredded_image.size
print image_width, image_height

# get a column of pixels
#  returns a list of pixel data, len=image_height/sample_res
def get_column(column_index):
	#print 'ci: ' + str(column_index)
	pixel_data = []
	# range has +1 to include 0 row
	for row_index in range (image_height/sample_res):
		#print 'ri: ' + str(row_index)
		pixel_data.append(shredded_data[row_index*image_width + column_index*sample_res]) 
		#print y_index*sample_res
	return pixel_data
			
columns = []
for column_index in range(0,image_width):
	columns.append(get_column(column_index))
	#print column_index
#print len(columns)

# seems to store all pixel data correctly


# Create unshredded image
painted_image = Image.new("RGBA", shredded_image.size)
for col_index, column in enumerate(columns):
	for row_index, pixel in enumerate(column):
		#print 'ci: ' + str(col_index) + ', ri: ' + str(row_index)
		painted_image.putpixel((col_index,row_index), pixel)
painted_image.save('/home/matthese/Desktop/unshredder/painted_image.jpg', 'JPEG')








