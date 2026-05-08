#adding comments to be pushed to vs code

Module summary:
    Utilities for resolving two places (by name or "lat,lon" coordinates),
    computing the great-circle distance between them using the haversine formula,
    and printing a human-friendly formatted result in kilometers and miles.


Module-level behavior and notes:
    - Supports input as place names (geocoded via the OpenStreetMap Nominatim API)
      or as explicit coordinates in "lat,lon" string form.
    - Uses a custom User-Agent header when contacting Nominatim to comply with
      API requirements. Be mindful of Nominatim usage policy and rate limits.
    - Network calls may raise URLError/HTTPError or timeout exceptions; these
      should be handled by callers if programmatic use is required.
    - Coordinates are validated to be within standard latitude/longitude ranges.
    - Distances are returned in kilometers and formatted with an equivalent in miles.

Functions (explanatory comments):

    haversine(lat1, lon1, lat2, lon2)
        - Purpose:
            Compute the great-circle distance between two geographic points
            on the Earth using the haversine formula.
        - Parameters:
            lat1, lon1: float - latitude and longitude of the first point in degrees.
            lat2, lon2: float - latitude and longitude of the second point in degrees.
        - Returns:
            float - distance between the two points in kilometers.
        - Implementation notes:
            Converts degrees to radians, computes the haversine of the central
            angle, and multiplies by the mean Earth radius (approx. 6371.0088 km).
            Numerically stable for short and long distances.

    geocode(place)
        - Purpose:
            Resolve a place name (free-text) to a pair of (latitude, longitude)
            by querying the Nominatim search API.
        - Parameters:
            place: str - free-text place name or address to geocode.
        - Returns:
            tuple(float, float) - (latitude, longitude) of the top search result.
        - Errors / Exceptions:
            Raises ValueError if the API returns no results for the given place.
            Network-related exceptions (timeouts, HTTP errors) may also be raised
            by the underlying HTTP library; callers may catch these.
        - Implementation notes:
            Sends a GET request with format=json and limit=1, and parses the
            returned JSON to extract lat/lon. A descriptive User-Agent header
            is supplied to the API request.

    parse_point(s)
        - Purpose:
            Parse a string input into a geographic point (lat, lon).
            Accepts either "lat,lon" numeric coordinates or a place name.
        - Parameters:
            s: str - input string provided by the user or CLI.
        - Returns:
            tuple(float, float) - (latitude, longitude).
        - Behavior:
            If the string contains a comma and both parts can be parsed as floats,
            the function validates the numeric ranges (-90..90 for latitude,
            -180..180 for longitude) and returns them.
            Otherwise, it defers to geocode(s) to resolve the input as a place name.
        - Notes:
            Robust to whitespace and basic formatting errors; returns the first
            geocoding match for place names.

    format_dist_km_mi(km)
        - Purpose:
            Create a human-friendly string representation of a distance given
            in kilometers, including a miles equivalent.
        - Parameters:
            km: float - distance in kilometers.
        - Returns:
            str - formatted string, precision chosen based on magnitude.
        - Behavior:
            Converts kilometers to miles (1 km ≈ 0.62137119223733 mi).
            Uses higher precision for smaller distances and shorter formatting
            for very large distances (>= 1000 km).

    main(argv)
        - Purpose:
            Command-line entry point to accept two place arguments (or prompt
            interactively), resolve them to coordinates, compute the distance,
            and print results.
        - Parameters:
            argv: list - typically sys.argv from the caller; expects at least two
            positional arguments after the program name, otherwise falls back to
            interactive prompts.
        - Behavior:
            1. Read two inputs (from argv or via input()).
            2. Parse or geocode each input to (lat, lon) using parse_point().
            3. Compute distance with haversine().
            4. Print coordinates and a human-readable distance string.
        - Notes:
            - Handles KeyboardInterrupt/EOFError during interactive input by
              exiting cleanly.
            - Prints error information if point resolution fails.
            - Suitable for CLI usage; for library-style usage, import haversine
              and parse_point directly and handle exceptions as needed.

Possible improvements and warnings:
    - Add retry/backoff and caching around geocoding to reduce API load and
      improve robustness against transient network errors.
    - Respect Nominatim's usage policy (identify your application, limit
      request rate, and consider bulk/geocoding alternatives for heavy use).
    - Add unit tests for parse_point edge cases and haversine correctness.
    - Consider improving printed output (e.g., ANSI formatting) or providing
      machine-readable output (JSON) for integration with other tools.
import sys
import math
import json

#!/usr/bin/env python3
"""
Cal-1.py

Calculate distance between two places.
Supports:
- place names (geocoded via Nominatim)
- coordinates in "lat,lon" format

Usage examples:
    python Cal-1.py "New York, NY" "Los Angeles, CA"
    python Cal-1.py "40.7128,-74.0060" "34.0522,-118.2437"
"""

import urllib.parse
import urllib.request

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "DistanceScript/1.0 (GitHub Copilot)"

def haversine(lat1, lon1, lat2, lon2):
        # returns distance in kilometers
        R = 6371.0088  # mean Earth radius in km
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

def geocode(place):
        q = urllib.parse.urlencode({"q": place, "format": "json", "limit": 1})
        req = urllib.request.Request(f"{NOMINATIM_URL}?{q}", headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.load(resp)
        if not data:
                raise ValueError(f"Place not found: {place!r}")
        return float(data[0]["lat"]), float(data[0]["lon"])

def parse_point(s):
        s = s.strip()
        # coordinate? e.g., "lat,lon"
        if "," in s:
                parts = [p.strip() for p in s.split(",")]
                if len(parts) == 2:
                        try:
                                lat = float(parts[0])
                                lon = float(parts[1])
                                if -90 <= lat <= 90 and -180 <= lon <= 180:
                                        return lat, lon
                        except ValueError:
                                pass
        # otherwise treat as place name and geocode
        return geocode(s)

def format_dist_km_mi(km):
        mi = km * 0.62137119223733
        if km >= 1000:
                return f"{km:,.1f} km ({mi:,.1f} mi)"
        return f"{km:,.3f} km ({mi:,.3f} mi)"

def main(argv):
        if len(argv) >= 3:
                a = argv[1]
                b = argv[2]
        else:
                try:
                        a = input("First place (name or lat,lon): ").strip()
                        b = input("Second place (name or lat,lon): ").strip()
                except (KeyboardInterrupt, EOFError):
                        print()
                        return

        try:
                lat1, lon1 = parse_point(a)
                lat2, lon2 = parse_point(b)
        except Exception as e:
                print("Error resolving points:", e)
                return

        km = haversine(lat1, lon1, lat2, lon2)
        print(f"Point A: {lat1:.6f}, {lon1:.6f}")
        print(f"Point B: {lat2:.006f}, {lon2:.006f}")
        print("Distance:", format_dist_km_mi(km))

if __name__ == "__main__":
        main(sys.argv)
