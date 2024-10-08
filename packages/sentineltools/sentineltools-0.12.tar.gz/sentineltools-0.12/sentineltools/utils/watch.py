from dataclasses import dataclass, field
import time


@dataclass
class TimeMarker:
    mode: str = "start"
    time: float = 0
    elapsed: float = 0


@dataclass
class Track:
    running: bool = False
    times: list[TimeMarker] = field(default_factory=list)


class Watch:
    def __init__(self) -> None:
        self.tracks = {}

    def _get_track(self, track_name: str = "default") -> Track:
        if track_name in self.tracks:
            return self.tracks[track_name]
        else:
            track = Track(False, [])
            self.tracks[track_name] = track
            return track

    def lap(self, track_name: str = "default"):
        track: Track = self._get_track(track_name)
        track.running = True
        if len(track.times) == 0:
            track.times.append(TimeMarker(
                "lap", time.time(), 0))
        else:
            prev_marker = track.times[-1]
            new_time = time.time()
            track.times.append(TimeMarker(
                "lap",  new_time, new_time - prev_marker.time if prev_marker.mode != "stop" else 0))

    def start(self, track_name: str = "default"):
        track: Track = self._get_track(track_name)
        track.running = True
        track.times.append(TimeMarker("start", time.time(), 0))

    def stop(self, track_name: str = "default"):
        track: Track = self._get_track(track_name)
        track.running = False
        if len(track.times) == 0:
            track.times.append(TimeMarker(
                "stop", time.time(), 0))
        else:
            prev_marker = track.times[-1]
            new_time = time.time()
            track.times.append(TimeMarker(
                "stop",  new_time, new_time - prev_marker.time if prev_marker.mode != "stop" else 0))

    def total_elapsed(self, track_name: str = "default") -> float:
        track = self._get_track(track_name)
        total_time = sum(marker.elapsed for marker in track.times)

        if track.running and track.times:
            total_time += time.time() - track.times[-1].time

        return total_time

    def print_times(self) -> None:
        """
        Prints the total elapsed time for all tracks.
        """
        if not self.tracks:
            print("No tracks available.")
            return

        for track_name, track in self.tracks.items():
            total_time = self.total_elapsed(track_name)
            print(f"Track '{track_name}': {total_time:.2f} seconds")
