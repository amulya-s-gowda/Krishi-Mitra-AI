
from modules.weather_alerts import get_weather_alert

test_values = [
    0,
    1.5,
    10,
    30,
    80,
    150,
    220
]

print("\nKRISHIMITRA AI")
print("WEATHER ALERT TEST")
print("=" * 40)

for rainfall in test_values:

    result = get_weather_alert(
        rainfall,
        language="English"
    )

    print(f"\nPredicted Rainfall: {rainfall} mm")
    print("Category:", result["category"])
    print("Advice:", result["advice"])

print("\nKannada Test:")

result_kn = get_weather_alert(
    30,
    language="ಕನ್ನಡ"
)

print("Category:", result_kn["category"])
print("Advice:", result_kn["advice"])
