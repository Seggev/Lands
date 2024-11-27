import requests
import urllib.parse


class GeocodeAPI:
    def __init__(self, api_key):
        """
        Initialize the GeocodeAPI class with the Google API key.

        :param api_key: Google Geocoding API key
        """
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_county_and_state(self, location):
        """
        Get the county and state for a given location.

        :param location: Address, coordinates, or place name
        :return: Tuple containing county and state (county, state)
        """
        try:
            # URL encode the location and form the API URL
            url = f"{self.base_url}?address={urllib.parse.quote(location)}&key={self.api_key}"

            # Make a request to the API
            response = requests.get(url)
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()
            results = data.get('results', [])

            if not results:
                return None, None

            # Find county and state from the address components
            county = None
            state = None

            for component in results[0]['address_components']:
                types = component['types']

                if 'administrative_area_level_2' in types:
                    county = component['long_name']
                elif 'administrative_area_level_1' in types:
                    state = component['short_name']

            return county, state

        except Exception as e:
            print(f"An error occurred in get_county_and_state: {e}")
            return None, None
