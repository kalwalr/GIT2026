#adding comments to be pushed to vs code
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
