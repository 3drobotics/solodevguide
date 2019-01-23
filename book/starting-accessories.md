# Solo Accessory Overview

This page is an overview of the main interface points for developing Solo accessories.


## Payload bays/integration points

Solo has three different payload bays:

* [Gimbal Bay](hardware-gimbalbay.md) - Primary payload, typically a camera.
* [Accessory Bay](hardware-accessorybay.md) - Secondary bay for high power accessories.
* [Battery Bay](hardware-batterybay.md) - Power system devices.

Other accessory/integration options include:

* [Solo Battery Chargers](hardware-battery-charging.md)
* Propellers


## Reserved zones

Modularity is a key benefit to developing on Solo. It is important to say inside the zone reserved for your accessory (outside of the zones reserved for other bays and the propeller keep-out zones). 

The diagram below shows the main zones available to all bays and the propellers.

![Solo Accessory Zones](/images/solo-accessory-zones.jpg)

Accessories exponentially increase in value when strategically combined!


## Accessory Communications

In order to communicate with Solo your accessory must establish a connection and be recognised by Solo. The two supported interfaces are USB and I2C (depending on payload bay).

Information for communicating with each bay is part of individual bay documentation.


<aside class="note">
At time of writing you can connect via USB but care needs to be taken not to interfere with other port configuration and devices.

We are currently developing a framework for safe and seamless accessory discoverability, app integration, and firmware updates.
</aside>



## Safety

Safety must be your top concern when developing for Solo.

Accessories should be firmly attached using the provided mechanical interfaces. 



