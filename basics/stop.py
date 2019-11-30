# Stop the thing
from easygopigo3 import EasyGoPiGo3
import time


gpg = EasyGoPiGo3()
time.sleep(1)
gpg.stop()
