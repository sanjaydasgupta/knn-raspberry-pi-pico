import machine
import utime

# The 3.3V on my Pico is actually 3.24 (as measured)
MY3V3 = 3.24

led_onboard = machine.Pin(25, machine.Pin.OUT)
led_red = machine.Pin(16, machine.Pin.OUT)
sensor_temp_internal = machine.ADC(4)
sensor_temp_lm35 = machine.ADC(26)

led_onboard.value(0)
led_red.value(0)

adc_conversion_factor = MY3V3 / 65535
delta = 200 # milliseconds
cycle_time = 5 # seconds

def blink(pin):
    pin.value(1)
    utime.sleep_ms(delta)
    pin.value(0)

def get_temp_internal():
    reading = sensor_temp_internal.read_u16() * adc_conversion_factor
    return 27 - (reading - 0.706)/0.001721

def get_temp_lm35():
    value = sensor_temp_lm35.read_u16() * adc_conversion_factor
    return value * 100

while True:
    blink(led_onboard)
    temp_ambient = get_temp_internal()
    print('ambient temperature', temp_ambient)
    temp_door = get_temp_lm35()
    print('door temperature', temp_door)
    if temp_door <= temp_ambient - 5:
        led_red.value(1)
    else:
        led_red.value(0)
    utime.sleep(cycle_time)