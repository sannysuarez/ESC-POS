"""
RAASU v2.0.0 - Web-based Thermal Printer POS System
Configuration and environment setup
"""
import os

# Environment variable setup
ENV = os.environ.get('FLASK_ENV', 'development')
DEBUG = ENV == 'development'

# Database
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///raasu.db')

# Flask secret
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Thermal printer settings
PRINTER_PORT = os.environ.get('PRINTER_PORT', '/dev/ttyUSB0')
PRINTER_BAUDRATE = int(os.environ.get('PRINTER_BAUDRATE', 9600))

# Venture/Business information (editable by admin)
VENTURE_NAME = os.environ.get('VENTURE_NAME', 'RAASU POS System')
VENTURE_ADDRESS = os.environ.get('VENTURE_ADDRESS', 'Default Address')
