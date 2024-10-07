from shapely.geometry import Polygon
import requests
import pandas as pd

NADAG_URL = "https://ogcapitest.ngu.no/rest/services/grunnundersokelser_utvidet"


def get_nadag_geotekniskborehull():
    url = f"{NADAG_URL}/collections/geotekniskborehull/items"
    return url


def _calculate_bbox_from_polygon(polygon: Polygon) -> str:
    """
    Calculate the bounding box from a Polygon object.
    """
    x_min, y_min, x_max, y_max = polygon.bounds
    return f"{x_min},{y_min},{x_max},{y_max}"


def fetch_geotechnical_borehole_data(
    polygon_lon_lat: Polygon,
    bbox_crs="http://www.opengis.net/def/crs/OGC/1.3/CRS84",
    crs="http://www.opengis.net/def/crs/OGC/1.3/CRS84",
    filter_crs="http://www.opengis.net/def/crs/OGC/1.3/CRS84",
    filter_lang="cql2-text",
    limit=100,
    max_allowable_offset=0.05,
    offset=0,
    skip_geometry=False,
):
    url = f"{NADAG_URL}/collections/geotekniskborehullunders/items"
    params = {
        "bbox": _calculate_bbox_from_polygon(polygon_lon_lat),
        "bbox-crs": bbox_crs,
        "crs": crs,
        "filter-crs": filter_crs,
        "filter-lang": filter_lang,
        "limit": limit,
        "maxAllowableOffset": max_allowable_offset,
        "offset": offset,
        "skipGeometry": str(skip_geometry).lower(),
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


url = f"{NADAG_URL}/collections/geotekniskborehullunders/items"
bbox_crs = ("http://www.opengis.net/def/crs/OGC/1.3/CRS84",)
crs = ("http://www.opengis.net/def/crs/OGC/1.3/CRS84",)
filter_crs = ("http://www.opengis.net/def/crs/OGC/1.3/CRS84",)
filter_lang = ("cql2-text",)
limit = (100,)
max_allowable_offset = (0.05,)
offset = (0,)
skip_geometry = False


params = {
    "bbox": "10,59,10.02,59.2",
    "bbox-crs": bbox_crs,
    "crs": crs,
    "filter-crs": filter_crs,
    "filter-lang": filter_lang,
    "limit": limit,
    "maxAllowableOffset": max_allowable_offset,
    "offset": offset,
    "skipGeometry": str(skip_geometry).lower(),
}

url_tolketlag = f"{NADAG_URL}/collections/geoteknisktolketlag/items"
url_grunnvann = f"{NADAG_URL}/collections/grunnvanndata/items"
# denne inneholder d meste av dataen
url_geotekniskborehull = f"{NADAG_URL}/collections/geotekniskborehullunders/items"
# url_geotekniskborehull= f"{NADAG_URL}/collections/geotekniskborehull/items"
# mulig nederste er bedre her faktiks inneholder kvikkleirePåvisning, boretlengde etc
# må sjekke om det er noe som mangler
response = requests.get(url_geotekniskborehull, params=params)
response.raise_for_status()
data = response.json()
features = data.get("features", [])
data_geometry = features[0].get("geometry", {})
data_prop = features[0].get("properties", {})
method = data_prop.get("geotekniskMetode", None)
methods = {"15": "metode-KombinasjonSondering"}
method_data = data_prop[methods.get(method, "")]
id = method_data[0]["title"]
href = method_data[0]["href"]
method_url = (
    f"{NADAG_URL}/collections/kombinasjonsonderingdata/items?kombinasjonSondering={id}"
)
r = requests.get(method_url)
r.raise_for_status()

data_method = r.json()
features_method = data_method.get("features", [])
get_properties = [properties.get("properties", {}) for properties in features_method]
dataframe = pd.DataFrame(get_properties)
