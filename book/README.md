<div style="text-align: center">
<img src="http://3drobotics.com/wp-content/uploads/2015/01/solo-drone-spin-transparent-500px.png">
<h1 style="border: none; font-size: 2.8em; margin-top: 0;" id="solo-development-guide">Solo Development Guide</h1>
</div>

<aside class="caution">
Developers only! This guide is under active development and not intended for consumers. Some modifications may require you to factory reset your Solo in order to return it to a working (and flying) state.
</aside>

This guide describes how to work inside Solo's system architecture and develop applications for Solo.

The objective of this guide is to enable developers to:

* Get a General Overview of how Solo works
* Access and work with Solo's Linux distribution
* Upload and run Python scripts, including DroneKit-Python
* Run services that run on boot
* Process video as it’s being streamed to and from Solo
* Troubleshoot Solo

Navigate using the sidebar or the "next page" arrows to begin.

## Changelog

### 2016-02-01

* New docs for accessory developers: [Solo Accessory Overview](starting-accessories.md), [Battery Bay](hardware-batterybay.md), [Battery Charger Interface](hardware-battery-charging.md).
* [Gimbal](hardware-gimbalbay.md) docs updated. Added power supply information, new gimbal "Beauty Plate" CAD file, information about software integration. Corrected description of HDMI cable.
* [Accessory Bay](hardware-accessorybay.md) docs updated. Added new power supply and communications architecture sections, along with information about how to connect to the accessory port via USB. Improved the information in the pinout.
* [System architecture diagram](concept-architecture.md) updated. Added more detail about components, power supply, data flow.

### 2015-10-29

* Guide relicensed as [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### 2015-09-25

* `solo-utils` is removed.
* The PC command line tool [*Solo CLI*](https://github.com/3drobotics/solo-cli) is now used for all examples.
* Video output examples temporarily reduced in scope to improve reliability.

### 2015-09-09

* Initial release!

## License

The Solo Development Guide is released as [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). See our [Github Repository](https://github.com/3drobotics/solodevguide) for more details.
