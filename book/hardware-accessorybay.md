# Accessory Port

## Mechanical

The *Accessory Bay* is considered to be the area behind the gimbal under the Solo that does not interfere with the 3DR Gimbal. It is roughly 3" wide x 5.25" long x 4" deep. 

Maximum payload of the system is 700g, the 3DR Gimbal + GoPro weigh approximately 390g, leaving 310g for accessories that are meant to be used with the 3DR Gimbal.

The Accessory Bay hole pattern is M2 screws in a 1.655" x 1.15" rectangular pattern. Ensure that the rectangle is not intersected by the path of the gimbal.

![Hole Pattern](https://cloud.githubusercontent.com/assets/2678765/10023369/612fcd74-6117-11e5-961d-6a9d4ffeeb35.png)

## Electrical

The mating connector part number is [JAE SJ038252](https://jae-connectors.com/en/pdf_download_exec.cfm?param=SJ038252.pdf) and can be purchased on [Mouser](http://www.mouser.com/ProductDetail/JAE-Electronics/TX24-30R-6ST-N1E/?qs=%2fha2pyFaduiqgba8kBa6TtehVWNIeLFx3lhQ48lSxiSCqywLxSV2eg%3d%3d).

The pinout of the Accessory Port is:

Pin | Name | Description
--- | --- | --- 
1. | USB D- | Negative differential data signal to iMX6 OTG USB port.
2. | USB D+ | Positive differential data signal to iMX6 OTG USB port.
3. | N/C | 
4. | N/C | 
5. | N/C |  
6. | N/C | 
7. | N/C |  
8. | N/C |  
9. | SER5 TX (DEBUG) | UART5 TX output from Pixhawk 2.
10. | SER2RT | UART2 RTS output from Pixhawk 2 for flow control. Connect to device's CTS pin.
11. | SER2Tx | UART3 RX signal to Pixhawk 2. Connect to device's TX pin. Voltage is 3.3V.
12. | CANH1 | CAN bus high to the Pixhawk 2.
13. | CANL1 | CAN bus low to the Pixhawk 2.
14. | GND | Ground reference on Solo system.
15. | BATT | 14V to 16.8V. PTC 1.1A fuse.
16. | USB GND |  
17. | +5V |  4.75 to 5.5V voltage pin for USB device. Current trip set to 1.2A.
18. | N/C |  
19. | +5V |  4.75 to 5.5V voltage pin for USB device. Current trip set to 1.2A.
20. | N/C |  
21. | GND | Ground reference on Solo system.
22. | N/C |  
23. | BUS ID |  
24. | SER5 RX (DEBUG) | UART5 RX input to Pixhawk 2.
25. | SER2CT | UART2 CTS input to Pixhawk 2 for flow control. Connect to device's RTS pin.
26. | SER2Rx | UART3 TX signal from Pixhawk 2. Connect to device RX pin. Voltage is 3.3V.
27. | 3DRID | USB ID pin for OTG port on iMX6 OTG port	
28. | GND | Ground reference on Solo system.
29. | GND | Ground reference on Solo system.
30. | BATT (14.0-16.8V, 1.5A max) | 14V to 16.8V. PTC 1.1A fuse.


## Communication Protocol

The two primary interfaces to the *Accessory Bay* will be the CAN bus for direct integration with the flight controller and the USB port for higher-level interactions with Smart shots, DroneKit, and interactions with the Controller.

CAN - Uses the [UAVCAN](http://uavcan.org/UAVCAN) protocol and interfaces directly with the Pixhawk. 

USB - USB Host device to the iMX6 co-processor.

## Accessory Breakout Board

An open source reference design for a breakout board can be found [here](https://github.com/3drobotics/Pixhawk_OS_Hardware/tree/master/Accessory_Breakout_X1).
