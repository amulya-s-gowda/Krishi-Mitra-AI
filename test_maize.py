from modules.crop_information import get_crop_information

fields = ["sowing", "seed_rate", "duration", "irrigation", "harvesting"]

for lang in ["English", "Kannada"]:
    info = get_crop_information("maize", lang)

    print("\nLanguage:", lang)
    print("Crop:", info["name"])

    for field in fields:
        print(field, ":", "OK" if info.get(field) else "MISSING")
