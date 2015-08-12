# Getting Started

Development for Solo encompasses both externally interfacing to Solo (for a mobile app, ground control station, or API) and controlling the onboard computer. To begin, let's look at gaining control of Solo's shell console over SSH..

**NOTE:** We advise that you connect your computer to the Internet via ethernet while developing for Solo. When paired with Solo's WiFi network, you will not be able to access any webpages over your WiFi connection.

Power your Controller and your Solo. Connect your computer to Solo's Wifi network using the password for your given network (default password: "sololink").

To SSH into solo:

```
ssh root@10.1.1.10
```

Contact a 3DR employee for the default SSH password.
