class DifficultyAttributes:
    def __init__(
        self,
        star_rating: float,
        mods: list[int],
        aim_difficulty: float,
        speed_difficulty: float,
        speed_note_count: float,
        flashlight_difficulty: float,
        slider_factor: float,
        approach_rate: float,
        overall_difficulty: float,
        drain_rate: float,
        max_combo: int,
        hit_circle_count: int,
        slider_count: int,
        spinner_count: int,
    ) -> None:
        self.mods = mods
        self.star_rating = star_rating
        self.max_combo = max_combo
        self.aim_difficulty = aim_difficulty
        self.speed_difficulty = speed_difficulty
        self.speed_note_count = speed_note_count
        self.flashlight_difficulty = flashlight_difficulty
        self.slider_factor = slider_factor
        self.approach_rate = approach_rate
        self.overall_difficulty = overall_difficulty
        self.drain_rate = drain_rate
        self.hit_circle_count = hit_circle_count
        self.slider_count = slider_count
        self.spinner_count = spinner_count
