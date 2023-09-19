# tmc5072
Rudimentary control of Trinamic TMC5072 stepper motor driver written in Python, intended for use on the Raspberry Pi

## Raspberry pi config

Auxilliary SPI peripherals (SPI1 and SPI2 on the Pi4) do not work with SPI mode 3.  SPI0 and SPI6 are confirmed working with this driver.

Add these lines to /boot/config.txt on the raspberry pi to enable SPI1 and SPI6, then reboot:

dtparam=spi=on


dtoverlay=spi1-1cs

dtoverlay=spi6-2cs

## Wiring TMC5072-BOB to Raspberry pi

If using the TMC5072-BOB, connect to the pi as follows for SPI6:

TMC5072-BOB    <---->    Raspberry Pi

VCCIO          <---->    3.3V (pin 1)

GND            <---->    GND  (pin 6, 14, 20, 30, or, 34)

CSN            <---->    SPI6_CE0_N (pin 12)

SCK            <---->    SPI6_SCLK (pin 40)

SDI            <---->    SPI6_MOSI (pin 38)

SDO            <---->    SPI6_MISO (pin 35)

CLK16          <---->    GND  (pin 6, 14, 20, 30, or, 34)

ENN            <---->    GND  (pin 6, 14, 20, 30, or, 34)

Connect GND to external power supply GND.
Connect VS to external power supply V+ (+5V minimum, +24V maximum)
