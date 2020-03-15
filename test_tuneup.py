""" Test Suite for tuneup module. """
import unittest
import timeit
from tuneup import find_duplicate_movies, profile


# Using the previous function to check performance
###################################################

def test_read_movies(src):
    """Returns a list of movie titles"""
    with open(src, 'r') as f:
        return f.read().splitlines()


def test_is_duplicate(title, movies):
    """returns True if title is within movies list"""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False


@profile
def test_find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list"""
    movies = test_read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if test_is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates

###################################################


class TestTuneUp(unittest.TestCase):
    """Tuneup test case."""

    def test_tuneup(self):
        initial_time = timeit.Timer(
            lambda: test_find_duplicate_movies('movies.txt')).timeit(number=1)
        performance_time = initial_time / 670
        my_time = timeit.Timer(lambda: find_duplicate_movies(
            'movies.txt')).timeit(number=1)
        failure_text = (
            "find_duplicates_movies took {:.3f} seconds, which it "
            "doesn't achieve at least a 670x improvement of performance "
            "({:.3f})".format(my_time, performance_time))
        self.assertTrue(my_time <= performance_time, failure_text)


if __name__ == '__main__':
    unittest.main()
