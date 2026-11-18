
def get_farming_advisory(
    rainfall,
    temperature,
    humidity,
    language="English",
    data_is_recent=True
):
    """
    Generate general farming suggestions.

    Rainfall is a model estimate.
    Temperature and humidity are recorded observations.
    Data freshness is used to qualify the advisory.
    """

    advisories = []

    # Warn farmers when the available weather data is delayed.
    if not data_is_recent:

        if language == "English":
            advisories.append(
                "WARNING: Weather data is delayed. The rainfall estimate "
                "and recorded weather conditions may not reflect current "
                "conditions. Check your field conditions and the latest "
                "official IMD updates before making farming decisions."
            )
        else:
            advisories.append(
                "ಎಚ್ಚರಿಕೆ: ಹವಾಮಾನ ದತ್ತಾಂಶವು ವಿಳಂಬವಾಗಿದೆ. ಮಳೆಯ ಅಂದಾಜು ಮತ್ತು "
                "ದಾಖಲಾದ ಹವಾಮಾನ ಪರಿಸ್ಥಿತಿಗಳು ಪ್ರಸ್ತುತ ಪರಿಸ್ಥಿತಿಯನ್ನು "
                "ಪ್ರತಿಬಿಂಬಿಸದೇ ಇರಬಹುದು. ಕೃಷಿ ನಿರ್ಧಾರಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುವ ಮೊದಲು "
                "ಹೊಲದ ಪರಿಸ್ಥಿತಿ ಮತ್ತು ಇತ್ತೀಚಿನ ಅಧಿಕೃತ IMD ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ."
            )

    if language == "English":

        # Rainfall-based suggestions
        if rainfall >= 64.5:
            advisories.append(
                "High rainfall is estimated. Check field drainage "
                "and take precautions against waterlogging."
            )
            advisories.append(
                "Avoid unnecessary fertilizer or pesticide spraying "
                "during rainfall. Follow local agricultural guidance."
            )

        elif rainfall < 2.4:
            advisories.append(
                "Very little rainfall is estimated. Check actual soil "
                "moisture and crop water requirements before irrigation."
            )

        elif rainfall < 15.5:
            advisories.append(
                "Light rainfall is estimated. Monitor soil moisture "
                "and plan irrigation according to crop requirements."
            )

        else:
            advisories.append(
                "Moderate rainfall is estimated. Monitor field conditions "
                "and avoid unnecessary irrigation."
            )

        # Temperature-based suggestions
        if temperature >= 35:
            advisories.append(
                "High temperature was recorded in the available weather "
                "data. Monitor crops for heat stress and check soil moisture."
            )

        elif temperature >= 30:
            advisories.append(
                "Warm conditions were recorded. Monitor crops for signs "
                "of water stress, especially during afternoon hours."
            )

        elif temperature < 15:
            advisories.append(
                "Low temperature was recorded. Monitor sensitive crops "
                "for cold-related stress."
            )

        # Humidity-based suggestions
        if humidity >= 80:
            advisories.append(
                "High humidity was recorded. Inspect crops for possible "
                "fungal disease symptoms and maintain proper field ventilation."
            )

        elif humidity < 35:
            advisories.append(
                "Low humidity was recorded. Monitor soil moisture "
                "and watch for signs of crop water stress."
            )

    else:

        # ಮಳೆಯ ಆಧಾರಿತ ಸಲಹೆಗಳು
        if rainfall >= 64.5:
            advisories.append(
                "ಹೆಚ್ಚಿನ ಮಳೆಯ ಅಂದಾಜು ಇದೆ. ಹೊಲದಲ್ಲಿ ನೀರು ನಿಲ್ಲದಂತೆ "
                "ಒಳಚರಂಡಿ ವ್ಯವಸ್ಥೆಯನ್ನು ಪರಿಶೀಲಿಸಿ."
            )
            advisories.append(
                "ಮಳೆಯ ಸಮಯದಲ್ಲಿ ಅನಗತ್ಯವಾಗಿ ಗೊಬ್ಬರ ಅಥವಾ ಕೀಟನಾಶಕಗಳನ್ನು "
                "ಸಿಂಪಡಿಸುವುದನ್ನು ತಪ್ಪಿಸಿ. ಸ್ಥಳೀಯ ಕೃಷಿ ಇಲಾಖೆಯ ಸಲಹೆ ಪಾಲಿಸಿ."
            )

        elif rainfall < 2.4:
            advisories.append(
                "ಬಹಳ ಕಡಿಮೆ ಮಳೆಯ ಅಂದಾಜು ಇದೆ. ನೀರಾವರಿ ಮಾಡುವ ಮೊದಲು "
                "ಮಣ್ಣಿನ ನಿಜವಾದ ತೇವಾಂಶ ಮತ್ತು ಬೆಳೆಯ ನೀರಿನ ಅಗತ್ಯವನ್ನು ಪರಿಶೀಲಿಸಿ."
            )

        elif rainfall < 15.5:
            advisories.append(
                "ಲಘು ಮಳೆಯ ಅಂದಾಜು ಇದೆ. ಮಣ್ಣಿನ ತೇವಾಂಶವನ್ನು ಗಮನಿಸಿ "
                "ಬೆಳೆಯ ಅಗತ್ಯಕ್ಕೆ ಅನುಗುಣವಾಗಿ ನೀರಾವರಿ ಯೋಜಿಸಿ."
            )

        else:
            advisories.append(
                "ಮಧ್ಯಮ ಮಳೆಯ ಅಂದಾಜು ಇದೆ. ಹೊಲದ ಪರಿಸ್ಥಿತಿಯನ್ನು ಗಮನಿಸಿ "
                "ಅನಗತ್ಯ ನೀರಾವರಿಯನ್ನು ತಪ್ಪಿಸಿ."
            )

        # ತಾಪಮಾನದ ಆಧಾರಿತ ಸಲಹೆಗಳು
        if temperature >= 35:
            advisories.append(
                "ಲಭ್ಯವಿರುವ ಹವಾಮಾನ ದತ್ತಾಂಶದಲ್ಲಿ ಹೆಚ್ಚಿನ ತಾಪಮಾನ ದಾಖಲಾಗಿದೆ. "
                "ಬೆಳೆಗಳಲ್ಲಿ ಉಷ್ಣ ಒತ್ತಡದ ಲಕ್ಷಣಗಳನ್ನು ಗಮನಿಸಿ ಮತ್ತು "
                "ಮಣ್ಣಿನ ತೇವಾಂಶ ಪರಿಶೀಲಿಸಿ."
            )

        elif temperature >= 30:
            advisories.append(
                "ಲಭ್ಯವಿರುವ ದತ್ತಾಂಶದಲ್ಲಿ ಬಿಸಿಯಾದ ವಾತಾವರಣ ದಾಖಲಾಗಿದೆ. "
                "ವಿಶೇಷವಾಗಿ ಮಧ್ಯಾಹ್ನದ ಸಮಯದಲ್ಲಿ ಬೆಳೆಗಳಲ್ಲಿ ನೀರಿನ ಕೊರತೆಯ "
                "ಲಕ್ಷಣಗಳನ್ನು ಗಮನಿಸಿ."
            )

        elif temperature < 15:
            advisories.append(
                "ಕಡಿಮೆ ತಾಪಮಾನ ದಾಖಲಾಗಿದೆ. ಚಳಿಯಿಂದ ಸೂಕ್ಷ್ಮ ಬೆಳೆಗಳಿಗೆ "
                "ಆಗುವ ಹಾನಿಯನ್ನು ಗಮನಿಸಿ."
            )

        # ತೇವಾಂಶದ ಆಧಾರಿತ ಸಲಹೆಗಳು
        if humidity >= 80:
            advisories.append(
                "ಹೆಚ್ಚಿನ ತೇವಾಂಶ ದಾಖಲಾಗಿದೆ. ಬೆಳೆಗಳಲ್ಲಿ ಶಿಲೀಂಧ್ರ ರೋಗಗಳ "
                "ಲಕ್ಷಣಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಗಾಳಿಯಾಡುವಿಕೆಯನ್ನು ಕಾಪಾಡಿ."
            )

        elif humidity < 35:
            advisories.append(
                "ಕಡಿಮೆ ತೇವಾಂಶ ದಾಖಲಾಗಿದೆ. ಮಣ್ಣಿನ ತೇವಾಂಶವನ್ನು ಪರಿಶೀಲಿಸಿ "
                "ಬೆಳೆಗಳಲ್ಲಿ ನೀರಿನ ಕೊರತೆಯ ಲಕ್ಷಣಗಳನ್ನು ಗಮನಿಸಿ."
            )

    return advisories
