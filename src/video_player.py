"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.current_video = []
        self.pausing_video = False
        self.video_playlist = {}
        self.flag_videos = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos_object = self._video_library.get_all_videos()
        sorted_video_list = []
        for video_object in all_videos_object:
            if video_object.video_id in self.flag_videos.keys():
                sorted_video_list.append(video_object.title + " (" + video_object.video_id + ") " + str(list(video_object.tags)).replace(",","").replace("'", "") +" - FLAGGED (reason: "+self.flag_videos[video_object.video_id]+")")

            else:
                sorted_video_list.append(video_object.title + " ("+video_object.video_id+") " + str(list(video_object.tags)).replace(",","").replace("'",""))
        sorted_video_list.sort()
        print("Here's a list of all available videos:", *sorted_video_list, sep= "\n\t")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        if self._video_library.get_video(video_id) == None:
            print("Cannot play video: Video does not exist")
        elif video_id in self.flag_videos.keys():
            print("Cannot play video: Video is currently flagged (reason:" , self.flag_videos[video_id]+")")
        elif self.current_video == []:
            self.current_video = [video_id]
            print("Playing video:" , self._video_library.get_video(video_id).title)
            self.pausing_video = False
        else:
            self.stop_video()
            self.current_video = [video_id]
            print("Playing video:", self._video_library.get_video(video_id).title)
            self.pausing_video = False

    def stop_video(self):
        """Stops the current video."""
        if self.current_video == []:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video:", self._video_library.get_video(self.current_video[0]).title)
            self.current_video = []

    def play_random_video(self):
        """Plays a random video from the video library."""
        flag = True
        all_video_object = self._video_library.get_all_videos()
        while flag == True:
            random_number = random.randint(0, 4)
            video_object = all_video_object[random_number]
            if len(self.flag_videos.keys()) == len(all_video_object):
                print("No videos available")
                break
            elif video_object.video_id in self.flag_videos.keys():
                continue
            else:
                self.play_video(video_object.video_id)
                flag = False

    def pause_video(self):
        """Pauses the current video."""
        if self.current_video == []:
            print("Cannot pause video: No video is currently playing")
        elif self.pausing_video == False:
            print("Pausing video:", self._video_library.get_video(self.current_video[0]).title)
            self.pausing_video = True
        else:
            print("Video already paused:", self._video_library.get_video(self.current_video[0]).title)

    def continue_video(self):
        """Resumes playing the current video."""
        if self.current_video == []:
            print("Cannot continue video: No video is currently playing")
        elif self.pausing_video == True:
            print("Continuing video:", self._video_library.get_video(self.current_video[0]).title)
            self.pausing_video = False
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self.current_video == []:
            print("No video is currently playing")
        elif self.pausing_video == True:
            object = self._video_library.get_video(self.current_video[0])
            print("Currently playing:", object.title + " ("+object.video_id+") " + str(list(object.tags)).replace(",","").replace("'",""), "- PAUSED")
        else:
            object = self._video_library.get_video(self.current_video[0])
            print("Currently playing:", object.title + " ("+object.video_id+") " + str(list(object.tags)).replace(",","").replace("'",""))

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_lower = playlist_name.lower()
        if playlist_name_lower in self.video_playlist.keys():
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            print("Successfully created new playlist:", playlist_name)
            self.video_playlist[playlist_name_lower] = Playlist(playlist_name,[])

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist_name_lower = playlist_name.lower()
        if playlist_name_lower not in self.video_playlist.keys():
            print("Cannot add video to", playlist_name +": Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print("Cannot add video to", playlist_name +": Video does not exist")
        else:
            previous_videos_stored = self.video_playlist[playlist_name_lower].playlist_videos
            if video_id in self.flag_videos.keys():
                print("Cannot add video to", playlist_name+": Video is currently flagged (reason:", self.flag_videos[video_id]+")")
            elif video_id in previous_videos_stored:
                print("Cannot add video to", playlist_name + ": Video already added")
            else:
                previous_videos_stored = previous_videos_stored + [video_id]
                self.video_playlist[playlist_name_lower] = Playlist(playlist_name,previous_videos_stored)
                print("Added video to", playlist_name +":",self._video_library.get_video(video_id).title)


    def show_all_playlists(self):
        """Display all playlists."""
        sorted_objects = []
        if len(self.video_playlist) == 0:
            print("No playlists exist yet")
        else:
            objects = list(self.video_playlist.values())
            print("Showing all playlists:")
            for object in objects:
                sorted_objects.append(object.playlist_name)
            sorted_objects.sort()
            print("    ", end= "")
            print(*sorted_objects,sep="\n\t" )

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_lower = playlist_name.lower()
        if playlist_name_lower in self.video_playlist.keys():
            videos_in_playlist = self.video_playlist[playlist_name_lower].playlist_videos
            if len(videos_in_playlist) == 0:
                print("Showing playlist:" , playlist_name + "\n\t" + "No videos here yet")
            else:
                print("Showing playlist:", playlist_name)
                for video in videos_in_playlist:
                    object = self._video_library.get_video(video)
                    if object.video_id in self.flag_videos.keys():
                        print("\t" + object.title + " (" + object.video_id + ") " + str(list(object.tags)).replace(",","").replace("'", "") +" - FLAGGED (reason:", self.flag_videos[object.video_id]+")")
                    else:
                        print("\t" + object.title + " (" + object.video_id + ") " + str(list(object.tags)).replace(",", "").replace("'", ""))
        else:
            print("Cannot show playlist", playlist_name +": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_name_lower = playlist_name.lower()
        if playlist_name_lower not in self.video_playlist.keys():
            print("Cannot remove video from", playlist_name + ": Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print("Cannot remove video from", playlist_name + ": Video does not exist")
        else:
            previous_videos_stored = self.video_playlist[playlist_name_lower].playlist_videos
            if video_id in previous_videos_stored:
                previous_videos_stored.remove(video_id)
                self.video_playlist[playlist_name_lower] = Playlist(playlist_name, previous_videos_stored)
                print("Removed video from", playlist_name + ":", self._video_library.get_video(video_id).title)
            else:
                print("Cannot remove video from", playlist_name + ": Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_lower = playlist_name.lower()
        if playlist_name_lower not in self.video_playlist.keys():
            print("Cannot clear playlist", playlist_name + ": Playlist does not exist")
        else:
            self.video_playlist[playlist_name_lower] = Playlist(playlist_name,[])
            print("Successfully removed all videos from", playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_lower = playlist_name.lower()
        if playlist_name_lower not in self.video_playlist.keys():
            print("Cannot delete playlist" , playlist_name + ": Playlist does not exist")
        else:
            self.video_playlist.pop(playlist_name_lower)
            print("Deleted playlist:", playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        video_objects = self._video_library.get_all_videos()
        videos_related = []
        for object in video_objects:
            object_title_lowered = object.title.lower()
            if object.video_id in self.flag_videos.keys():
                continue
            elif object_title_lowered.count(search_term.lower()):
                videos_related.append(object.video_id)
        if len(videos_related) == 0:
            print("No search results for", search_term)
        else:
            videos_related.sort()
            print("Here are the results for", search_term + ":")
            index = 1
            for object in videos_related:
                object = self._video_library.get_video(object)
                print("   ", str(index) + ")",object.title ,"("+object.video_id+") "+ str(list(object.tags)).replace(",","").replace("'",""))
                index+=1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            answer = input()
            if answer.isdigit():
                if 0 < int(answer) <= len(videos_related):
                    self.play_video(videos_related[int(answer)-1])


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        video_objects = self._video_library.get_all_videos()
        video_tag_lowered = video_tag.lower()
        videos_related = []
        for object in video_objects:
            video_tags = str(object.tags)
            if object.video_id in self.flag_videos.keys():
                continue
            elif video_tags.count(video_tag_lowered) > 0:
                videos_related.append(object.video_id)
        if len(videos_related) == 0:
            print("No search results for", video_tag)
        else:
            videos_related.sort()
            print("Here are the results for", video_tag + ":")
            index = 1
            for object in videos_related:
                object = self._video_library.get_video(object)
                print("   ", str(index) + ")",
                      object.title + " (" + object.video_id + ") " + str(list(object.tags)).replace(",", "").replace("'", ""))
                index += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            answer = input()
            if answer.isdigit():
                if 0 < int(answer) <= len(videos_related):
                    self.play_video(videos_related[int(answer) - 1])

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if self._video_library.get_video(video_id) == None:
            print("Cannot flag video: Video does not exist")
        elif video_id in self.flag_videos.keys():
            print("Cannot flag video: Video is already flagged")
        else:
            if video_id in self.current_video:
                self.stop_video()
            print("Successfully flagged video:",self._video_library.get_video(video_id).title, "(reason:", flag_reason +")")
            self.flag_videos[video_id] = flag_reason


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        if self._video_library.get_video(video_id) == None:
            print("Cannot remove flag from video: Video does not exist")
        elif video_id in self.flag_videos.keys():
            print("Successfully removed flag from video:", self._video_library.get_video(video_id).title)
            self.flag_videos.pop(video_id)
        else:
            print("Cannot remove flag from video: Video is not flagged")