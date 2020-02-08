# imu-positioning

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
