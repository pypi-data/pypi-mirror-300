import logging
import logging.config
import toml

def setup_logging(config_file='logging_config.toml'):
    """
    Set up logging using a configuration from a TOML file.
    
    :param config_file: The path to the TOML file with logging configuration.
    """
    config = toml.load(config_file)
    
    # Get the log level and log file from the config
    log_level = config.get('logger', {}).get('level', 'DEBUG')
    log_file = config.get('logger', {}).get('file', 'app.log')
    
    # Get the format of the log messages
    log_format = config.get('format', {}).get('message_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    date_format = config.get('format', {}).get('date_format', '%Y-%m-%d %H:%M:%S')
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        datefmt=date_format,
        filename=log_file,  # Output to file
        filemode='a'  # Append mode
    )

