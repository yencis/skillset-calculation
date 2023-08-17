from Beatmap import Beatmap
from Object.TimingPoint import TimingPoint
from Object.Slider import Slider
from Object.HitObject import HitObject
from Object.HitCircle import HitCircle
from Object.Spinner import Spinner

"""
Import hitobjects from .osu file
"""


def is_slider(obj_type):
    return obj_type & 2 == 2

def is_spinner(obj_type):
    return obj_type & 8 == 8


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

        current_beatmap = Beatmap(hp_drain_rate, circle_size, overall_difficulty, approach_rate,
                                          slider_multiplier,
                                          slider_tick_rate)

        # skip lines until we reach timing points

        while True:
            if f.readline() == "[TimingPoints]\n":
                break

        timing_points = []
        red_timing_points = []

        # process each line as a unique timing point until reaching a newline

        while True:

            line = f.readline()

            if line == "\n":
                break

            timing_points.append(TimingPoint.from_text(line))
            if not timing_points[-1].is_inherited():
                red_timing_points.append(timing_points[-1])

        current_beatmap.timingPoints = timing_points
        current_beatmap.redTimingPoints = red_timing_points

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

                # check sv at this moment
                slider_obj = Slider.from_text(line)
                slider_velocity = current_beatmap.get_sv_at(slider_obj.time)
                slider_obj.set_sv(slider_velocity)
                hitobjects.append(slider_obj)
            elif is_spinner(int(csv[3])):
                hitobjects.append(Spinner.from_text(line))
            else:
                hitobjects.append(HitCircle.from_text(line))

        current_beatmap.hitObjects = hitobjects

    return current_beatmap

