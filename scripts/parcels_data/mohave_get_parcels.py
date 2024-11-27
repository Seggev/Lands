import json

from utils.ApiClient import ApiClient

# APN_PREFIX = 209
#
#
# apns = []
api = ApiClient("")
#
# url = "https://mcgis.mohave.gov/Geocortex/Essentials/REST/sites/Copy_of_Public_Map_Viewer/map/mapservices/126/rest/services/x/MapServer/dynamicLayer/query"
#
#
# params = {
#         'f': 'json',
#         'where': f"TAXPIN Like '{APN_PREFIX}-%'",
#         'returnGeometry': 'false',
#         'spatialRel': 'esriSpatialRelIntersects',
#         'outFields': 'TAXPIN',
#         'returnDistinctValues': 'true',
#         'layer': json.dumps({"source": {"type": "mapLayer", "mapLayerId": 14}})
#     }
#
# headers = {
#         'accept': '*/*',
#         'accept-encoding': 'gzip, deflate, br, zstd',
#         'accept-language': 'en-US,en;q=0.9',
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
#         'x-requested-with': 'XMLHttpRequest'
#     }
#
# apns_response = api.get(url,params=params,headers=headers)
# if 'features' in apns_response:
#         for feature in apns_response['features']:
#             if 'attributes' in feature and 'TAXPIN' in feature['attributes']:
#                 apns.append(feature['attributes']['TAXPIN'])


apn = "209-04-045"
