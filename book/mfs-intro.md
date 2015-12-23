# Creating a Solo accessory

This page will be an overview on how to develop Solo accessories. The main components of integration are:

### 1. Select a Solo payload bay
There are three different payload bays on Solo to integrate your accessory. Each accessory bay has it's own features and benefits.

+ [Gimbal Bay](hardware-gimbalbay.md) - Primary payload, typically a camera
+ [Accessory Bay](hardware-accessorybay.md) - Secondary payload, high power option
+ Battery Bay - Power system devices

It is important to stay outside of designated keep out zones since modularity is a key benefit to developing on Solo. Accessories exponentially increase in value when strategically combined.

[Learn more...](mfs-payloadbays)

### 2. Get discovered by Sololink

In order to communicate with Solo your accessory must establish a connection and be recognized by Solo. The two supported hardware interfaces are via USB and I2C (depending on the payload bay). Your accessory hardware should contain a small amount of memory to store it's Vendor and Product ID's so Solo knows what driver to use.

[Learn more...](mfs-discovery)

### 3. Create driver and UI



### 4. Enable upgrade path

### 5. TEST TEST TEST
