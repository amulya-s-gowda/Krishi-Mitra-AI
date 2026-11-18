from modules.district_data import district_coordinates

print("TOTAL DISTRICTS:", len(district_coordinates))

district = "Shivamogga"

latitude, longitude = district_coordinates[district]

print("Selected district:", district)
print("Latitude:", latitude)
print("Longitude:", longitude)