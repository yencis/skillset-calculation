from DifficultyAttributes import DifficultyAttributes
from DifficultyObject import DifficultyObject
from Skills.Aim import Aim
from Skills.Speed import Speed
from Skills.Flashlight import Flashlight
from Beatmap.Beatmap import Beatmap
from Beatmap.Object.HitCircle import HitCircle
from Beatmap.Object.Slider import Slider
from Beatmap.Object.Spinner import Spinner
import math


class DifficultyCalculator:
    DIFFICULTY_MULTIPLIER = 0.0675

    def __init__(self, beatmap: Beatmap, mods: list[int], clock_rate: float) -> None:
        self.beatmap = beatmap
        self.mods = mods
        self.clock_rate = clock_rate

    def calculate_difficulty(self):
        self.preprocess_mods()

        skills = self.create_skills()
        for object in self.create_difficulty_objects():
            for skill in skills:
                skill.process(object)
        return self.create_difficulty_attributes(skills)

    def preprocess_mods(self):
        pass

    def create_skills(self):
        return [
            Aim(self.mods, True),
            Aim(self.mods, False),
            Speed(self.mods),
            Flashlight(self.mods),
        ]

    def create_difficulty_objects(self):
        objects: list[DifficultyObject] = []

        for i in range(1, len(self.beatmap.hitObjects)):
            lastlast = self.beatmap.hitObjects[i - 2] if i > 1 else None
            objects.append(
                DifficultyObject(
                    objects=objects,
                    index=len(objects),
                    hit_object=self.beatmap.hitObjects[i],
                    last_object=self.beatmap.hitObjects[i - 1],
                    last_last_object=lastlast,
                    clock_rate=self.clock_rate,
                )
            )

        return objects

    def create_difficulty_attributes(self, skills: list[int]):
        aim_rating = math.sqrt(skills[0].difficulty_value() * self.DIFFICULTY_MULTIPLIER)
        aim_rating_no_sliders = math.sqrt(skills[1].difficulty_value() * self.DIFFICULTY_MULTIPLIER)
        speed_rating = math.sqrt(skills[2].difficulty_value() * self.DIFFICULTY_MULTIPLIER)
        speed_notes = skills[2].relevant_note_count()
        flashlight_rating = math.sqrt(skills[3].difficulty_value() * self.DIFFICULTY_MULTIPLIER)

        slider_factor = aim_rating_no_sliders / aim_rating if aim_rating > 0 else 1

        # TODO: touchscreen/relax check, need to define mod spec numbers

        base_aim_performance = (5 * max(1, aim_rating / 0.0675) - 4) ** 3 / 100000
        base_speed_performance = (5 * max(1, speed_rating / 0.0675) - 4) ** 3 / 100000
        base_flashlight_performance = 0

        # TODO: flashlight calculation

        base_performance = (
            base_aim_performance**1.1
            + base_speed_performance**1.1
            + base_flashlight_performance**1.1
        ) ** (1.0 / 1.1)

        # TODO: magic number here
        star_rating = (
            (
                (1.14 ** (1.0 / 3))
                * 0.027
                * ((100000 / (2 ** (1.0 / 1.1))) ** (1.0 / 3) * base_performance)
                + 4
            )
            if base_performance > 0.00001
            else 0
        )

        # TODO: preempt is re-calculated here?
        drain_rate = self.beatmap.difficulty.hp
        max_combo = len(self.beatmap.hitObjects)
        hit_circle_count = sum(isinstance(x, HitCircle) for x in self.beatmap.hitObjects)
        slider_count = sum(isinstance(x, Slider) for x in self.beatmap.hitObjects)
        spinner_count = sum(isinstance(x, Spinner) for x in self.beatmap.hitObjects)

        attributes = DifficultyAttributes(
            star_rating=None,
            mods=None,
            aim_difficulty=None,
            speed_difficulty=None,
            speed_note_count=None,
            flashlight_difficulty=None,
            slider_factor=None,
            approach_rate=None,
            overall_difficulty=None,
            drain_rate=None,
            max_combo=None,
            hit_circle_count=None,
            slider_count=None,
            spinner_count=None,
        )

        return attributes
