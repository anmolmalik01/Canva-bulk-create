import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from helper import get_random_font, find_font_size, get_visible_color

def main(image_directory, save_directory):
    text_array = [ "Meet womens near you", "Relationship feels boring, here's you the solution", "Find your kinky partner today", "Explore your dark side", "Meet the nautiest women of your life" ]

    files = os.listdir(image_directory)
    image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg'))]

    for i, image_file in enumerate(image_files):
        image_path = os.path.join(image_directory, image_file)

        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        text = text_array[i % len(text_array)]

        # ======= Choosing font style ============
        font_dir = os.path.join(os.getcwd(), 'fonts')
        random_font_path = get_random_font(font_dir)

        # =========== Chosing font size ==========
        font_size = find_font_size(text=text, font_path=random_font_path, image=img, img_fraction=0.60)

        # ======= Chossing font color =============
        font_color = get_visible_color(style="mono", image_path=image_path , brightness_variation=0.7, hue_variation=0.7, saturation_variation=0.6)

        font = ImageFont.truetype(random_font_path, font_size)

        # width and height of text
        w, h = draw.textsize(text, font=font)

        # position to center the text
        left = (img.width - w) / 2
        top = (img.height - h) * (3/4)

        draw.text((left, top), text, font=font, fill=font_color)

        modified_image_path = os.path.join(save_directory, 'modified_' + image_file)
        img.save(modified_image_path)

        print(f" {i+1}st image saved")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process images with text.')
    parser.add_argument('--image_directory', type=str, required=True, help='Directory containing images.')
    parser.add_argument('--save_directory', type=str, required=True, help='Directory to save modified images.')
    args = parser.parse_args()

    main(args.image_directory, args.save_directory)