# Battery Interface

## Overview

Solo's battery is used to power Solo, and needs regular recharging. This document specs out the interface to the Solo battery to build things like chargers and charging pads.

For information on interfacing with the Solo through the Battery Bay, visit the [Battery Bay page](hardware-batterybay.md).

## Battery Specs

> <sub>* 500 grams

> <sub>* Total capacity: 5.2 Ah (not a required spec)

> <sub>* Charge rate: 1-2 C

> <sub>* Discharge rate (continuous): 5 C

> <sub>* Discharge rate (peak): 10 C

> <sub>* Operating voltage range: 16.8 V to 10.0 V

> <sub>* Charging temp: 0℃ ~ 40℃

> <sub>* Discharging operating temp: -20℃ ~ 60℃

## Mechanical Interface Specifications

To interface with Solo there are a few crucial interface points to pay attention to

> <sub>* Interlocking with the battery

> <sub>* Interfacing the electrical connection

> <sub>* Using the release button

The best way to interface with these features is to use the battery bay CAD envelope (link to come).

## Electrical Interface Specifications

The electrical interface with Solo is done through the following connectors:

> <sub>* Battery side female connector is a Molex 171090-0048 ([PDF](https://drive.google.com/open?id=0B9l93ZUM5ooxMU0xM3h5MzNsMjVBV3NjYU9DSEdyZE5FQWhR)). This is a custom connector that can only be purchased in minimum orders of 1,000 units.

> <sub>* Solo / charger side male connector is a Molex 171088-0048 ([PDF](https://drive.google.com/open?id=0B9l93ZUM5ooxblFVOVhuY2JwMExjd3FnYjgzZmNsNy1ialAw))

The connector contacts are rated for 40A on the power contacts.

## Communication Protocol

Solo uses a standard SMBUS spec for communicating with the battery. To interface with the battery it is best to implement the [full SMBUS spec](https://drive.google.com/open?id=0B9l93ZUM5ooxXzZWT3FMdktaNjNGWDV6M0tQUDhwWWgtNEFB).
