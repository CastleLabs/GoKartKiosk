# Import necessary modules
from config_reader import read_config  # To read settings from a configuration file
from image_processor import capture_and_print  # For image capture and processing functions
from gpio_utils import check_button_press  # For handling GPIO operations
import time  # For time-related functions like sleep

# The main execution block
if __name__ == "__main__":
    try:
        # Read settings from the configuration file
        settings = read_config('settings.conf')

        # Convert string settings to the appropriate types (integer and float)
        button_pin = int(settings['button_pin'])
        debounce_time = float(settings['debounce_time'])

        # Main program loop
        while True:
            # Check if the button is pressed with debouncing
            if check_button_press(button_pin, debounce_time):
                # Capture and process the image if the button is pressed
                capture_and_print(settings)
                # Delay to prevent immediate re-triggering of the button press
                time.sleep(5)

    except KeyboardInterrupt:
        # Handle any interruption by the user (e.g., Ctrl+C)
        print("Script interrupted by user. Cleaning up GPIO and exiting.")
    finally:
        # Clean up the GPIO pins to a safe state
        GPIO.cleanup()
        # Print a goodbye message upon exiting the script
        print("GPIO cleaned up. Goodbye!")
