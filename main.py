import grovepi
from grove_rgb_lcd import *
import time

# Set up sensor pins
led_pins = [4, 3, 2]  # Red, Blue, Green LEDs
sound_sensor = 0
temp_hum_sensor = 7
light_sensor = 1
relay_pin = 8
button_pin = 6
ultrasonic_sensor = 2
rotary_sensor = 14
buzzer_pin = 5

# Initialize sensor connections
for led_pin in led_pins:
    grovepi.pinMode(led_pin, "OUTPUT")

grovepi.pinMode(sound_sensor, "INPUT")
grovepi.pinMode(temp_hum_sensor, "INPUT")
grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(relay_pin, "OUTPUT")
grovepi.pinMode(button_pin, "INPUT")
grovepi.pinMode(ultrasonic_sensor, "INPUT")
grovepi.pinMode(rotary_sensor, "INPUT")
grovepi.pinMode(buzzer_pin, "OUTPUT")

# Initialize LCD
setRGB(0, 128, 64)
setText("Initializing...")

try:
    while True:
        # Sound sensor
        sound_value = grovepi.analogRead(sound_sensor)
        if sound_value > 300:
            digitalWrite(led_pins[0], 1)  # Turn on the red LED
            setText("Sound detected")
            grovepi.digitalWrite(buzzer_pin, 1)
        else:
            digitalWrite(led_pins[0], 0)
            grovepi.digitalWrite(buzzer_pin, 0)

        # Temperature and humidity sensor
        [temp, humidity] = grovepi.dht(temp_hum_sensor, 0)
        setText(f"Temp: {temp:.1f}C  Humidity: {humidity:.1f}%")

        # Light sensor
        light_value = grovepi.analogRead(light_sensor)
        if light_value < 300:
            digitalWrite(led_pins[2], 1)  # Turn on the green LED
        else:
            digitalWrite(led_pins[2], 0)

        # Ultrasonic sensor
        distance = grovepi.ultrasonicRead(ultrasonic_sensor)
        setText(f"Distance: {distance} cm")

        # Button
        button_state = grovepi.digitalRead(button_pin)
        if button_state == 1:
            digitalWrite(led_pins[1], 1)  # Turn on the blue LED
        else:
            digitalWrite(led_pins[1], 0)

        # Rotary sensor
        rotary_value = grovepi.analogRead(rotary_sensor)
        setText(f"Rotary: {rotary_value}")

        time.sleep(0.5)

except KeyboardInterrupt:
    digitalWrite(relay_pin, 0)  # Turn off relay
    for led_pin in led_pins:
        digitalWrite(led_pin, 0)
    grovepi.digitalWrite(buzzer_pin, 0)
    setText("Goodbye!")
