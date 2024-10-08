import numpy as np

class EndoCalculations:
    def __init__(self):
        pass

    def crown_to_root_ratio(self, crown_length, root_length):
        """Calculate the crown-to-root ratio."""
        return crown_length / root_length if root_length != 0 else None

    def root_canal_volume(self, radius, length):
        """Calculate the volume of the root canal using the formula for a cylinder."""
        volume = np.pi * (radius ** 2) * length
        return volume

    def pulp_chamber_volume(self, radius, height):
        """Estimate the volume of the pulp chamber, approximated as a cone."""
        volume = (1/3) * np.pi * (radius ** 2) * height
        return volume

    def anesthesia_dosage(self, weight, dosage_per_kg):
        """Calculate the required dosage of local anesthetics based on weight."""
        return weight * dosage_per_kg

    def success_rate(self, successes, total_treatments):
        """Calculate the treatment success rate as a percentage."""
        return (successes / total_treatments) * 100 if total_treatments != 0 else 0

    def failure_rate(self, failures, total_treatments):
        """Calculate the treatment failure rate as a percentage."""
        return (failures / total_treatments) * 100 if total_treatments != 0 else 0

    def surface_area_of_tooth(self, height, radius):
        """Calculate the surface area of a tooth assuming it is conical."""
        slant_height = np.sqrt(height ** 2 + radius ** 2)
        surface_area = np.pi * radius * (radius + slant_height)  # Lateral surface area + base area
        return surface_area

    def average_root_canal_curvature(self, angles):
        """Calculate the average curvature of root canals based on a list of angles in degrees."""
        if not angles:
            return None
        return np.mean(angles)

    def convert_length_units(self, length, from_unit, to_unit):
        """Convert lengths between mm, cm, and inches."""
        unit_conversions = {
            'mm': 1,
            'cm': 10,
            'inches': 25.4
        }
        if from_unit not in unit_conversions or to_unit not in unit_conversions:
            raise ValueError("Invalid unit. Use 'mm', 'cm', or 'inches'.")
        return length * (unit_conversions[from_unit] / unit_conversions[to_unit])

    def calculate_canal_diameter(self, volume, length):
        """Calculate the diameter of the canal given its volume and length."""
        radius = (volume / (np.pi * length)) ** (1/2)  # Solve for radius
        return radius * 2  # Return diameter
