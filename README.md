# tmc5072
Rudimentary control of Trinamic TMC5072 stepper motor driver written in Python, intended for use on the Raspberry Pi

Auxilliary SPI peripherals (SPI1 and SPI2 on the Pi4) do not work with SPI mode 3.  SPI0 and SPI6 are confirmed working with this driver.
