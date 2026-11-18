# Validation notes for this packaged version

## Passed in the available validation environment

- Python syntax compilation for all project Python files (`python -m compileall -q .`).
- Loading all three active model artifacts: weather rainfall model, crop model with soil-test features, and crop model without rainfall.
- `test_all_crop_fields.py` — English/Kannada crop detail fields for Blackgram, Chickpea and Maize.
- `test_all_climate_profiles.py` — 93 district/season profile checks.
- `test_all_crop_combinations.py` — soil/season recommendation combinations.
- `test_crop_without_soil_test.py` — rule-based recommendation path.
- `test_recommendation_engine.py` — ML recommendation path.
- `test_weather_advisory.py` — English/Kannada advisory and delayed-data warning cases.
- `test_weather_alerts.py` — rainfall alert categories and Kannada output.
- `test_district_data.py` — district coordinate data.
- `test_crop_model.py` and `test_crop_without_rainfall.py` — crop model inference checks.

## Not fully verified here

- The complete Streamlit browser app was not launched in this packaging environment because Streamlit and `streamlit-mic-recorder` are not installed here, and package installation was blocked by unavailable network access.
- Live NASA POWER requests and live Google Text-to-Speech/microphone interaction were not re-tested in this packaging environment. They require internet/browser microphone access.
- The model artifacts report that they were serialized with scikit-learn 1.9.1. `requirements.txt` pins that version; using a different scikit-learn version can cause compatibility warnings or failures.

Run the setup instructions in `README.md`, then launch the app and perform the final browser check on the target Windows machine before the project demonstration.
