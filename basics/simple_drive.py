from easygopigo3 import EasyGoPiGo3
import time

gpg = EasyGoPiGo3()
gpg.forward()
gpg.stop()
gpg.forward()

time.sleep(2)
gpg.right()
time.sleep(1)
gpg.left()

time.sleep(1)
gpg.backward()
time.sleep(3)
gpg.stop()
gpg.set_speed(10000)

# gpg.drive_cm(50, blocking=False)
time.sleep(1)

gpg.stop()
