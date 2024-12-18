from typing import List
import csv


class Song:
    title: str = ''
    artist: str = ''
    release_year: str = ''

    def __init__(self, title: str, artist: str, release_year: str):
        # Initialize Song object with title, artist, and release year
        self.title = title
        self.artist = artist
        self.release_year = release_year


class TunePalAPI:
    songs: List[Song] = []  # holds all songs available from this API
    page_size: int  # allows the user to decide how many songs are returned per page
    current_page_index: int

    def __init__(self, page_size=None):
        # Initialize TunePalAPI instance with given page size and load songs from CSV
        self.page_size = page_size
        self.current_page_index = 0
        with open('songlist.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = row['Song Clean']
                artist = row['ARTIST CLEAN']
                release_year = row['Release Year']
                self.songs.append(Song(title, artist, release_year))

    def _build_song_window(self, song_list: List[Song]):
        # Takes a list of songs and returns a smaller window using the current_page_index and page_size
        first_index = self.current_page_index * self.page_size
        last_index = first_index + self.page_size
        if self.current_page_index < len(song_list) / self.page_size:
            return song_list[first_index:last_index]
        elif self.current_page_index == 0 and len(song_list) < self.page_size:
            return song_list[first_index:]
        else:
            raise ValueError("Page index out of range")

    def add_song(self, title: str, artist: str, release_year: str):
        # Adds a song if it isn't already in the list
        songlist = self.search(title)
        for song in songlist:
            if song.title == title and song.artist == artist and song.release_year == release_year:
                return
        self.songs.append(Song(artist, title, release_year))

    def get_songs(self):
        # Returns a page of songs, use next_page and previous_page to change the window
        return self._build_song_window(self.songs)

    def next_page(self):
        # Moves to the next page
        self.current_page_index = self.current_page_index + 1

    def previous_page(self):
        # Moves to the previous page
        self.current_page_index = self.current_page_index - 1
        # Ensures that the current_page_index doesn't go below 0
        self.current_page_index = max(0, self.current_page_index)

    def set_page_size(self, page_size: int):
        # Sets the page size parameter, controlling how many songs are returned
        self.page_size = page_size
        # Ensures that the page_size is never less than 1
        self.page_size = max(1, self.page_size)

    def search(self, starts_with_query: str):
        # Matches any songs whose title or artist starts with the query provided
        hits = []
        for song in self.songs:
            if song.title.startswith(starts_with_query) or song.artist.startswith(starts_with_query):
                hits.append(song)
        return self._build_song_window(hits)

    def get_songs_since(self, release_year: str):
        # Filters out old-person music, returning songs released since a certain date
        hits = []
        for song in self.songs:
            if song.release_year >= release_year:
                hits.append(song)
        if not hits:
            raise ValueError("No songs found since " + release_year)
        return self._build_song_window(hits)
