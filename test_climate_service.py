
from modules.climate_service import get_seasonal_climate

district = "Shivamogga"

seasons = ["Kharif", "Rabi", "Summer"]

print("\nKRISHIMITRA AI - SEASONAL CLIMATE REPORT")
print("----------------------------------------")

for season in seasons:

    climate = get_seasonal_climate(district, season)

    print("\nDistrict:", district)
    print("Season:", season)
    print("Average Rainfall:", climate["rainfall"], "mm/day")
    print("Average Temperature:", climate["temperature"], "°C")
    print("Average Humidity:", climate["humidity"], "%")
