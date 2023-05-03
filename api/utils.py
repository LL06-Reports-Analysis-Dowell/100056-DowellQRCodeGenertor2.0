from PIL import Image
import base64
import io
import pyshorteners

def change_image_color_(image_path, new_color):
    # Load the image
    image = Image.open(image_path)

    # Convert the image to RGBA mode
    image = image.convert("RGBA")

    # Get the width and height of the image
    width, height = image.size

    # Create a new blank image of the same size and mode as the original image
    new_image = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))

    # Loop through each pixel in the image and change its color
    for x in range(width):
        for y in range(height):
            # Get the current pixel color
            current_color = image.getpixel((x, y))

            # Check if the current pixel color is not transparent
            if current_color[3] != 0:
                # Create a new color tuple with the specified color and alpha
                new_color_with_alpha = tuple(int(new_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (current_color[3],)

                # Replace the current pixel color with the new color
                new_image.putpixel((x, y), new_color_with_alpha)

    # Return the modified image
    return new_image


def resize_image(image_path, size):
    """
    Resizes the image at the given path to the given size.
    """
    # Open the image
    with Image.open(image_path) as image:
        # Calculate the new size
        width, height = image.size
        new_size = (int(size * width), int(size * height))
        # Resize the image
        resized_image = image.resize(new_size)
        # Return the resized image
        return resized_image


# def change_image_color(image, color_from, color_to):
#     """
#     Changes the color of the given image from color_from to color_to.
#     """
#     if not is_valid_hex_color(color_from):
#         raise ValueError("Invalid hex color code for color_from.")
#     if not is_valid_hex_color(color_to):
#         raise ValueError("Invalid hex color code for color_to.")

#     # Convert color codes to RGB tuples
#     rgb_from = tuple(int(color_from[i:i+2], 16) for i in (1, 3, 5))
#     rgb_to = tuple(int(color_to[i:i+2], 16) for i in (1, 3, 5))

#     # Replace the color in the image
#     data = np.array(image)
#     r, g, b, a = np.rollaxis(data, axis=-1)
#     mask = (r == rgb_from[0]) & (g == rgb_from[1]) & (b == rgb_from[2])
#     data[..., :-1][mask] = rgb_to
#     return Image.fromarray(data)