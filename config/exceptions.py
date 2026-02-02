"""
Custom Exception Handler
"""
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    """
    Custom exception handler that wraps errors in our standard format.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        # Get error code
        if isinstance(exc, APIException):
            code = exc.default_code.upper() if hasattr(exc, 'default_code') else 'ERROR'
        else:
            code = 'ERROR'
        
        # Get error message
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                # Validation errors
                errors = []
                for field, messages in exc.detail.items():
                    if isinstance(messages, list):
                        for msg in messages:
                            errors.append({'field': field, 'message': str(msg)})
                    else:
                        errors.append({'field': field, 'message': str(messages)})
                
                response.data = {
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Validation failed',
                        'details': errors
                    }
                }
            elif isinstance(exc.detail, list):
                response.data = {
                    'success': False,
                    'error': {
                        'code': code,
                        'message': exc.detail[0] if exc.detail else 'An error occurred'
                    }
                }
            else:
                response.data = {
                    'success': False,
                    'error': {
                        'code': code,
                        'message': str(exc.detail)
                    }
                }
        else:
            response.data = {
                'success': False,
                'error': {
                    'code': code,
                    'message': str(exc)
                }
            }
    
    return response
