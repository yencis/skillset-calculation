from DifficultyAttributes import DifficultyAttributes
from DifficultyObject import DifficultyObject
from Skills.Aim import Aim
from Skills.Speed import Speed
from Skills.Flashlight import Flashlight
from Beatmap.Beatmap import Beatmap
from Beatmap.Object.HitCircle import HitCircle
from Beatmap.Object.Slider import Slider
from Beatmap.Object.Spinner import Spinner
from Mods import Mods
import math


class DifficultyCalculator:
    DIFFICULTY_MULTIPLIER = 0.0675

    def __init__(self, beatmap: Beatmap, mods: list[Mods], clock_rate: float) -> None:
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

    def preprocess_mods(self):  # TODO: HOW does this work?
        if Mods.DOUBLETIME in self.mods:
            clock_rate *= 1.5
        if Mods.HARDROCK in self.mods:
            self.beatmap.difficulty.cs *= 1.3
            self.beatmap.difficulty.ar *= 1.4
            self.beatmap.difficulty.hp *= 1.4
            self.beatmap.difficulty.od *= 1.4
        if Mods.HALFTIME in self.mods:
            clock_rate *= 0.75
        if Mods.EASY in self.mods:
            self.beatmap.difficulty.cs *= 0.5
            self.beatmap.difficulty.ar *= 0.5
            self.beatmap.difficulty.hp *= 0.5
            self.beatmap.difficulty.od *= 0.5

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

        # TODO: magic number 1.14 multiplier in here
        star_rating = (
            (
                (1.14 ** (1.0 / 3))
                * 0.027
                * (((100000 / (2 ** (1.0 / 1.1))) ** (1.0 / 3) * base_performance) + 4)
            )
            if base_performance > 0.00001
            else 0
        )

        max_combo = len(self.beatmap.hitObjects)  # TODO: this is INVALID for slider ticks

        attributes = DifficultyAttributes(
            star_rating=star_rating,
            mods=self.mods,
            aim_difficulty=aim_rating,
            speed_difficulty=speed_rating,
            speed_note_count=speed_notes,
            flashlight_difficulty=flashlight_rating,
            slider_factor=slider_factor,
            approach_rate=self.beatmap.difficulty.ar,
            overall_difficulty=self.beatmap.difficulty.od,
            drain_rate=self.beatmap.difficulty.hp,
            max_combo=max_combo,
            hit_circle_count=sum(isinstance(x, HitCircle) for x in self.beatmap.hitObjects),
            slider_count=sum(isinstance(x, Slider) for x in self.beatmap.hitObjects),
            spinner_count=sum(isinstance(x, Spinner) for x in self.beatmap.hitObjects),
        )

        return attributes
