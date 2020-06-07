import time
import multiprocessing
from easygopigo3 import EasyGoPiGo3

gpg = EasyGoPiGo3()


def drive_and_queue(action_type, value, q):
    if action_type == 'drive':
        gpg.drive_cm(value)

    if action_type == 'drive':
        gpg.turn_degrees(value)

    if q:
        q.put([action_type, value])


def drive_demo_1(q=None):
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
    gpg.drive_cm(50)
    gpg.turn_degrees(90)
    gpg.drive_cm(50)
    gpg.turn_degrees(-90)
    gpg.drive_cm(50)
    gpg.stop()


def drive_inst_2():
    """Drive Instructions 2

    Drive in a square with side 75cm
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    for _ in range(4):
        gpg.drive_cm(75)
        gpg.turn_degrees(90)
    gpg.stop()


def drive_inst_3():
    """Drive Instructions for demo path 2

    Go 125cm, left 90 degrees, 50cm, right 90 degrees, 125cm
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    gpg.drive_cm(150)
    gpg.turn_degrees(-90)
    gpg.drive_cm(50)
    gpg.turn_degrees(-90)
    gpg.drive_cm(150)
    gpg.stop()


def drive_mini_1():
    """Drive Instructions mini 1

    Make a few short drives with 45 degree turns
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    for _ in range(4):
        gpg.drive_cm(10)
        gpg.turn_degrees(45)
    gpg.drive_cm(10)
    gpg.stop()


def drive_mini_2():
    """Drive Instructions mini 2

    Drive 30cm with a 45 degree right turn in the middle
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    time.sleep(1)
    gpg.drive_cm(15)
    time.sleep(1)
    gpg.turn_degrees(45)
    time.sleep(1)
    gpg.drive_cm(15)
    gpg.stop()


def drive_pause_1():
    """Drive Instructions with pause for rotation

    Drive 30cm with a 3 second pause then another 30 cm
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    gpg.drive_cm(30)
    time.sleep(3)
    gpg.drive_cm(30)
    gpg.stop()


def turn_series():
    """Test a series of rotations for tuning integration of encoders

    Make a series of turns that eventually go back to a common center
    :return: None
    """
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    scale = 1.66
    print("Starting 5 degree turn right")
    gpg.turn_degrees(5 * scale)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 10 degree turn right")
    gpg.turn_degrees(10 * scale)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 30 degree turn right")
    gpg.turn_degrees(30 * scale)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 45 degree turn right")
    gpg.turn_degrees(45 * scale)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 90 degree turn right")
    gpg.turn_degrees(90 * scale)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 30 degree turn left")
    gpg.turn_degrees(-30 * scale)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 60 degree turn left")
    gpg.turn_degrees(-60 * scale)
    print("Completed turn")
    time.sleep(1.5)
    print("Starting 90 degree turn left")
    gpg.turn_degrees(-90 * scale)
    print("Completed turn")
    gpg.stop()
