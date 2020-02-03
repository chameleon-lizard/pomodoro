# Pomodoro
A simple python pomodoro timer. I was bored and my code sucks.

## Dependencies
Pomodoro sends notifications using libnotify. Most of mere mortals that use Gnome, KDE, XFCE and any other DE are covered, but if you are using some kind of a WM (like i3wm or whatever else), you have to make sure that you have libnotify and a notification server installed and running. I, personally, prefer [dunst](https://github.com/dunst-project/dunst), but you can read all about notifications on [ArchWiki](https://wiki.archlinux.org/index.php/Desktop_notifications).

## Installation:
Currently you just clone the repo and run the script with python. Nothing fancy yet.

## Usage:
Pomodoro recieves 3+ parameters. First is the length of worktime (in minutes), second is the length of free time, third and all next parameters are used as the name for your activity.

If less than 3 parameters are specified, it uses default values - 30 minutes for working, 5 minutes for relaxing and "Random stuff" as the name of activity.

If you want to end your session, you have to send SIGINT to the process (Ctrl+C). After that it logs your worktime into "data" file in human readable format.

## TODO:
- Script for installing the pomodoro
- NCurses graphics
- MAYBE notes and tasks for the day, if I'll have the time and motivation

Peace!
