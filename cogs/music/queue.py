from random import randint

class Queue:
    def __init__(self, max_length : int = None):
        self.tracks : list[dict] = []
        self.__max_length : int = max_length

    def add_track_start(self, track : dict):
        self.tracks : list[dict] = [track] + self.tracks

    def add_track_end(self, track : dict):
        self.tracks.append(track)
        if self.__max_length is not None:
            self.tracks[-self.__max_length:]
    
    def pop_first_track(self) -> dict:
        if len(self.tracks) == 0:
            return None
        
        track : dict = self.tracks[0]
        del self.tracks[0]

        return track

    def pop_last_track(self) -> dict:
        if len(self.tracks) == 0:
            return None
        
        track : dict = self.tracks[-1]
        del self.tracks[-1]

        return track
    
    def get_queue_length(self) -> int:
        return len(self.tracks)
    
    def is_empty(self) -> bool:
        return self.get_queue_length() == 0
    
    def reset(self):
        self.tracks : list[dict] = []

    def shuffle(self):
        shuffled_tracks : list[dict] = []

        while len(self.tracks) > 0:
            index : int = randint(0, len(self.tracks) - 1)
            shuffled_tracks.append(self.tracks[index])
            del self.tracks[index]

        self.tracks : list[dict] = shuffled_tracks