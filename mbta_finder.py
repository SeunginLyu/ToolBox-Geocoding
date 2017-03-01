"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib.parse
import urllib.request
import json

# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation?"
MBTA_BASE_URL2 = "http://realtime.mbta.com/developer/api/v2/routesbystop?"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read()
    response_data = json.loads(str(response_text, "utf-8"))
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    You can choose to only get output for certain modes of transporation
    which include "Bus", "Subway", "Commuter rail", "Boat"

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    url = GMAPS_BASE_URL
    querystring = {'address': place_name}
    url += urllib.parse.urlencode(querystring)
    json_output = get_json(url)
    latitude = json_output["results"][0]["geometry"]["location"]["lat"]
    longitude = json_output["results"][0]["geometry"]["location"]["lng"]
    return (latitude, longitude)


def get_nearest_station(latitude, longitude, only=None):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    You can choose to only get output for certain modes of transporation
    which include "Bus", "Subway", "Commuter rail", "Boat"

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    url = MBTA_BASE_URL
    querystring = {'api_key': MBTA_DEMO_API_KEY, 'lat': latitude,
                   'lon': longitude, 'format': 'json'}
    url += urllib.parse.urlencode(querystring)
    json_output = get_json(url)

    i = 0
    while (i < 15):  # MBTA returns 15 maximum stops
        station_name = json_output["stop"][i]["stop_name"]
        distance = json_output["stop"][i]["distance"]
        station_id = json_output["stop"][i]["stop_id"]

        if only is None:
            break
        else:
            url2 = MBTA_BASE_URL2
            querystring = {'api_key': MBTA_DEMO_API_KEY, 'stop': station_id,
                           'format': 'json'}
            url2 += urllib.parse.urlencode(querystring)
            json_output2 = get_json(url2)
            stop_mode_name = json_output2["mode"][0]["mode_name"]
            if(stop_mode_name == only):
                break
            else:
                i += 1

    return (station_name, distance)


def find_stop_near(place_name, only=None):
    """
    Given a place name or address, print the nearest MBTA stop and the
    distance from the given place to that stop.
    """
    place_coordinates = get_lat_long(place_name)
    mbta_data = get_nearest_station(place_coordinates[0], place_coordinates[1],
                                    only)
    return mbta_data


if __name__ == '__main__':
    target_place = "TD Garden"
    nearest_subway_stop = find_stop_near(target_place, "Subway")
    nearest_bus_stop = find_stop_near(target_place, "Bus")
    nearest_commuter_rail_stop = find_stop_near(target_place, "Commuter Rail")
    nearest_ferry_stop = find_stop_near(target_place, "Ferry")
    print("Nearest Subway : " + nearest_subway_stop[0] +
          "\nDistance : " + nearest_subway_stop[1])
    print("Nearest Bus : " + nearest_bus_stop[0] +
          "\nDistance : " + nearest_bus_stop[1])
    print("Nearest Commuter Rail : " + nearest_commuter_rail_stop[0] +
          "\nDistance : " + nearest_commuter_rail_stop[1])
    print("Nearest Ferry : " + nearest_ferry_stop[0] +
          "\nDistance : " + nearest_ferry_stop[1])
