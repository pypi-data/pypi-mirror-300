"""
ansiparser.api
~~~~~~~~~~~~~~

This module implements the ansiparser API.
"""

from collections import deque

from . import screen_parser


def new_screen() -> screen_parser.ScreenParser:
    """Initialize new  parser for screen """

    return screen_parser.ScreenParser()


def from_inter_converted(parsed_screen: deque) -> screen_parser.ScreenParser:
    """Initialize from old inter_converted."""

    screen_parser_class = screen_parser.ScreenParser()
    screen_parser_class.from_parsed_screen(parsed_screen)

    return screen_parser_class
