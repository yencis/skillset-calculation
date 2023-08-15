import numpy as np
from PIL import Image, ImageDraw
import cv2


# 512 x 384 with 180 x 72 border (osu pixel size)

def render(beatmap):
    print("Begin rendering")
    x = 512
    y = 384
    x_offset = 180
    y_offset = 72
    scale = 2
    dim = ((x + 2 * x_offset) * scale, (y + 2 * y_offset) * scale)

    radius = (54.4 - 4.48 * beatmap.difficulty.cs) * scale

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter("output.mp4", fourcc, 15, dim)

    print("Total beatmap duration: " + str(beatmap.get_duration()))

    for i in np.arange(0, beatmap.get_duration(), 66.666666666667):  # i in milliseconds, 60 frames per second

        if 0.249 < i / beatmap.get_duration() < 0.251:
            print("25%")

        if 0.499 < i / beatmap.get_duration() < 0.501:
            print("50%")

        if 0.749 < i / beatmap.get_duration() < 0.751:
            print("75%")

        # image = Image.open("x.png") in case we want background
        img = Image.new('RGB', dim, color='black')
        draw = ImageDraw.Draw(img, 'RGBA')

        objects = beatmap.get_objects_at(i)

        for obj in objects[::-1]:  # iterate in reverse for stacking
            opacity = beatmap.get_opacity_of_hitobject(obj, i)

            # process coordinates

            if not obj.is_slider():

                x_img = (obj.x + x_offset) * scale
                y_img = (obj.y + y_offset) * scale

                draw.ellipse(xy=[(x_img - radius, y_img - radius), (x_img + radius, y_img + radius)],
                             fill=(255, 0, 0, int(255 * opacity)))
            else:
                corrected_len_ratio = np.clip(obj.length / obj.bezier.curve.length,0,1)
                slider_segment = obj.bezier.segment(np.linspace(0,corrected_len_ratio,100))
                # print(slider_segment)
                for p in slider_segment:
                    slider_x = (p[0] + x_offset) * scale
                    slider_y = (p[1] + y_offset) * scale
                    draw.ellipse(xy=[(slider_x - radius, slider_y - radius), (slider_x + radius, slider_y + radius)],
                                 fill=(int(255//2 * opacity), 0, 0, 255))

                x_img = (obj.x + x_offset) * scale
                y_img = (obj.y + y_offset) * scale

                draw.ellipse(xy=[(x_img - radius, y_img - radius), (x_img + radius, y_img + radius)],
                             fill=(255, 0, 0, int(255 * opacity)))


        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA))

    video.release()

    print("Done")
