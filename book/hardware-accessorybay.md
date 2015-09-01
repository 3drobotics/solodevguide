# Accessory Port

## Mechanical

The Accessory Bay is considered to be the area behind the gimbal under the Solo that does not interfere with the 3DR Gimbal. It is roughly 3" wide x 5.25" long x 4" deep. 

Maximum payload of the system is 700g, the 3DR Gimbal + GoPro weigh approximately 390g, leaving 310g for accessories that are meant to be used with the 3DR Gimbal.

The Accessory Bay hole pattern is M2 screws in a 1.655" x 1.15" rectanglar pattern. Beware that the rectangle is intersected by the path of the gimbal.

## Electrical

The connector part number is [JAE SJ038252](https://jae-connectors.com/en/pdf_download_exec.cfm?param=SJ038252.pdf) and can be purchased on [Digi-Key](https://www.digikey.com/product-search/en?keywords=TX24-30R-6ST-N1E).

The pinout of the Accessory Port is:

Pin | Description | Pin | Description
--- | --- | --- | ---
1. | USB D- | 16. | USB GND
2. | USB D+ | 17. | +5V
3. | N/C | 18. | N/C
4. | N/C | 19. | +5V
5. | N/C | 20. | N/C
6. | N/C | 21. | GND
7. | N/C | 22. | N/C
8. | N/C | 23. | BUS ID
9. | SER5 TX (DEBUG) | 24. | SER5 RX (DEBUG)
10. | SER2RT | 25. | SER2CT
11. | SER2Tx | 26. | SER2Rx
12. | CANH1 | 27. | 3DRID (USB ID)
13. | CANL1 | 28. | GND
14. | GND | 29. | GND
15. | BATT | 30. | BATT

## Communication Protocol

The two primary interfaces to the Accessory Bay will be the CAN bus for direct integration with the flight controller and the USB port for higher-level interactions with Smart shots, DroneKit, and interactions with Artoo.

CAN - Uses the [UAVCAN](http://uavcan.org/UAVCAN) protocol and interfaces directly with the Pixhawk. 

USB - USB Host device to the IMX co-processor.

SERIAL 2 - A direct MAVLink connection to the PixHawk.

SERIAL 5 - Shell access to the Pixhawk for debug access. We will not actively encourage developers to use this bus.
