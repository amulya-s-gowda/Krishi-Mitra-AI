
from modules.crop_information import (
    crop_information,
    crop_information_kn
)

print("TOTAL CROPS:", len(crop_information))
print("KANNADA CROPS:", len(crop_information_kn))

missing = set(crop_information) - set(crop_information_kn)

print("\nMissing Kannada translations:")

for crop in sorted(missing):
    print("-", crop)

if not missing:
    print("\nAll 22 crops have Kannada translations!")
