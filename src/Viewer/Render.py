import numpy as np
from PIL import Image, ImageDraw
import cv2


# 512 x 384 with 180 x 72 border (osu pixel size)

def render_slider(draw, obj, opacity, x_offset, y_offset, radius, scale):
    """
    Render a slider. Not too proud of this function
    """
    """: Old slider code for creation through ellipses
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
                    """

    """"""
    # more efficient slider code built from linear piecewise interpolation
    # need to go through less points

    lin_points = obj.bezier.linear_points

    last_point = [None, None]
    _l_p = None  # storing last point without coord conversion

    # cap short slider
    corrected_len_ratio = np.clip(obj.length / obj.bezier.curve.length, 0, 1)
    corrected_maximum_point = np.ndarray.flatten(obj.bezier.evaluate(corrected_len_ratio))

    running_length = 0

    # print(lin_points)

    for point in lin_points:
        if not last_point[0]:
            last_point = (point + np.array([x_offset, y_offset])) * scale
            _l_p = point
        else:
            running_length += np.linalg.norm(_l_p - point)

            # if slider is about to exceed object length, end slider rendering and replace next point with
            # the correct max endpoint
            if running_length >= obj.length:
                point = corrected_maximum_point

            cur_point = (point + np.array([x_offset, y_offset])) * scale
            draw.ellipse(
                xy=[(cur_point[0] - radius, cur_point[1] - radius), (cur_point[0] + radius, cur_point[1] + radius)],
                fill=(int(255 // 2 * opacity), 0, 0, 255))
            draw.line(list(np.concatenate((last_point, cur_point), axis=None)),
                      fill=(int(255 // 2 * opacity), 0, 0, 255), width=int(radius) * 2)
            last_point = cur_point
            _l_p = point

            if running_length >= obj.length:
                break

    # end array with circle at last point

    draw.ellipse(
        xy=[(last_point[0] - radius, last_point[1] - radius), (last_point[0] + radius, last_point[1] + radius)],
        fill=(int(255 // 2 * opacity), 0, 0, 255))

    # draw a normal circle for sliderhead

    x_img = (obj.x + x_offset) * scale
    y_img = (obj.y + y_offset) * scale

    draw.ellipse(xy=[(x_img - radius, y_img - radius), (x_img + radius, y_img + radius)],
                 fill=(255, 0, 0, int(255 * opacity)))


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
    video = cv2.VideoWriter("output_2.mp4", fourcc, 15, dim)

    print("Total beatmap duration: " + str(beatmap.get_duration()))

    slider_buffer = []  # store active sliders and end times
    temp = []  # sliders to be added to active sliders next iteration

    spinner_buffer = []
    spinner_temp = []

    step = 66.666666666667

    for i in np.arange(0, beatmap.get_duration(), step):  # i in milliseconds, 60 frames per second

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

        for slider in slider_buffer:
            if i <= slider.time + slider.travel_time():
                temp.append(slider)

        slider_buffer = temp
        temp = []

        for spinner in spinner_buffer:
            if i <= spinner.endTime:
                spinner_temp.append(spinner)

        spinner_buffer = spinner_temp
        spinner_temp = []

        # render old spinners first so they are in the back

        for spinner in spinner_buffer:  # realistically like 1 spinner

            x_img = (spinner.x + x_offset) * scale
            y_img = (spinner.y + y_offset) * scale

            draw.ellipse(xy=[(x_img - y, y_img - y), (x_img + y, y_img + y)],
                         fill=(0, 255, 0, int(255 // 2)))



        for obj in objects[::-1]:  # iterate in reverse for stacking
            opacity = beatmap.get_opacity_of_hitobject(obj, i)

            # process coordinates

            if obj.is_slider():

                render_slider(draw, obj, opacity, x_offset, y_offset, radius, scale)
                if obj.time < i + step:  # if slider is hit in between this frame and next frame
                    temp.append(obj)

            elif obj.is_spinner():

                # render spinner

                x_img = (obj.x + x_offset) * scale
                y_img = (obj.y + y_offset) * scale

                draw.ellipse(xy=[(x_img - y, y_img - y), (x_img + y, y_img + y)],
                             fill=(0, 255, 0, int(255//2 * opacity)))
                if obj.time < i + step:  # if spinner is hit in between this frame and next frame
                    spinner_temp.append(obj)


            else:

                x_img = (obj.x + x_offset) * scale
                y_img = (obj.y + y_offset) * scale

                draw.ellipse(xy=[(x_img - radius, y_img - radius), (x_img + radius, y_img + radius)],
                             fill=(255, 0, 0, int(255 * opacity)))


        # remove any sliders from active sliders that have already finished



        # render any active sliders AFTER the hitobject time
        # this is not rendered in order of time begun and may cause stacking issues

        for slider in slider_buffer:
            if i > slider.time:
                render_slider(draw, slider, 1, x_offset, y_offset, radius, scale)

        # draw sliderball

        if len(slider_buffer) > 0:
            active_slider = slider_buffer[0]

            slider_ball_point = active_slider.slider_at_time(i)

            if slider_ball_point[0]:  # if slider ball point is not None (this occurs if the slider has just been
                # added but actually begins next step)

                x_img = (slider_ball_point[0] + x_offset) * scale
                y_img = (slider_ball_point[1] + y_offset) * scale

                draw.ellipse(xy=[(x_img - radius, y_img - radius), (x_img + radius, y_img + radius)],
                             fill=(255,255,255,255))

        video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA))

    video.release()

    print("Done")
