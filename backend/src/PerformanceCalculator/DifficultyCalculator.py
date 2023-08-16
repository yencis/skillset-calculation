from DifficultyAttributes import DifficultyAttributes
from DifficultyObject import DifficultyObject
from Skills.Aim import Aim
from Skills.Speed import Speed
from Skills.Flashlight import Flashlight
from Beatmap.Beatmap import Beatmap


class DifficultyCalculator:
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

        return objects

    def create_difficulty_attributes(self, skills: list[int]):
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
