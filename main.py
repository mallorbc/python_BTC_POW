import hashlib
import argparse
import multiprocessing
import numpy as np


def set_difficulty(difficulty):
    check_hash = ""
    for i in range(difficulty):
        check_hash = check_hash + "0"
    return check_hash


def one_core(difficulty, base_message):
    counter = 0
    solution = set_difficulty(difficulty)
    while True:
        message = base_message + " " + str(counter)
        message = str.encode(message)
        hashed_message = hashlib.sha256(message).hexdigest()
        check_hash = hashed_message[:difficulty]
        if check_hash == solution:
            print()
            print(base_message + " " + str(counter))
            print()
            print(hashed_message)
            print("Hashed " + str(counter) + " times")
            break
        counter = counter + 1
        if counter % 1000000 == 0:
            million = counter / 1000000
            print("Hashed " + str(int(million)) + " million times")


def hash_process(low_bound, high_bound, base_message, difficulty, solution, return_dict):
    # return_dict = {}
    for i in range(low_bound, high_bound):
        message = base_message + " " + str(i)
        message = str.encode(message)
        hashed_message = hashlib.sha256(message).hexdigest()
        check_hash = hashed_message[:difficulty]
        if check_hash == solution:
            return_dict['status'] = i
            return return_dict

    return_dict['status'] = False
    return return_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Tool to demonstrate POW")
    parser.add_argument("-message", type=str, default="Hello world")
    parser.add_argument("-diff", type=int, default=1)
    parser.add_argument("-processes", type=int, default=6)
    parser.add_argument("-mode", type=int, default=0)
    process_size = 10000000

    args = parser.parse_args()
    base_message = args.message
    difficulty = args.diff
    number_of_processes = args.processes
    mode_to_run = args.mode
    if mode_to_run != 0:
        one_core(difficulty, base_message)
    else:
        counter = 0
        solution = set_difficulty(difficulty)
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        exit_status = False
        while True:
            jobs = []
            for i in range(number_of_processes):
                low_bound = counter*process_size
                high_bound = ((counter+1)*process_size)-1
                counter = counter + 1
                p = multiprocessing.Process(target=hash_process, args=(
                    low_bound, high_bound, base_message, difficulty, solution, return_dict))
                jobs.append(p)
                p.start()
            for proc in jobs:
                proc.join()
                status = return_dict.values()[0]
                if status != False and exit_status == False:
                    print(status)
                    exit_status = True
            if exit_status:
                break
            millions = high_bound/1000000
            print("Hashed " + str(np.round(millions)) + " million times")
