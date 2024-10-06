#!/usr/bin/env python3
# coding=utf-8

import curses
import render
from notify import notify
from time import sleep

ENCODING = "utf-8"


def last_key(stdscr):
    """Show last pressed key chars at the bottom-right corner."""
    h, w = stdscr.getmaxyx()
    win = stdscr.derwin(h - 1, w - 5)
    while True:
        c = str(win.get_wch())
        cs = f" {c[1:]}"  # fix: slice first character which repeats twice
        win.insstr(0, 0, cs)
        if c == "q":
            break


def main():
    stdscr = curses.initscr()    # initialize screen
    #  curses.curs_set(0)           # Turn off cursor
    #  curses.use_default_colors()  # terminal colors & transparency

    #  window = render.Window(stdscr)
    #  notify(render.Window(stdscr).cols, render.Window(stdscr).rows)
    # get screen size
    screen_h_rows, screen_w_cols = stdscr.getmaxyx()
    #  stdscr.refresh()

    prompt = "input:"
    curses.echo()
    input = stdscr.getstr(0, len(prompt) + 1)
    curses.noecho()
    #  last_key(stdscr)

    # curses.napms(5000)
    #  stdscr.getch()      # wait for a key press to exit
    #  curses.curs_set(1)  # Turn cursor back on
    curses.endwin()
    decoded = str(input, ENCODING).strip()
    #  decoded = str(input.decode(encoding=ENCODING)).strip()
    #  decoded = str(input).strip()
    #  decoded = input.decode(encoding=ENCODING)
    print(input)
    print(f"'{decoded}'")


main()
