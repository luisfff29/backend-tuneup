#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment"""

__author__ = "luisfff29"

import cProfile
import pstats
import functools
import timeit
import io
import argparse


def profile(func):
    """A function that can be used as a decorator to measure performance"""
    # You need to understand how decorators are constructed and used.
    # Be sure to review the lesson material on decorators, they are used
    # extensively in Django and Flask.
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        function = func(*args, **kwargs)
        pr.disable()
        s = io.BytesIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print s.getvalue()
        return function

    return decorator


def read_movies(src):
    """Returns a list of movie titles"""
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """returns True if title is within movies list"""
    if title in movies:
        return True


def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list"""
    movies = read_movies(src)
    movies.sort()
    duplicates = []
    for i, movie in enumerate(movies[:-1]):
        if movie == movies[i+1]:
            duplicates.append(movie)
    return duplicates


def timeit_helper(num=5):
    """Part A:  Obtain some profiling measurements using timeit"""
    print('Printing the best time...')
    t = timeit.Timer(stmt="find_duplicate_movies('movies.txt')",
                     setup='from __main__ import find_duplicate_movies')
    result = t.repeat(repeat=7, number=num)
    print('\tBest time across {} repeats of {} runs per repeat: {} sec'.format(
        len(result), num, min(result)))
    print ''


def main(src='movies.txt'):
    """Computes a list of duplicate movie entries"""
    # Create parser for Part A
    parser = argparse.ArgumentParser(description="Part A")
    parser.add_argument(
        '--partA', help='Print the best time for part A', action='store_true')
    args = parser.parse_args()
    # Call function when '--partA' is applied
    if args.partA:
        timeit_helper()

    # Apply decorator to the function
    find_duplicate_movies_decorated = profile(find_duplicate_movies)
    result = find_duplicate_movies_decorated(src)
    print('Reading file: {}'.format(src))
    print('Found {} duplicate movies:'.format(len(result)))
    print('\n'.join(result))


if __name__ == '__main__':
    main()
