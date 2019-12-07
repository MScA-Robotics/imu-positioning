import time
from easygopigo3 import EasyGoPiGo3


gpg = EasyGoPiGo3()
gpg.reset_encoders()

gpg.forward()
time.sleep(2)
gpg.stop()
print(gpg.read_encoders())

# (1934, 13208)
# (1334, 12608
# (1316, 13771)

##https://gopigo3.readthedocs.io/en/master/_modules/easygopigo3.html
