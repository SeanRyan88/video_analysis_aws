import numpy as np

# # Version 2
def calculate_angle(a, b, c):
    print("Run Process calculate_angle")
    a = np.array(a)  # Shoulder
    b = np.array(b)  # Elbow
    c = np.array(c)  # Wrist
    
    # Create vectors from points
    ba = a - b
    bc = c - b
    
    # Calculate the cosine angle using the dot product
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    
    # Take the arc cosine of the cosine_angle to find the angle in radians
    angle = np.arccos(cosine_angle)
    
    # Convert the angle to degrees
    angle = np.degrees(angle)
    
    return angle

# Example usage:
# a, b, c are tuples or lists containing the x, y (and z if in 3D) coordinates of the shoulder, elbow, and wrist respectively.
# angle = calculate_angle(a, b, c)

