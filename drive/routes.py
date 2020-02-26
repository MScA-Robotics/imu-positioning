
def drive_inst_1():
    """Drive Instructions 1

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
    """Drive Instructions 3

    Go 75cm, right turn, 25cm, right turn, 50cm
    :return: None
    """
    pro_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(pro_name))
    gpg.drive_cm(75)
    gpg.turn_degrees(90)
    gpg.drive_cm(25)
    gpg.turn_degrees(90)
    gpg.drive_cm(50)
    gpg.stop()
