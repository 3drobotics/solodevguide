# Battery Interface

Solo's battery is used to power Solo, and needs regular recharging. This document specs out the interface to the Solo battery to build things like chargers and charging pads.

For information on interfacing with the Solo through the Battery Bay, visit the [Battery Bay page](hardware-batterybay.md).

## Battery Specs

* 500 grams
* Total capacity: 5.2 Ah (not a required spec)
* Charge rate: 1-2C
* Discharge rate (continuous): 5C
* Discharge rate (peak): 10C
* Operating voltage range: 16.8 V to 10.0 V
* Charging temp: 0C ~ 40C
* Discharging operating temp: -20C ~ 60C

## Mechanical Interface Specifications

To interface with Solo there are a few crucial interface points to pay attention to

* Interlocking with the battery
* Interfacing the electrical connection
* Using the release button

The best way to interface with these features is to use the battery bay CAD envelope (link to come).

## Electrical Interface Specifications

The electrical interface with Solo is done through the following connectors:

* Battery side female connector is a Molex 171090-0048 ([PDF](https://drive.google.com/open?id=0B9l93ZUM5ooxMU0xM3h5MzNsMjVBV3NjYU9DSEdyZE5FQWhR)). This is a custom connector that can only be purchased in minimum orders of 1,000 units.

* Solo / charger side male connector is a Molex 171088-0048 ([PDF](https://drive.google.com/open?id=0B9l93ZUM5ooxblFVOVhuY2JwMExjd3FnYjgzZmNsNy1ialAw))

The connector contacts are rated for 40A on the power contacts.

## Communication Protocol

Solo uses a standard SMBUS spec for communicating with the battery. To interface with the battery it is best to implement the [full SMBUS spec](https://drive.google.com/open?id=0B9l93ZUM5ooxXzZWT3FMdktaNjNGWDV6M0tQUDhwWWgtNEFB).
