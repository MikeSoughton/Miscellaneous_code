#!/usr/bin/python
import time

def stopwatch(seconds):
    start = time.time()
    time.clock()
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
        print("loop cycle time: %f, seconds count: %02d" % (time.clock() , elapsed))
        time.sleep(1)

#stopwatch(20)

def print_on_interval(savepoint, max_time):
    start = time.time()
    #time.clock()
    time.perf_counter()
    elapsed = 0
    while True:
        try:
            while elapsed < max_time:
                elapsed = time.time() - start
                if round(elapsed,0) % savepoint == 0 and round(elapsed,1) > 0:
                    print("Maybe I can do something at this point in time...: %f, seconds count: %02d" % (time.perf_counter(), elapsed))


                print("loop cycle time: %f, seconds count: %02d" % (time.perf_counter(), elapsed))
                time.sleep(1)

        except KeyboardInterrupt:
            print("Are you sure you want to end the loop?")
            end = input()
            if end.lower() == "yes" or end.lower() == "y":
                print("Ending loop now.")
                break
            else:
                print("Continuing loop")
                continue

        break


print_on_interval(5, 10)