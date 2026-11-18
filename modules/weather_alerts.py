
def get_weather_alert(rainfall, language="English"):

    # Prevent negative rainfall estimates from being displayed.
    rainfall = max(0.0, float(rainfall))

    if rainfall == 0:
        category = "No Rain"
        category_kn = "ಮಳೆ ಇಲ್ಲ"
        advice = (
            "No rainfall is indicated by the model. "
            "Check soil moisture before irrigation."
        )
        advice_kn = (
            "ಮಳೆಯ ಸೂಚನೆ ಇಲ್ಲ. ನೀರಾವರಿ ಮಾಡುವ ಮೊದಲು "
            "ಮಣ್ಣಿನ ತೇವಾಂಶವನ್ನು ಪರಿಶೀಲಿಸಿ."
        )

    elif rainfall <= 2.4:
        category = "Very Light Rain"
        category_kn = "ಅತಿ ಕಡಿಮೆ ಮಳೆ"
        advice = (
            "Very light rainfall is indicated. "
            "Continue normal field monitoring."
        )
        advice_kn = (
            "ಅತಿ ಕಡಿಮೆ ಮಳೆಯ ಸೂಚನೆ ಇದೆ. "
            "ಹೊಲವನ್ನು ಸಾಮಾನ್ಯವಾಗಿ ಪರಿಶೀಲಿಸುತ್ತಿರಿ."
        )

    elif rainfall <= 15.5:
        category = "Light Rain"
        category_kn = "ಹಗುರ ಮಳೆ"
        advice = (
            "Light rainfall is indicated. "
            "Monitor soil moisture and avoid unnecessary irrigation."
        )
        advice_kn = (
            "ಹಗುರ ಮಳೆಯ ಸೂಚನೆ ಇದೆ. ಮಣ್ಣಿನ ತೇವಾಂಶ ಪರಿಶೀಲಿಸಿ. "
            "ಅಗತ್ಯವಿಲ್ಲದ ನೀರಾವರಿಯನ್ನು ತಪ್ಪಿಸಿ."
        )

    elif rainfall <= 64.4:
        category = "Moderate Rain"
        category_kn = "ಮಧ್ಯಮ ಮಳೆ"
        advice = (
            "Moderate rainfall is indicated. "
            "Check field drainage and avoid water stagnation."
        )
        advice_kn = (
            "ಮಧ್ಯಮ ಮಳೆಯ ಸೂಚನೆ ಇದೆ. ಹೊಲದಲ್ಲಿ ನೀರು ಹರಿದುಹೋಗುವ "
            "ವ್ಯವಸ್ಥೆಯನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳಿ."
        )

    elif rainfall <= 115.5:
        category = "Heavy Rain"
        category_kn = "ಭಾರಿ ಮಳೆ"
        advice = (
            "Heavy rainfall is indicated by the model. "
            "Check drainage, protect stored seeds and fertilizers, "
            "and follow official weather advisories."
        )
        advice_kn = (
            "ಭಾರಿ ಮಳೆಯ ಸೂಚನೆ ಇದೆ. ನೀರು ಹರಿದುಹೋಗುವ ವ್ಯವಸ್ಥೆ ಪರಿಶೀಲಿಸಿ. "
            "ಸಂಗ್ರಹಿಸಿದ ಬೀಜ ಮತ್ತು ರಸಗೊಬ್ಬರಗಳನ್ನು ಸುರಕ್ಷಿತವಾಗಿಡಿ. "
            "ಅಧಿಕೃತ ಹವಾಮಾನ ಸಲಹೆಗಳನ್ನು ಅನುಸರಿಸಿ."
        )

    elif rainfall <= 204.4:
        category = "Very Heavy Rain"
        category_kn = "ಅತಿ ಭಾರಿ ಮಳೆ"
        advice = (
            "Very heavy rainfall is indicated. "
            "Take precautions against waterlogging and follow "
            "official weather and safety advisories."
        )
        advice_kn = (
            "ಅತಿ ಭಾರಿ ಮಳೆಯ ಸೂಚನೆ ಇದೆ. ಹೊಲದಲ್ಲಿ ನೀರು ನಿಲ್ಲದಂತೆ "
            "ಮುನ್ನೆಚ್ಚರಿಕೆ ವಹಿಸಿ. ಅಧಿಕೃತ ಹವಾಮಾನ ಮತ್ತು ಸುರಕ್ಷತಾ "
            "ಸಲಹೆಗಳನ್ನು ಅನುಸರಿಸಿ."
        )

    else:
        category = "Extremely Heavy Rain"
        category_kn = "ಅತ್ಯಂತ ಭಾರಿ ಮಳೆ"
        advice = (
            "Extremely heavy rainfall is indicated by the model. "
            "Check official IMD alerts immediately and follow "
            "local administration safety instructions."
        )
        advice_kn = (
            "ಅತ್ಯಂತ ಭಾರಿ ಮಳೆಯ ಸೂಚನೆ ಇದೆ. ತಕ್ಷಣ ಅಧಿಕೃತ IMD "
            "ಎಚ್ಚರಿಕೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಸ್ಥಳೀಯ ಆಡಳಿತದ "
            "ಸುರಕ್ಷತಾ ಸೂಚನೆಗಳನ್ನು ಅನುಸರಿಸಿ."
        )

    if language == "ಕನ್ನಡ":
        return {
            "category": category_kn,
            "advice": advice_kn,
            "rainfall": rainfall
        }

    return {
        "category": category,
        "advice": advice,
        "rainfall": rainfall
    }
