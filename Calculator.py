from math import radians, sin, cos, sqrt, asin

#This is simple calculator application
#updated code to calculate in kilometers and miles using haversine formula
create a simple python code to calculate the area of a circle given its radius.import math
def calculate_circle_area(radius):
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    area = math.pi * (radius ** 2)
    return area
# Example usage:
if __name__ == "__main__":
    # Example usage: prompt the user for a radius and print the computed area.
    # We catch ValueError to handle invalid numeric input or negative radius.
    try:
        radius = float(input("Enter the radius of the circle: "))
        area = calculate_circle_area(radius)
        print(f"The area of the circle with radius {radius} is: {area:.2f}")
    except ValueError as e:
        print(e)ˆ
        def haversine_km(lat1, lon1, lat2, lon2):
            # Haversine formula to calculate great-circle distance between two points
            # given in decimal degrees; returns distance in kilometers.
            lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a))
            earth_radius_km = 6371.0
            return earth_radius_km * c

        try:
            coords = input("Enter lat1, lon1, lat2, lon2 (degrees, comma-separated): ")
            lat1, lon1, lat2, lon2 = map(float, coords.split(","))
            distance = haversine_km(lat1, lon1, lat2, lon2)
            print(f"Distance between points: {distance:.3f} km")
        except Exception as ex:
            print("Could not compute distance:", ex)

