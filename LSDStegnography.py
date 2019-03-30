from PIL import Image, ImageFont, ImageDraw
import textwrap


def write_text(text_to_write, image_size):
	"""writes text to an RGB image"""
	image_text = Image.new("RGB", image_size)
	font = ImageFont.load_default().font
	drawer = ImageDraw.Draw(image_text)

	#changes the parameters for different text wrapping
	margin = 10
	offset = 10
	for line in textwrap.wrap(text_to_write, width=60):
		drawer.text((margin,offset), line, font=font)
		offset += 10
	return image_text


def encode_image(encode_text, imageToEncode="chi.jpg"):
	"""encodes a hidden message in a selected image"""
	imageToEncode = Image.open(imageToEncode)
	red_pixels = imageToEncode.split()[0]
	green_pixels = imageToEncode.split()[1]
	blue_pixels = imageToEncode.split()[2]

	x_axis = imageToEncode.size[0]
	y_axis = imageToEncode.size[1]

	#draw text
	image_text = write_text(encode_text, imageToEncode.size)
	bw_encode = image_text.convert('1')

	#encode text into image
	encoded_image = Image.new("RGB", (x_axis, y_axis))
	pixels = encoded_image.load()
	for i in range(x_axis):
		for j in range(y_axis):
			red_pixel_templates = bin(red_pixels.getpixel((i,j)))
			old_pixel = red_pixels.getpixel((i,j))
			tencode_pixel = bin(bw_encode.getpixel((i,j)))

			if tencode_pixel[-1] == '1':
				red_pixel_templates = red_pixel_templates[:-1] + '1'
			else:
				red_pixel_templates = red_pixel_templates[:-1] + '0'
			pixels[i, j] = (int(red_pixel_templates, 2), green_pixels.getpixel((i,j)), blue_pixels.getpixel((i,j)))

		#saved the file as a png to avoid quality lost
	encoded_image.save("encoded_image.png")
	print("done")


def decode_image(imageToDecode="encoded_image.png"):
	"""Decodes the hidden message in the selected image"""
	encoded_image = Image.open(imageToDecode)
	red_pixs = encoded_image.split()[0]

	x_axis = encoded_image.size[0]
	y_axis = encoded_image.size[1]

	decoded_image = Image.new("RGB", encoded_image.size)
	pixels = decoded_image.load()

	for i in range(x_axis):
		for j in range(y_axis):
			if bin(red_pixs.getpixel((i, j)))[-1] == '0':
				pixels[i, j] = (255, 255, 255)
			else:
				pixels[i, j] = (0,0,0)
	decoded_image.save("decoded_image.png")
	print("Done decoding")



if __name__ == '__main__':
	# encode_image("This is computer security!!!")
	decode_image()