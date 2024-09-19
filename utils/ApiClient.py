import requests
import json
from bs4 import BeautifulSoup


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present

    def get(self, url, params=None, headers=None):
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {
                        'error': 'Invalid JSON response',
                        'status_code': response.status_code,
                        'content': response.text[:1000]
                    }
            else:
                return {
                    'error': 'Non-JSON response',
                    'status_code': response.status_code,
                    'content': response.text[:1000]
                }

        except requests.RequestException as e:
            return {
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None),
                'content': getattr(e.response, 'text', '')[:1000] if e.response else ''
            }

    def post(self, url, data=None, headers=None):
        try:
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()

            return {
                'content': response.text,
                'status_code': response.status_code
            }

        except requests.RequestException as e:
            return {
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None),
                'content': getattr(e.response, 'text', '')[:1000] if e.response else ''
            }

    ### Cochise County AZ

    def cochise_get_parcel_count(self, apn_prefix, acres_min=0.14, acres_max=1):
        endpoint = "/Yxem0VOcqSy8T6TE/arcgis/rest/services/Cad_Parcel_TaxInfo/FeatureServer/0/query"
        where_clause = f"((apn LIKE '{apn_prefix}%') AND (accttype = 'Vacant') AND (owner_name1 NOT LIKE '%LLC') AND (acres >= {acres_min}) AND (acres <= {acres_max}) AND (state <> 'AZ') AND (owner_name1 NOT LIKE '%PROPERTIES%'))"

        params = {
            "f": "json",
            "where": where_clause,
            "returnIdsOnly": "true",
            "returnCountOnly": "true",
            "returnGeometry": "false",
            "spatialRel": "esriSpatialRelIntersects"
        }
        return self.get(endpoint, params)

    def cochise_query_parcel_info(self, apn_prefix, acres_min=0.14, acres_max=1):
        endpoint = f"{self.base_url}/Yxem0VOcqSy8T6TE/arcgis/rest/services/Cad_Parcel_TaxInfo/FeatureServer/0/query"
        where_clause = f"((apn LIKE '{apn_prefix}%') AND (accttype = 'Vacant') AND (owner_name1 NOT LIKE '%LLC') AND (acres >= {acres_min}) AND (acres <= {acres_max}) AND (state <> 'AZ') AND (owner_name1 NOT LIKE '%PROPERTIES%'))"
        params = {
            "f": "json",
            "where": where_clause,
            "returnGeometry": "true",
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": "*",
            "orderByFields": "OBJECTID ASC",
            "outSR": "102100"
        }
        return self.get(endpoint, params)



