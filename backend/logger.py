#!/usr/bin/env python3
"""
Logging Configuration for Household Services
Provides centralized logging with file rotation and detailed error tracking
"""

import os
import logging
import logging.handlers
from datetime import datetime
from functools import wraps
import traceback
import sys

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

def setup_logger(name='household_services', level=logging.INFO):
    """
    Setup a logger with file rotation and console output
    
    Args:
        name (str): Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s'
    )
    
    # Console handler (INFO and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler for all logs (DEBUG and above)
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Error file handler (ERROR and above)
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/errors.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    # Database operations handler
    db_handler = logging.handlers.RotatingFileHandler(
        'logs/database.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    db_handler.setLevel(logging.DEBUG)
    db_handler.setFormatter(detailed_formatter)
    
    # Create database logger
    db_logger = logging.getLogger('database')
    db_logger.setLevel(logging.DEBUG)
    db_logger.handlers.clear()
    db_logger.addHandler(db_handler)
    
    return logger

def log_function_call(func):
    """
    Decorator to log function calls with parameters and execution time
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('household_services')
        
        # Log function entry
        func_name = func.__name__
        module_name = func.__module__
        
        logger.debug(f"Entering function: {module_name}.{func_name}")
        logger.debug(f"Args: {args}")
        logger.debug(f"Kwargs: {kwargs}")
        
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            logger.debug(f"Function {func_name} completed successfully in {execution_time:.3f}s")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Function {func_name} failed after {execution_time:.3f}s: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    return wrapper

def log_database_operation(operation_type):
    """
    Decorator to log database operations
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            db_logger = logging.getLogger('database')
            
            func_name = func.__name__
            db_logger.info(f"Database {operation_type}: {func_name}")
            db_logger.debug(f"Args: {args}")
            db_logger.debug(f"Kwargs: {kwargs}")
            
            start_time = datetime.now()
            
            try:
                result = func(*args, **kwargs)
                execution_time = (datetime.now() - start_time).total_seconds()
                
                db_logger.info(f"Database {operation_type} completed in {execution_time:.3f}s")
                return result
                
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                db_logger.error(f"Database {operation_type} failed after {execution_time:.3f}s: {str(e)}")
                db_logger.error(f"Exception type: {type(e).__name__}")
                db_logger.error(f"Traceback: {traceback.format_exc()}")
                raise
        
        return wrapper
    return decorator

def log_api_request(func):
    """
    Decorator to log API request/response
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('household_services')
        
        # Try to get request info
        request_info = "Unknown"
        try:
            from flask import request
            if request:
                request_info = f"{request.method} {request.path}"
        except:
            pass
        
        logger.info(f"API Request: {request_info}")
        logger.debug(f"Function: {func.__name__}")
        
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"API Response: {request_info} - {execution_time:.3f}s")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"API Error: {request_info} - {str(e)} - {execution_time:.3f}s")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    return wrapper

def log_error_with_context(error, context=None):
    """
    Log an error with additional context information
    
    Args:
        error: The exception that occurred
        context (dict): Additional context information
    """
    logger = logging.getLogger('household_services')
    
    error_info = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'timestamp': datetime.now().isoformat(),
        'context': context or {}
    }
    
    logger.error(f"Error occurred: {error_info['error_type']}: {error_info['error_message']}")
    logger.error(f"Context: {error_info['context']}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return error_info

def log_performance_metric(metric_name, value, unit="ms"):
    """
    Log performance metrics
    
    Args:
        metric_name (str): Name of the metric
        value (float): Metric value
        unit (str): Unit of measurement
    """
    logger = logging.getLogger('household_services')
    logger.info(f"Performance Metric: {metric_name} = {value} {unit}")

def log_security_event(event_type, details, severity="INFO"):
    """
    Log security-related events
    
    Args:
        event_type (str): Type of security event
        details (str): Event details
        severity (str): Event severity (INFO, WARNING, ERROR)
    """
    logger = logging.getLogger('household_services')
    
    security_info = {
        'event_type': event_type,
        'details': details,
        'timestamp': datetime.now().isoformat(),
        'severity': severity
    }
    
    if severity == "ERROR":
        logger.error(f"Security Event: {event_type} - {details}")
    elif severity == "WARNING":
        logger.warning(f"Security Event: {event_type} - {details}")
    else:
        logger.info(f"Security Event: {event_type} - {details}")

# Initialize the main logger
main_logger = setup_logger()

# Export commonly used functions
__all__ = [
    'setup_logger',
    'log_function_call',
    'log_database_operation',
    'log_api_request',
    'log_error_with_context',
    'log_performance_metric',
    'log_security_event',
    'main_logger'
] 