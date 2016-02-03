# Battery Bay

The *Battery Bay* can be used for mounting power system accessories including high capacity batteries, tethers, fuel cells and alternative energy sources. 

<aside class="tip">See the <a href="hardware-battery-charging.md">Battery Charger Interface</a> page for information needed to develop alternative battery charger products for Solo.</aside>

<aside class="caution">Battery Bay payloads must not interfere with other payload bay keepout areas.</aside>


## Mechanical Interface

The *Battery Bay* mechanical interface points with Solo are:

* Battery tray interlock
* Electrical connectors
* Release button
* Keep-out zones for propellers (and also other payload bays).

We recommend you enclose your power solution using the *battery bay envelope*, as this correctly implements the required mechanical interface points. The battery bay envelope CAD file [can be downloaded from here](https://drive.google.com/uc?id=0B9l93ZUM5ooxbUhDOUVVRWRORlkzdmY3LXI1T2YtVUJYbWtJ&export=download).

<aside class="note">The envelope CAD file can also be used for creating your own power supply enclosures.</aside>


## Electrical Interface

The electrical interface with Solo uses the following connectors:

* Battery side female connector is a Molex 171090-0048 ([PDF](https://drive.google.com/open?id=0B9l93ZUM5ooxMU0xM3h5MzNsMjVBV3NjYU9DSEdyZE5FQWhR)). This is a custom connector that can only be purchased in minimum orders of 1,000 units.

* Solo / charger side male connector is a Molex 171088-0048 ([PDF](https://drive.google.com/open?id=0B9l93ZUM5ooxblFVOVhuY2JwMExjd3FnYjgzZmNsNy1ialAw))

The connector contacts are rated for 40A on the power contacts



## Battery Payload Requirements

Battery bay payloads should have approximately the same physical and electrical characteristics as the current battery: [Solo Battery Specifications](hardware-battery-charging.html#solo-battery-specifications).

### Physical

The recommended physical characteristics are:

* 500 grams
* Operating Temp: 0C ~ 40C
* Discharging operating temp: -20C ~ 60C

Changing the battery weight will have a corresponding impact on the weight available for accessories. The center of gravity must remain close to the current location.

### Electrical

The main physical characteristics are:

* Operating voltage range: 16.8 V to 12.0 V
* 15A draw during hover with no payload (no Gimbal/Camera or other acessories)
* 20A draw during hover with full 700g payload
* 120A maximum burst (depends on wind, payload, and maneuver)


### Battery Safety Features

It is up to the power system manufacturer to make sure all safety and regulatory certifications (including UL) are obtained. The power system must not have a low-voltage or low-capacity cut-off.

## Communication Protocol

Solo uses the [standard SMBUS spec](https://drive.google.com/open?id=0B9l93ZUM5ooxXzZWT3FMdktaNjNGWDV6M0tQUDhwWWgtNEFB) for communicating with the battery. To interface with the battery it is best to implement the full specification.

The required SMBus connector is shown in the image below. The connector has 3 contacts across the top and bottom: the top contacts are connected to SCL/Clock, the bottom contacts are SDA/Data. The battery and SMBus must share a common ground.

![Solo Battery and SMBus Connectors](/images/solo_battery_charger_interface.png)