"""
Raw Shark Texts Image Converter

This script converts input images to jumbled overlapping text in "The Raw Shark Texts" style.

Usage:
    python script_name.py

Configuration:
    The configuration settings are specified in the 'config.ini' file.

"""

import os
from collections import namedtuple
from PIL import Image, ImageDraw
from manager.config import CONFIG

# Define a named tuple for pixel coordinates
PixelCoords = namedtuple("PixelCoords", ["x", "y"])

# Initialize default_config
default_config = CONFIG["default"]


def get_intensity(pixel_data, coords, width, height, radius=1):
    """
    Calculate intensity considering the neighborhood of pixels.

    Args:
        pixel_data (list): List of pixel intensities.
        coords (PixelCoords): Coordinates of the pixel.
        width (int): Width of the image.
        height (int): Height of the image.
        radius (int): Radius to consider for intensity calculation. Default is 1.

    Returns:
        int: Calculated intensity.
    """
    total_intensity = 0
    count = 0
    for i in range(max(0, coords.x - radius), min(width, coords.x + radius + 1)):
        for j in range(max(0, coords.y - radius), min(height, coords.y + radius + 1)):
            total_intensity += pixel_data[j * width + i]
            count += 1
    return total_intensity // count if count > 0 else 0


def convert_to_raw_shark_text(input_file, output_file):
    """
    Converts input image to jumbled overlapping text in "The Raw Shark Texts" style.

    Args:
        input_file (str): Input File.
        output_file (str): Output File.
    """
    original_image = Image.open(input_file).convert("L")
    pixel_data, width, height = list(original_image.getdata()), *original_image.size

    # Create a new image and drawing object
    raw_shark_text_image = Image.new(
        "RGB", (width, height), color=default_config["BACKGROUND_COLOR"]
    )
    draw = ImageDraw.Draw(raw_shark_text_image)

    for pixel_y in range(0, height, default_config.getint("STEP_SIZE")):
        for pixel_x in range(0, width, default_config.getint("STEP_SIZE")):
            coords = PixelCoords(pixel_x, pixel_y)
            intensity = get_intensity(
                pixel_data, coords, width, height, default_config.getint("RADIUS")
            )
            intensity_scale = len(default_config["CHARACTER_SET"]) - 1
            intensity = min(max(intensity * intensity_scale // 255, 0), intensity_scale)
            draw.text(
                (pixel_x, pixel_y),
                default_config["CHARACTER_SET"][intensity],
                fill=default_config["TEXT_COLOR"],
            )

    raw_shark_text_image.save(output_file)


if __name__ == "__main__":
    os.makedirs(default_config["OUTPUT_FOLDER"], exist_ok=True)

    for image in os.listdir(default_config["INPUT_FOLDER"]):
        if image.endswith(".png"):
            input_path, output_path = os.path.join(
                default_config["INPUT_FOLDER"], image
            ), os.path.join(default_config["OUTPUT_FOLDER"], image)
            convert_to_raw_shark_text(input_path, output_path)
