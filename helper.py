import os
from PIL import Image, ImageFont
import random
import colorsys
import numpy as np



# ================ font family ================
def get_random_font(directory):
    files = os.listdir(directory)
    font_files = [file for file in files if file.endswith(('.ttf', '.otf'))]
    
    random_font = random.choice(font_files)
    
    return os.path.join(directory, random_font)



# ================ color ================
def find_dominant_color(image_path):
    width, height = 150, 150
    image = Image.open(image_path)
    image = image.resize((width, height), resample=Image.LANCZOS)

    img_array = np.array(image)
    pixels = img_array.reshape((-1, 3))

    unique_colors, color_counts = np.unique(pixels, axis=0, return_counts=True)
    sorted_color_counts = np.argsort(color_counts)[::-1]

    dominant_color = unique_colors[sorted_color_counts[0]]
    return tuple(dominant_color)


def monochromatic_color(background_color, brightness_variation, hue_variation, saturation_variation):
    h, s, v = colorsys.rgb_to_hsv(*[x / 255.0 for x in background_color])

    v_i = min(1.0, max(0.0, v + brightness_variation))
    h_i = min(1.0, max(0.0, h + hue_variation))
    s_i = min(1.0, max(0.0, s + saturation_variation))

    r, g, b = colorsys.hsv_to_rgb(h_i, s_i, v_i)

    return (int(r * 255), int(g * 255), int(b * 255))


def complementary_color(background_color, brightness_variation, hue_variation, saturation_variation):
    h, s, v = colorsys.rgb_to_hsv(*[x / 255.0 for x in background_color])
    
    complementary_hue = (h + hue_variation) % 1.0
    
    s = min(1.0, max(0.0, s + saturation_variation))
    v = min(1.0, max(0.0, v + brightness_variation))
    
    r, g, b = colorsys.hsv_to_rgb(complementary_hue, s, v)
    
    return (int(r * 255), int(g * 255), int(b * 255))


def get_visible_color(style, image_path , brightness_variation, hue_variation, saturation_variation):
    dominant_color = find_dominant_color(image_path)
    
    if style=='complementary':
        visible_color = complementary_color(dominant_color, brightness_variation, hue_variation, saturation_variation)
    elif style=='mono':
        visible_color = monochromatic_color(dominant_color, brightness_variation, hue_variation, saturation_variation)
    
    return visible_color



# ================ font size ================
def find_font_size(text, font_path, image, img_fraction):
    fontsize = 1
    font = ImageFont.truetype(font_path, fontsize)
    
    while font.getsize(text)[0] < img_fraction * image.size[1]:
        fontsize += 1
        font = ImageFont.truetype(font_path, fontsize)
    
    fontsize -= 1
    
    return fontsize