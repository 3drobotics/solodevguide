# Battery Charger Interface

This topic specifies the charging interface to the Solo battery (this is needed if you want to build chargers, charging pads, etc).

<aside class="tip">See the [Battery Bay](hardware-batterybay.html) page for information needed to develop alternative battery or power supply products for Solo.</aside>

## Solo Battery Specifications

The Solo battery has the following physical and electrical specifications:

* 500 grams
* Total capacity: 5.2 Ah (not a required spec)
* Charge rate: 1-2C
* Discharge rate (continuous): 5C
* Discharge rate (peak): 10C
* Operating voltage range: 10.0 V to 16.8 V
* Charging temp: 0C ~ 40C
* Discharging operating temp: -20C ~ 60C


## Mechanical Interface Specifications

The charger must be able to physically connect to the battery (the available space for the connector is bounded by the top cover off the battery).

![Solo Battery Charger Connection](/images/solo_battery_charger_interface.jpg)


## Electrical Interface Specifications

The electrical interface with the Solo battery uses the following connectors:

* Battery side female connector is a Molex 171090-0048 ([PDF](https://drive.google.com/open?id=0B9l93ZUM5ooxMU0xM3h5MzNsMjVBV3NjYU9DSEdyZE5FQWhR)). This is a custom connector that can only be purchased in minimum orders of 1,000 units.

* Charger side male connector is a Molex 171088-0048 ([PDF](https://drive.google.com/open?id=0B9l93ZUM5ooxblFVOVhuY2JwMExjd3FnYjgzZmNsNy1ialAw))

The connector contacts are rated for 40A on the power contacts.




## Communication Protocol

Solo uses the [standard SMBUS spec](https://drive.google.com/open?id=0B9l93ZUM5ooxXzZWT3FMdktaNjNGWDV6M0tQUDhwWWgtNEFB) for communicating with the battery. To interface with the battery it is best to implement the full specification.
