# imu-positioning

## Sensor - Returned Measurements  
Magnet x:  
Magnet y:  
Magnet z:  
Euler Heading: Dir w/ 0 being North 90 East, 180 South, 270 West  
Euler Roll:  
Euler Pitch: Angle up   
Accel x:  
Accel y:  
Accel z:  
Euler x:  
Euler y:  
Euler z:  
Thermometer: Temperature in Celcius  
Left Encoder: Odometer of left wheel  
Right Encoder: Odometer of right wheel  

### Node Setup
https://github.com/DexterInd/GoPiGo/tree/master/Software/NodeJS

$ npm install node-gopigo

This will break python gopigo
```
cd /home/pi/Dexter/GoPiGo3/Firmware
cp GoPiGo3_Firmware_1.0.0.bin ./archives/
cp archives/GoPiGo3_Firmware_0.3.4.bin .
rm GoPiGo3_Firmware_1.0.0.bin
bash gopigo3_flash_firmware.sh
```

Inorder for both node and python to gopygo to work change line 969 fo gopigo3.js to `Gopigo3.FIRMWARE_VERSION_REQUIRED = '1.0.x';`
