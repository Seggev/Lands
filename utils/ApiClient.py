import requests
import json

class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present

    def get(self, url, params=None, headers=None):
        full_url = f"{self.base_url}/{url.lstrip('/')}"  # Construct the full URL
        try:
            response = requests.get(full_url, params=params, headers=headers)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {
                        'error': 'Invalid JSON response',
                        'status_code': response.status_code,
                        'content': response.text
                    }
            else:
                return {
                    'error': 'Non-JSON response',
                    'status_code': response.status_code,
                    'content': response.text
                }
        except requests.RequestException as e:
            return {
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None),
                'content': getattr(e.response, 'text', '') if e.response else ''
            }

    def post(self, url, data=None, headers=None):
        full_url = f"{self.base_url}/{url.lstrip('/')}"  # Construct the full URL
        try:
            response = requests.post(full_url, data=data, headers=headers)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {
                        'error': 'Invalid JSON response',
                        'status_code': response.status_code,
                        'content': response.text
                    }
            else:
                return {
                    'error': 'Non-JSON response',
                    'status_code': response.status_code,
                    'content': response.text
                }
        except requests.RequestException as e:
            return {
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None),
                'content': getattr(e.response, 'text', '') if e.response else ''
            }
