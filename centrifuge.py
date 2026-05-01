#!/usr/bin/env python3

import argparse, os, shutil
from PIL import Image

def main():
    """
    Extract images from Factorio spritesheets and convert them into a GIF file
    """
    PATH = "./temp/"
    if not os.path.isdir(PATH):
        os.mkdir(PATH)

    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-o", "--output", required=True)
    p.add_argument("-d", "--duration", type=int, default=50 ,help="Define duration in milliseconds of each frame in the GIF (Don't set too low or your GIF might render REALLY slowly!) (Default: 50)")
    p.add_argument("-k", "--keep-temp", default=False, action="store_true", help="Don't delete temporary folder containing frames used to build the GIF.")
    args = p.parse_args()
    spritesheet = Image.open(args.input)
    width, height = spritesheet.size

    horizontal_items = int(input("Number of horizontal items: "))
    vertical_items = int(input("Number of vertical items: "))

    real_width = width / horizontal_items
    real_height = height / vertical_items

    left = 0
    up = 0

    right = real_width
    down = real_height
    files = []

    for i in range(vertical_items):
        for l in range(horizontal_items):
            print(f"{left} {up} | {right*(l+1)} x {down*(i+1)}")
            frame = spritesheet.crop((left, up, right*(l+1), down*(i+1)))
            save = f"{PATH}/frame_{i}-{l}.png"
            frame.save(save)
            files.append(save)
            left += right
        left = 0
        up += down
    frames = [Image.open(image) for image in files]
    frames[0].save(args.output, save_all=True, append_images=frames[1:], duration=args.duration, loop=0, lossless=True, optimize=False)
    if not args.keep_temp:
        shutil.rmtree(PATH)


if __name__ == "__main__":
    main()
