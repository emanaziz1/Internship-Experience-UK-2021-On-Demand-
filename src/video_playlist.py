"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_name: str, playlist_videos: list):
        """Video constructor."""
        self._playlist_name = playlist_name
        self._playlist_videos = playlist_videos

    @property
    def playlist_name(self) -> str:
        return self._playlist_name

    @property
    def playlist_videos(self) -> list:
        return self._playlist_videos