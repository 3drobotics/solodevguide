# Architectural Overview

Solo is a Linux system (iMX.6 running [Yocto Linux](advanced-linux.html)) connected to a Pixhawk autopilot.

The Pixhawk controls flight modes, stabilization, and recovery in the case of an RTL event (return-to-launch). Pixhawk communicates over the MAVLink telemetry protocol to both the onboard Linux computer and downstream devices like the Controller and mobile phone Solo apps.

The Linux system controls high-level operation of the copter: [smart shots](concept-smartshot.html), camera and gimbal control, mobile app communication, and accessory interaction are all implemented in this layer.

<img src="images/system-diagram.png" alt="Solo System Diagram" width="400" style="margin: 0 auto; display: block">

<!--<img src="images/system-telemetry.svg" alt="Solo System Telemetry" width="400" style="margin: 0 auto; display: block">-->
