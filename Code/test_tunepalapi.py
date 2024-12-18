from unittest import TestCase
from tunepalapi import TunePalAPI, Song


class TestTunePalAPI(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        # Initialize current page index to 0
        self.current_page_index = 0
        # Initialize TunePalAPI instance with a page size of 10
        self.music = TunePalAPI(page_size=10)
        # Initialize songs list from TunePalAPI class
        self.songs = TunePalAPI.songs

    def test_build_song_window(self):
        # Setting up TunePalAPI instance
        # Set current page index
        self.music.current_page_index = 0
        # Create a list of 100 songs
        song_list = [Song("title", "artist", "release_year") for _ in range(100)]
        # Calculate the expected song window
        first_index = self.music.current_page_index * self.music.page_size
        last_index = first_index + self.music.page_size
        expected_window = song_list[first_index:last_index]
        # Create the song window
        song_window = self.music._build_song_window(song_list)
        # Assert the equality of the expected and actual song windows
        self.assertEqual(song_window, expected_window)

    def test_build_song_window_with_higher_than_maximum_page_index(self):
        # Set the current page index to a value higher than the maximum allowed page index
        self.music.current_page_index = 8
        # Create a list of 70 songs
        song_list = [Song("title", "artist", "release_year") for _ in range(70)]
        # Assert that the _build_song_window method raises a ValueError
        self.assertRaises(ValueError, self.music._build_song_window, song_list)

    def test_build_song_window_with_small_song_list(self):
        # Test with a smaller song list
        self.music.current_page_index = 0
        # Create a list of 5 songs
        song_list = [Song("title", "artist", "release_year") for _ in range(5)]  # Small song list
        # Calculate the expected song window
        first_index = self.music.current_page_index * self.music.page_size
        last_index = first_index + self.music.page_size
        expected_window = song_list[first_index:last_index]
        # Create the song window
        song_window = self.music._build_song_window(song_list)
        # Assert the equality of the expected and actual song windows
        self.assertEqual(song_window, expected_window)

    def test_add_song(self):
        # Test adding a song
        length = len(self.music.songs)
        self.music.add_song("Independence Song", "National Artist", "1917")
        self.assertEqual(len(self.music.songs), length + 1)

    def test_get_songs(self):
        # Test getting songs
        songs = self.music.get_songs()
        self.assertEqual(len(songs), 10)

    def test_next_page(self):
        # Test to see if the current page index is incremented by 1
        self.music.current_page_index = 1
        self.music.next_page()
        self.assertEqual(self.music.current_page_index, 2)

    def test_previous_page(self):
        # Test to see if the current page index is decremented by 1
        self.music.current_page_index = 3
        self.music.previous_page()
        self.assertEqual(self.music.current_page_index, 2)

    def test_previous_page_not_going_to_negative(self):
        # Test to see if the current page index is decremented by 1 but doesn't go negative
        self.music.current_page_index = 0
        self.music.previous_page()
        self.assertEqual(self.music.current_page_index, 0)

    def test_set_page_size(self):
        # Test setting page size
        self.music.set_page_size(10)
        self.assertEqual(self.music.page_size, 10)

    def test_set_page_size_with_negative_numbers(self):
        # Test setting page size with negative numbers (should default to 1)
        self.music.set_page_size(-10)
        self.assertEqual(self.music.page_size, 1)

    def test_search(self):
        # Test searching for songs
        self.music.songs = self.songs
        # Set current page index
        self.music.current_page_index = 0
        # Search with a query that matches some songs
        result = self.music.search("Black")
        # Check if "Black" is in titles of songs returned in result
        self.assertTrue("Black" in song.title for song in result)

    def test_get_songs_since(self):
        # Test getting songs released since a certain year
        self.music.songs = self.songs
        # Set current page index
        self.music.current_page_index = 0
        # Get songs released since 1990
        result = self.music.get_songs_since("1990")
        # Check if all songs in result are released since 1990
        self.assertTrue(all(int(song.release_year) >= 1990 for song in result))

    def test_get_songs_since_with_invalid_release_year(self):
        # Test getting songs released since an invalid year
        self.music.songs = self.songs
        # Set current page index
        self.music.current_page_index = 0
        # Get songs released since 1990
        result = self.music.get_songs_since("1990")
        # Check if there are no songs released since before 1900 or after 2024
        self.assertFalse(all(int(song.release_year) >= 2024 for song in result))
        self.assertFalse(all(int(song.release_year) <= 1900 for song in result))
