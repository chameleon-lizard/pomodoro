import signal
import time
import sys
import os

def print_cycle(cycles, passed, timer):
    os.system("clear")
    print("Current cycles: "+ str(cycles) + ".")
    print("\n[" + "#" * int(30 * passed // timer[cycles % 2]) + "-" * int(30 - 30 * passed // timer[cycles % 2]) + "]")
    if cycles % 2 == 0:
        print("\nYou should work. Current time: " + str(passed) + " out of " + str(timer[cycles % 2]) + ".")
    else:
        print("\nYou should rest. Current time: " + str(passed) + " out of " + str(timer[cycles % 2]) + ".")

def signal_handler(sig, frame):
    os.system("clear")
    print("You worked " + str(cycles // 2 + cycles % 2) + " cycles, totalling " + str(passed + timer[0] * (cycles // 2 + cycles % 2)) + " minutes.")
    sys.exit(0)

# 30 minutes for work, 15 minutes for rest by default
timer = [30, 15]
cycles = 0
passed = 0

if len(sys.argv) == 3:
    timer = [int(sys.argv[1]), int(sys.argv[2])]

signal.signal(signal.SIGINT, signal_handler)

while True:
    passed = 0
    while passed != timer[cycles % 2]:
        print_cycle(cycles, passed, timer)
        passed += 1
        time.sleep(60)

    os.system("clear")
    print_cycle(cycles, passed, timer)
    cycles += 1
    time.sleep(1)
