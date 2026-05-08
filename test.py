creeate a simple python code to calculate the area of a circle given its radius.import math
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
        print(e)