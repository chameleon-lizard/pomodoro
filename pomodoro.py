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
    file = open("data", "a+")
    file.close()

    # Opening file
    file = open("data", "r+")
    file.seek(0, 0)

    try:
        # If there already is a line with our activity, we are reading all the lines,
        # finding the line with our activity, reading numbers from it, updating deleting
        # the line and writing an updated line to the end of the file in human readable format. 
        # TODO: find out if there is a better algorythm.
        content = file.readlines()
        previous = content.index([s for s in content if activity in s][0])
        prev_data = []
        for i in content[previous].split():
            if i.isnumeric():
                prev_data.append(int(i))

        prev_data[0] += cycles
        prev_data[1] += minutes + timer[0] * (cycles // 2 + cycles % 2)

        file.seek(0)
        for i in content:
            if activity not in i:
                file.write(i)

        file.write(activity + ": " +
                   str(prev_data[0]) + " cycle(s), " + str(prev_data[1]) + " minute(s);\n")
        file.truncate()
    # If we catch ValueError or IndexError, it means that we couldn't find the line
    # with our activity. So, in this case we just create a line in the end.
    except ValueError:
        file.seek(0, 2)
        file.write(activity + ": " + str(cycles) + " cycle(s), " +
                   str(minutes + timer[0] * (cycles // 2 + cycles % 2)) + " minute(s);\n")
    except IndexError:
        file.seek(0, 2)
        file.write(activity + ": " + str(cycles) + " cycle(s), " +
                   str(minutes + timer[0] * (cycles // 2 + cycles % 2)) + " minute(s);\n")

    file.close()


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
    os.system("notify-send 'Time to rest'") if cycles % 2 == 0 else os.system("notify-send 'Time to work'")
