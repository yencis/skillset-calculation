import backend.api.osu_api as osu_api
import backend.api.util_io as util_io
import backend.src.Beatmap.BeatmapFileImport as beatmap_import
import backend.src.Beatmap.Beatmap as Beatmap
import backend.src.Beatmap.Object.Slider as Slider
import backend.src.Viewer.Render as Render
import random
import numpy as np
from PIL import Image, ImageDraw


def get_beatmap_ids(filename="top5000byplaycount.txt"):
    ids = []
    with open(filename, 'r') as f:
        while True:
            text = f.readline().strip()
            if text:
                ids.append(f.readline().strip())
            else:
                break
    return ids


def get_sliders(id_list):
    """
    Parse beatmaps, get useable sliders
    """

    nice_sliders = []

    for i in id_list:
        print(i)
        try:
            cur_beatmap = beatmap_import.import_beatmap_from_file(util_io.text_to_file(osu_api.OSUAPI.get_beatmap(i)))

            # find a fire slider
            for obj in cur_beatmap.hitObjects:
                if obj.is_slider() and (len(obj.control_points) > 20):
                    nice_sliders.append((obj, cur_beatmap.difficulty.cs))
                    print("Slider found")
                    break
        except:
            continue

    return nice_sliders


def run(difficulty="medium"):
    ids = get_beatmap_ids()
    if difficulty == "easy":
        ids = ids[:50]
    elif difficulty == "medium":
        ids = ids[:2000]
    else:
        ids = ids


    sliders = get_sliders(ids)

    if len(sliders) == 0:
        return

    print("Found this many sliders "+str(len(sliders)))

    rand_int = random.randint(0, len(sliders)-1)

    # rendering
    print(rand_int)


    slider,cs = sliders[rand_int]

    x = 512
    y = 384
    x_offset = 180
    y_offset = 72
    scale = 2
    dim = ((x + 2 * x_offset) * scale, (y + 2 * y_offset) * scale)
    radius = (54.4 - 4.48 * cs) * scale

    img = Image.new('RGB', dim, color='black')
    draw = ImageDraw.Draw(img, 'RGBA')
    Render.render_slider(draw, slider, 1, x_offset, y_offset, radius, scale)

    img.show()

run("easy")