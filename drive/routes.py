from datetime import datetime
import time
import multiprocessing
from easygopigo3 import EasyGoPiGo3

gpg = EasyGoPiGo3()


def drive_and_queue(action_type, value, q=None):
    if action_type == 'drive':
        gpg.drive_cm(value)

    if action_type == 'turn':
        gpg.turn_degrees(value)

    if q:
        q.put([action_type, value, datetime.now().timestamp()])


def drive_demo_1(q=None):
    drive_and_queue('turn', 30, q)
    drive_and_queue('drive', 30, q)
    drive_and_queue('turn', 45, q)
    gpg.stop()


def drive_demo_2(q=None):
    drive_and_queue('turn', -30, q)
    drive_and_queue('drive', -30, q)
    drive_and_queue('turn', -45, q)
    gpg.stop()


def drive_inst_1(q=None):
    """Drive Instructions 1 (for demo path 1)

    Go 50cm, right turn, 50cm, left turn, 50cm
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    drive_and_queue('drive', 50, q)
    drive_and_queue('turn', 90, q)
    drive_and_queue('drive', 50, q)
    drive_and_queue('turn', -90, q)
    drive_and_queue('drive', 50, q)
    gpg.stop()


def drive_inst_2(q=None):
    """Drive Instructions 2

    Drive in a square with side 75cm
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    for _ in range(4):
        drive_and_queue('drive', 75, q)
        drive_and_queue('turn', 90, q)
    gpg.stop()


def drive_inst_3(q=None):
    """Drive Instructions for demo path 2

    Go 125cm, left 90 degrees, 50cm, right 90 degrees, 125cm
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    drive_and_queue('drive', 150, q)
    drive_and_queue('turn', -90, q)
    drive_and_queue('drive', 50, q)
    drive_and_queue('turn', -90, q)
    drive_and_queue('drive', 150, q)
    gpg.stop()


def drive_mini_1(q=None):
    """Drive Instructions mini 1

    Make a few short drives with 45 degree turns
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    for _ in range(4):
        drive_and_queue('drive', 10, q)
        drive_and_queue('turn', 45, q)
    drive_and_queue('drive', 10, q)
    gpg.stop()


def drive_mini_2(q=None):
    """Drive Instructions mini 2

    Drive 30cm with a 45 degree right turn in the middle
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    time.sleep(1)
    drive_and_queue('drive', 15, q)
    time.sleep(1)
    drive_and_queue('turn', 45, q)
    time.sleep(1)
    drive_and_queue('drive', 15, q)
    gpg.stop()


def drive_pause_1(q=None):
    """Drive Instructions with pause for rotation

    Drive 30cm with a 3 second pause then another 30 cm
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    drive_and_queue('drive', 30, q)
    time.sleep(3)
    drive_and_queue('drive', 30, q)
    gpg.stop()


def turn_series(q =None):
    """Test a series of rotations for tuning integration of encoders

    Make a series of turns that eventually go back to a common center
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    scale = 1.66
    print("Starting 5 degree turn right")
    drive_and_queue('drive', 5 * scale, q)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 10 degree turn right")
    drive_and_queue('turn', 10 *  scale, q)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 30 degree turn right")
    drive_and_queue('turn', 30 *  scale, q)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 45 degree turn right")
    drive_and_queue('turn', 45 *  scale, q)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 90 degree turn right")
    drive_and_queue('turn', 90 *  scale, q)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 30 degree turn left")
    drive_and_queue('turn', -30 *  scale, q)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 60 degree turn left")
    drive_and_queue('turn', -60 *  scale, q)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 90 degree turn left")
    drive_and_queue('turn', -90 *  scale, q)
    print("Completed turn")
    gpg.stop()
