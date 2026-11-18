import pandas as pd

from modules.climate_service import get_seasonal_climate
from modules.district_data import district_coordinates

seasons = ["Kharif", "Rabi", "Summer"]

print("\nKRISHIMITRA AI - CLIMATE DATA VALIDATION")
print("----------------------------------------")

total_tests = 0
successful_tests = 0
failed_tests = []

for district in district_coordinates:

    for season in seasons:

        total_tests += 1

        try:
            climate = get_seasonal_climate(district, season)

            if all(
                isinstance(value, (int, float))
                for value in climate.values()
            ):
                successful_tests += 1
            else:
                failed_tests.append(f"{district} - {season}")

        except Exception as error:
            failed_tests.append(
                f"{district} - {season}: {error}"
            )

print("\nTOTAL TESTS:", total_tests)
print("SUCCESSFUL:", successful_tests)
print("FAILED:", len(failed_tests))

if failed_tests:
    print("\nFAILED TESTS:")
    for item in failed_tests:
        print(item)
else:
    print("\nAll district-season climate profiles are working!")