import logging

# Default API configuration
DEFAULT_CONFIG = {
    "base_url": "https://dev.beamdust.com",
    "api_version": "v1",
    "blocked_functions": []  # List of functions to be blocked (operationIds)
}

# Logging configuration
LOG_CONFIG = {
    "level": logging.INFO,  
    "filename": "beamdust.log",  
    "filemode": "a", 
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
}

# Documentation generation configuration
DOCUMENTATION_CONFIG = {
    "package_name": "Beamdust SDK",
    "introduction": (
        "Beamdust SDK is a Python package for interacting with a Swagger-based API. "
        "This package allows you to call API endpoints as Python functions."
    ),
    "usage": (
        "To use the package, initialize the Beamdust class with your API credentials and call the methods. "
        "All dynamically generated methods are based on the API's Swagger specification."
    ),
    "help_options": ["Use the _help parameter to get additional information about a method."],
    "output_file": "beamdust_documentation.html"
}
