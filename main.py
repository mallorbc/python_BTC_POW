import hashlib
import argparse
import multiprocessing


def set_difficulty(difficulty):
    check_hash = ""
    for i in range(difficulty):
        check_hash = check_hash + "0"
    return check_hash


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Tool to demonstrate POW")
    parser.add_argument("-message", type=str, default="Hello world")
    parser.add_argument("-diff", type=int, default=1)
    args = parser.parse_args()
    base_message = args.message
    difficulty = args.diff
    counter = 0
    solution = set_difficulty(difficulty)
    while True:
        message = base_message + " " + str(counter)
        message = str.encode(message)
        # hashed_message = hashlib.sha224(message).hexdigest()
        hashed_message = hashlib.sha256(message).hexdigest()

        check_hash = hashed_message[:difficulty]
        solution = set_difficulty(difficulty)
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
