# Import the RPi.GPIO library to control Raspberry Pi GPIO pins
import RPi.GPIO as GPIO
# Import the time library for delays
import time

# Function to check for a button press with software debouncing
def check_button_press(button_pin, debounce_time):
    # Set the GPIO mode to BCM
    GPIO.setmode(GPIO.BCM)
    # Set up the specified GPIO pin as an input with a pull-up resistor
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Read the initial state of the button
    input_state = GPIO.input(button_pin)

    # Check if the button is initially pressed
    if input_state == False:
        # Wait for the specified debounce time
        time.sleep(debounce_time)
        # Read the state of the button again
        input_state = GPIO.input(button_pin)
        # If the button is still pressed, return True
        if input_state == False:
            return True

    # If no valid press is detected, return False
    return False
