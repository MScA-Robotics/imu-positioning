import multiprocessing
from easygopigo3 import EasyGoPiGo3

gpg = EasyGoPiGo3()


def drive_inst_1():
    """Drive Instructions 1 (for demo path 1)

    Go 50cm, right turn, 50cm, left turn, 50cm
    :return: None
    """
    pro_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(pro_name))
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
    pro_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(pro_name))
    for _ in range(4):
        gpg.drive_cm(75)
        gpg.turn_degrees(90)
    gpg.stop()


def drive_inst_3():
    """Drive Instructions for demo path 2

    Go 125cm, left 90 degrees, 50cm, right 90 degrees, 125cm
    :return: None
    """
    pro_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(pro_name))
    gpg.drive_cm(150)
    gpg.turn_degrees(-90)
    gpg.drive_cm(50)
    gpg.turn_degrees(-90)
    gpg.drive_cm(150)
    gpg.stop()


def drive_inst_mini():
    """Drive Instructions 2

    Drive in a square with side 75cm
    :return: None
    """
    pro_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(pro_name))
    for _ in range(4):
        gpg.drive_cm(10)
        gpg.turn_degrees(45)
    gpg.stop()
