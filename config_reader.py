# Import the configparser module to read configuration files
import configparser

# Define a function to read settings from a configuration file
def read_config(config_file):
    # Create an instance of ConfigParser
    config = configparser.ConfigParser()
    
    # Read the configuration file using the read method
    config.read(config_file)
    
    # Return the settings under the 'Settings' section of the configuration file
    return config['Settings']
