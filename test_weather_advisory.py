
from modules.weather_advisory import get_farming_advisory

print("\nTEST 1: ENGLISH - RECENT WEATHER DATA")
print("-------------------------------------")

result = get_farming_advisory(
    rainfall=20,
    temperature=32,
    humidity=85,
    language="English",
    data_is_recent=True
)

for advice in result:
    print("-", advice)


print("\nTEST 2: KANNADA - DELAYED WEATHER DATA")
print("--------------------------------------")

result = get_farming_advisory(
    rainfall=70,
    temperature=36,
    humidity=85,
    language="Kannada",
    data_is_recent=False
)

for advice in result:
    print("-", advice)


print("\nTEST 3: ENGLISH - LOW RAINFALL")
print("------------------------------")

result = get_farming_advisory(
    rainfall=0.5,
    temperature=28,
    humidity=50,
    language="English",
    data_is_recent=True
)

for advice in result:
    print("-", advice)
