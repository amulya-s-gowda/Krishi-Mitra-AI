from modules.crop_information import get_crop_information

crops = ["blackgram", "chickpea", "maize"]
languages = ["English", "Kannada"]
fields = ["sowing", "seed_rate", "duration", "irrigation", "harvesting"]

for lang in languages:
    print("\n==========", lang, "==========")
    for crop in crops:
        info = get_crop_information(crop, lang)
        missing = [field for field in fields if not info or not info.get(field)]
        print(crop, ":", "PASS" if not missing else f"MISSING {missing}")
