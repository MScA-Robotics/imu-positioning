
from drive.utils import get_reading


while ob_dist>=300:

    gpg.forward(100)
    gpg.turn_degrees(90)
    ob_dist=my_distance_sensor.read_mm()
    print(“Distance to Cone Reading: {} mm “.format(ob_dist))
gpg.stop()
