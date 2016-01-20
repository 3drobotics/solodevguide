# Battery Bay

The *Battery Bay* is the intended location for mounting power system accessories including high capacity batteries, tethers, fuel cells and alternative energy sources. 

Since power system payloads are useful for all applications it is very important to make sure it does not interfere with the keep out zones of the [Accessory Bay](hardware-accessorybay.md).

For information on interfacing with the battery, please visit the [Battery Interface](hardware-battery.md) page.

## Mechanical Interface Specifications

To interface with Solo there are a few crucial interface points to pay attention to

* Interlocking with the battery tray
* Interfacing the electrical connection
* Using the release button
* Keep out zones for accessory payloads and props

Most all of these interfaces can be found in the battery bay envelope cad file (link to come).

Any battery options operating in the battery bay should minor approximately the same specs of the current battery:

* Weight: 500g
* Operating Temp: 0C ~ 40C
* Discharging operating temp: -20C ~ 60C

## Electrical Interface Specifications

The electrical interface with Solo is done through the following connectors:

* Battery side female connector is a Molex 171090-0048 ([PDF](https://drive.google.com/open?id=0B9l93ZUM5ooxMU0xM3h5MzNsMjVBV3NjYU9DSEdyZE5FQWhR)). This is a custom connector that can only be purchased in minimum orders of 1,000 units.

* Solo / charger side male connector is a Molex 171088-0048 ([PDF](https://drive.google.com/open?id=0B9l93ZUM5ooxblFVOVhuY2JwMExjd3FnYjgzZmNsNy1ialAw))

The connector contacts are rated for 40A on the power contacts

## Battery Payload Requirements

### Physical Characteristics

Any payloads operating in the battery bay should have approximately the same specs of the current battery:

* 500 grams
* Operating voltage range: 16.8 V to 12.0 V
* Discharging temperature: -20C ~ 60C

### Current Draw

Solo will draw around 15A during hover. Depending on wind, payload, and maneuver, it's possible to burst up to 120A discharge

### Battery Safety Features

It is up to the power system manufacturer to make sure all safety and regulatory certifications (including UL) are obtained. The power system must not have a low-voltage or low-capacity cut-off.

## Communication Protocol

Solo uses a standard SMBUS spec for communicating with the battery. To interface with Solo it is best to implement the [full SMBUS spec](https://drive.google.com/open?id=0B9l93ZUM5ooxXzZWT3FMdktaNjNGWDV6M0tQUDhwWWgtNEFB).
