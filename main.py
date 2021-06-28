import hashlib
import argparse
import multiprocessing
import numpy as np
import time


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

def calc_hashrate(hashes,number_of_processes,time):
    hash_rate = hashes/1000000
    hash_rate = hash_rate * number_of_processes
    hash_rate = hash_rate/time
    hash_rate = np.round(hash_rate,3)
    return hash_rate


def hash_process(low_bound, high_bound, base_message, difficulty, solution, return_dict):
    return_dict['status'] = False
    for i in range(low_bound, high_bound):
        message = base_message + " " + str(i)
        message = str.encode(message)
        hashed_message = hashlib.sha256(message).hexdigest()
        check_hash = hashed_message[:difficulty]
        if check_hash == solution:
            return_dict['status'] = i
            break


    return return_dict

def main():
    parser = argparse.ArgumentParser("Tool to demonstrate POW")
    parser.add_argument("-mes","--message", type=str, default="Hello world")
    parser.add_argument("-d","--diff", type=int, default=7)
    parser.add_argument("-proc","--processes", type=int, default=10)
    parser.add_argument("-m","--mode", type=int, default=0)
    parser.add_argument("-s","--proc_size",type=int,default=7)

    args = parser.parse_args()
    process_size = args.proc_size
    process_size = pow(10,process_size)
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
            start = time.time()
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
                    exit_status = True
                    final_status = status
            end = time.time()
            if exit_status:
                print("found nounce: " + base_message + " " + str(final_status))
                message = base_message + " " + str(final_status)
                message = str.encode(message)
                hashed_message = hashlib.sha256(message).hexdigest()
                print(hashed_message)
                break
            if process_size*number_of_processes>=1000000000:
                billions = high_bound/1000000000
                print("Hashed " + str(np.round(billions)) + " billion times")
                hashes = high_bound - low_bound
                time_elasped = end-start
                hashrate = calc_hashrate(hashes,number_of_processes,time_elasped)
                print("Hashrate: " + str(hashrate) + " MH/sec")

            else:
                millions = high_bound/1000000
                print("Hashed " + str(np.round(millions)) + " million times")
                hashes = high_bound - low_bound
                time_elasped = end-start
                hashes = high_bound - low_bound
                time_elasped = end-start
                hashrate = calc_hashrate(hashes,number_of_processes,time_elasped)
                print("Hashrate: " + str(hashrate) + " MH/sec")

if __name__ == '__main__':
    main()
