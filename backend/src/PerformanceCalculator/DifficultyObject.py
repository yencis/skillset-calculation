from Beatmap.Object.HitObject import HitObject
from Beatmap.Object.Slider import Slider


class DifficultyObject:
    NORMALIZED_RADIUS = 50
    MIN_DELTA_TIME = 25
    MAX_SLIDER_RADIUS = NORMALIZED_RADIUS * 2.4
    ASSUMED_SLIDER_RADIUS = NORMALIZED_RADIUS * 1.8

    def __init__(
        self,
        difficulty_objects: list[HitObject],
        index: int,
        hit_object: HitObject,
        last_object: HitObject,
        last_last_object: HitObject | None,
        clock_rate: float,  # this is 1 for normal speed playback
    ) -> None:
        self.difficulty_objects = difficulty_objects
        self.index = index
        self.hit_object = hit_object
        self.last_object = last_object
        self.last_last_object = last_last_object
        self.delta_time = (self.hit_object.time - self.last_object.time) / clock_rate
        self.start_time = self.hit_object.time / clock_rate
        self.end_time = None  # TODO: need get_end_time() for hitobjects
        self.strain_time = max(self.MIN_DELTA_TIME, self.delta_time)
        self.lazy_jump_distance = None
        self.minimum_jump_distance = None
        self.minimum_jump_time = None
        self.travel_distance = None
        self.travel_time = None
        self.angle: float | None = None
        self.hit_window_great = (
            None if isinstance(hit_object, Slider) else None
        )  # TODO: need hit windows for head of slider and circles

    def previous(self, backwards_index: int):
        try:
            return self.difficulty_objects[self.index - (backwards_index + 1)]
        except IndexError:
            return None

    def next(self, forwards_index: int):
        try:
            return self.difficulty_objects[self.index + (forwards_index + 1)]
        except IndexError:
            return None

    def opacity_at(self, time: float, hidden: bool):
        if time > self.hit_object.time:
            return 0.0

    def set_distances(self, clock_rate: float):
        pass

    def compute_slider_cursor_position(self, slider: Slider):
        pass

    def get_end_cursor_position(self, hit_object: HitObject):
        pass
