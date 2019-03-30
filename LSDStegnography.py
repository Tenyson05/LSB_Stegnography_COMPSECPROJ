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


def encode_image(encode_text, target_image="chi.jpg"):
	target_image = Image.open(target_image)
	red_pixels = target_image.split()[0]
	green_pixels = target_image.split()[1]
	blue_pixels = target_image.split()[2]

	x_axis = target_image.size[0]
	y_axis = target_image.size[1]

	#draw text
	image_text = write_text(encode_text, target_image.size)
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


if __name__ == '__main__':
	encode_image("hello world")