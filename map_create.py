import numpy as np
from util import write_image

def base_map():
    image = np.zeros((1024, 1024, 3))
    center_x, center_y = 512, 512
    max_dist = np.sqrt((512) ** 2 + (512) ** 2)
    for y in range(1024):
        for x in range(1024):
            dx = x - center_x
            dy = y - center_y
            dist = np.sqrt(dx * dx + dy * dy)

            angle = np.arctan2(dy, dx)

            red = (np.sin(angle) + 1) / 2
            green = (np.sin(angle + 2 * np.pi / 3) + 1) / 2
            blue = (np.sin(angle + 4 * np.pi / 3) + 1) / 2

            closeness = 1 - (dist / max_dist)

            image[y, x, 0] = red + closeness
            image[y, x, 1] = green + closeness
            image[y, x, 2] = blue + closeness

    write_image("map.png", image)


def shifted_map():
    import numpy as np

    # Create 1024x1024x3 array initialized with zeros
    image = np.zeros((1024, 1024, 3))

    # Center point at top-center
    center_x, center_y = 512, 0

    # Maximum possible distance (from top-center to bottom corners)
    max_dist = np.sqrt((512) ** 2 + (1024) ** 2)

    # Iterate through each pixel
    for y in range(1024):
        for x in range(1024):
            # Calculate distance from top-center
            dx = x - center_x
            dy = y - center_y
            dist = np.sqrt(dx * dx + dy * dy)

            # Calculate angle in radians from top-center
            angle = np.arctan2(dy, dx)

            # Map full circle (2π) to semicircle (π)
            # Double the angle and shift to [-π/2, π/2] range
            angle = 2 * angle + np.pi/6
            # Clamp to [-π/2, π/2] to keep it in the downward semicircle


            # Calculate base RGB colors from mapped angle
            red = (np.sin(angle) + 1) / 2
            green = (np.sin(angle + 2 * np.pi / 3) + 1) / 2
            blue = (np.sin(angle + 4 * np.pi / 3) + 1) / 2

            # Calculate closeness (1 at top-center, 0 at farthest points)
            closeness = 1 - (dist / max_dist)*1.75

            # Apply colors with closeness brightness
            image[y, x, 0] = red + closeness  # Red channel
            image[y, x, 1] = green + closeness  # Green channel
            image[y, x, 2] = blue + closeness  # Blue channel

    # Insert your image saving function here
    write_image("map_shifted.png", image)

if __name__ == "__main__":
    shifted_map()
