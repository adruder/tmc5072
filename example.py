from tmc5072 import TMC5072

spi_device = 6
spi_cs = 0

motor_driver = TMC5072(spi_device, spi_cs)
motor_driver.load_config('.//tmc5072.ini')
motor_driver.basic_init()

motor_driver.goto_position(0, 512000)
motor_driver.goto_position(1, 512000)

