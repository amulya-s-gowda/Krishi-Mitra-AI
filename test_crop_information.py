
from modules.crop_information import get_crop_information

crops = ["jute", "coffee", "maize"]

for crop in crops:
    info = get_crop_information(crop)

    print("\nCROP:", info["name"].upper())
    print("Season:", info["season"])
    print("Suitable soil:", info["soil"])
    print("Water needs:", info["water"])

    print("Farming guidance:")
    for point in info["guidance"]:
        print("-", point)

    print("Karnataka note:", info["karnataka_note"])
