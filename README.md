# CH423_for_micropython
Uses micropython's CH423S-IO extension chip<br>
Note: I/O driving capability of CH423S is actually found to be weak. MOS or BJT should be used for long line or large current<br>
## Tips
CH423S supports digital tube dynamic driver. I want to divide the dynamic driver library and the general IO driver library into two to do, and the dynamic driver library is tentative<br>
Although the CH423S has both SCL and SDA pins, this does not mean that it supports the full I2C protocol. WCH(CH423S manufacturer) mentions in the manual that it is not the standard I2C.<br>
Therefore, we cannot communicate with MCU hardware I2C directly (ACK cannot answer), so we use softI2C, but the problem is that CH423S does not support I2C address, any jump to enable SCL at SDA high level will wake up IC.<br>
Does this mean that if we use CH423S, we lose 2 IO's and cannot use the I2C bus?<br>
No, we can use an analog switch that shares a clock (SCL) with the I2C bus, and use an analog switch that acts as IO_MUX for data (SDA).<br>
So we use 3 MCU IO to achieve an I2C bus and 24 IO!<br>

