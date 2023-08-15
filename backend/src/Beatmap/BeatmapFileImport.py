from Beatmap import Beatmap
from Beatmap.Object.TimingPoint import TimingPoint
from Beatmap.Object.Slider import Slider
from Beatmap.Object.HitObject import HitObject
from Beatmap.Object.HitCircle import HitCircle

"""
Import hitobjects from .osu file
"""


def is_slider(obj_type):
    return obj_type & 2 == 2


def import_beatmap(filename):
    with open(filename, 'r') as f:
        file_format = f.readline()
        print("File format " + file_format)

        # skip lines until we reach beatmap difficulty

        while True:
            if f.readline() == "[Difficulty]\n":
                break

        difficulty_settings = {}

        # process each line as a difficulty setting until reaching a newline

        while True:

            line = f.readline()

            if line == "\n":
                break

            setting_name = line.split(":")[0]
            setting_value = float(line.split(":")[1])

            difficulty_settings[setting_name] = setting_value

        hp_drain_rate = difficulty_settings["HPDrainRate"]
        circle_size = difficulty_settings["CircleSize"]
        overall_difficulty = difficulty_settings["OverallDifficulty"]
        approach_rate = difficulty_settings[
            "ApproachRate"] if "ApproachRate" in difficulty_settings else overall_difficulty
        slider_multiplier = difficulty_settings["SliderMultiplier"]
        slider_tick_rate = difficulty_settings["SliderTickRate"]

        current_beatmap = Beatmap.Beatmap(hp_drain_rate, circle_size, overall_difficulty, approach_rate, slider_multiplier,
                                  slider_tick_rate)

        # skip lines until we reach timing points

        while True:
            if f.readline() == "[TimingPoints]\n":
                break

        timing_points = []

        # process each line as a unique timing point until reaching a newline

        while True:

            line = f.readline()

            if line == "\n":
                break

            timing_points.append(TimingPoint.from_text(line))

        current_beatmap.timingPoints = timing_points

        assert current_beatmap.check_timings()

        # skip lines until we reach hitobjects

        while True:
            if f.readline() == "[HitObjects]\n":
                break

        hitobjects = []

        # process each line as a unique hitobject until reaching newline

        while True:

            line = f.readline()

            if line == "\n" or line == "":
                break

            csv = line.split(",")



            if is_slider(int(csv[3])):
                hitobjects.append(Slider.from_text(line))
            else:
                hitobjects.append(HitCircle.from_text(line))

        current_beatmap.hitObjects = hitobjects

    return current_beatmap
