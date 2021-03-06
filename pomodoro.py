#!/bin/python

import signal
import time
import sys
import os


def print_cycle(cycles, minutes, timer, activity):
    os.system("clear")
    print("You currently spent " + str(cycles) + " cycles on " + activity + ".")
    print("\n[" + "#" * int(30 * minutes // timer[cycles % 2]) +
          "-" * int(30 - 30 * minutes // timer[cycles % 2]) + "]")
    if cycles % 2 == 0:
        print("\nTime for work. Current time: " + str(minutes) +
              " out of " + str(timer[cycles % 2]) + ".")
    else:
        print("\nTime for rest. Current time: " + str(minutes) +
              " out of " + str(timer[cycles % 2]) + ".")


def write_to_file(cycles, minutes, timer, activity):
    # Creating file
    file = open(os.path.join(os.path.expanduser('~'),'.cache/pomodoro/data'), "a+")
    file.close()

    # Opening file
    file = open(os.path.join(os.path.expanduser('~'),'.cache/pomodoro/data'), "r+")
    file.seek(0, 0)

    try:
        # If there already is a line with our activity, we are reading all the lines,
        # finding the line with our activity, reading numbers from it, updating deleting
        # the line and writing an updated line to the end of the file in (more or less) 
        # human readable format.
        content = file.readlines()
        previous = content.index([s for s in content if activity in s][0])
        for i in content[previous].split():
            if i.isnumeric():
                prev_data = int(i)
                break

        prev_data += minutes + timer[0] * (cycles // 2 + cycles % 2)

        file.seek(0)
        for i in content:
            if activity not in i:
                file.write(i)

        file.write(activity + ": " + str(prev_data) + " minute(s);\n")
        file.truncate()
    # If we catch ValueError or IndexError, it means that we couldn't find the line
    # with our activity. So, in this case we just create a line in the end.
    except ValueError:
        file.seek(0, 2)
        file.write(activity + ": " + str(minutes +
                                         timer[0] * (cycles // 2 + cycles % 2)) + " minute(s);\n")
    except IndexError:
        file.seek(0, 2)
        file.write(activity + ": " + str(minutes +
                                         timer[0] * (cycles // 2 + cycles % 2)) + " minute(s);\n")

    file.close()


def read_file():
    # Opening file. If not possible, print error.
    try:
        file = open(os.path.join(os.path.expanduser('~'),'.cache/pomodoro/data'), "r")
        file.seek(0, 0)

        content = file.readlines()
        for line in content:
            for i in line.split():
                if i.isnumeric():
                    info = int(i)
                    break

            print(line[:line.index(":")] + ": " + str(info // 60) +
                  " hours and " + str(info % 60) + " minute(s);")

        file.close()
    except OSError:
        print("Data file missing.")


def signal_handler(sig, frame):
    os.system("clear")
    print("You worked on " + activity + " for " + str(cycles // 2 + cycles % 2) +
          " cycles, totalling " + str(minutes + timer[0] * (cycles // 2 + cycles % 2)) + " minutes.")
    write_to_file(cycles, minutes, timer, activity)
    sys.exit(0)


# 30 minutes for work, 5 minutes for rest by default.
timer = [30, 5]
cycles = 0
minutes = 1
activity = "random stuff"

if len(sys.argv) != 1:
    if len(sys.argv) < 4 and sys.argv[1] == "-t" or sys.argv[1] == "--time":
        read_file()
        sys.exit()
    elif len(sys.argv) == 2 and sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Type work time in minutes as the first argument, rest time as " +
              "second and activity name as third, or use flags:\n\t-t\tprint current " +
              "time spent on stuff\n\t-h\tprint help (equivalent to --help)")
        sys.exit(0)

    if len(sys.argv) >= 4:
        timer = [int(sys.argv[1]), int(sys.argv[2])]
        activity = " ".join(sys.argv[3:])

signal.signal(signal.SIGINT, signal_handler)

while True:
    # Endless loop, to stop you just send SIGINT.
    minutes = 1
    while minutes <= timer[cycles % 2]:
        # Every loop is 1 minute
        print_cycle(cycles, minutes, timer, activity)
        minutes += 1
        time.sleep(60)
    cycles += 1
    print("\a")
    os.system("notify-send 'Time to rest'") if not cycles % 2 == 0 else os.system(
        "notify-send 'Time to work'")
