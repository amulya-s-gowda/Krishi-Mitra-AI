# Krishi-Mitra AI 🌱

A Karnataka-focused smart farming assistant built with Streamlit. It combines district-aware weather data, rainfall estimation, crop recommendations, crop information in English and Kannada, and a voice question-and-answer interface.

## Features included

- English and Kannada interface options.
- District selection for 31 Karnataka districts.
- Seasonal climate summaries from the bundled district/season dataset.
- Weather data retrieval from the NASA POWER daily API.
- Machine-learning rainfall estimation using the bundled trained model.
- Weather freshness checks and delayed-data warnings.
- General farming advisories and rainfall alerts in English and Kannada.
- Crop recommendation using soil-test inputs when available.
- Rule-based district, soil and season-aware crop suggestions when a soil report is not available.
- Crop farming information including sowing time, seed-rate guidance, crop duration, irrigation and harvesting for supported crop entries.
- Voice question input and text-to-speech responses in English and Kannada (requires microphone permission and internet access).
- Test scripts for crop information, recommendations, climate profiles and weather advisories.

## Requirements

- Windows 10/11 (instructions below use PowerShell)
- Python 3.13 recommended for the supplied environment
- Internet connection for NASA POWER weather data and Google Text-to-Speech
- Microphone permission for voice input

The supplied serialized machine-learning models were saved with **scikit-learn 1.9.1**. Install that version to avoid model-version incompatibility warnings or errors.

## Setup on Windows

Open PowerShell in the extracted project folder (the folder containing `app.py`) and run:

```powershell
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, run this once in the same PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## Run the application

From the project root folder:

```powershell
streamlit run app.py --server.port 8511
```

Then open the local URL shown in the terminal (normally `http://localhost:8511`). Keep the terminal open while using the app. Press `Ctrl+C` in the terminal to stop it.

## Run the included checks

With the virtual environment activated:

```powershell
python -m compileall -q .
python test_all_crop_fields.py
python test_all_climate_profiles.py
python test_all_crop_combinations.py
python test_crop_without_soil_test.py
python test_weather_advisory.py
python test_weather_alerts.py
python test_district_data.py
```

Some weather tests call the live NASA POWER service and therefore need internet access. They may fail temporarily if the external service is unavailable.

## Data and model notes

- Weather CSV files and trained `.pkl` model files are included in this project.
- The active rainfall model is `weather_prediction_model.pkl`.
- The active crop recommendation models are `crop_recommendation_model.pkl` and `crop_recommendation_model_no_rainfall.pkl`.
- Other weighted-model artifacts and analysis scripts are retained for project evaluation/experimentation; they are not the active rainfall model used by the app.
- NASA POWER daily data can be delayed. The application displays a warning when the latest available data is not recent. A model estimate based on delayed data must not be treated as a live official forecast.
- Crop suggestions are preliminary decision support, not guaranteed yield predictions or a substitute for local agricultural/KVK advice. Seed rates and crop practices can vary by variety and district.

## Troubleshooting

**`ModuleNotFoundError`**: Activate `venv` and run `pip install -r requirements.txt` again.

**Model/scikit-learn version warning**: Confirm `python -c "import sklearn; print(sklearn.__version__)"` reports `1.9.1` inside the active environment.

**Weather information unavailable**: Check internet access and retry later. NASA POWER may be temporarily unavailable; use current official IMD information for time-sensitive decisions.

**Voice input does not start**: Allow microphone access in the browser, use a supported desktop browser, and check the internet connection. Text-based questions remain available.

## Project structure

- `app.py` — Streamlit user interface and application flow
- `modules/` — weather, climate, crop information, recommendation and voice features
- `models/` — crop recommendation model-loading and inference code
- `data/` — district weather/climate datasets and crop dataset
- `*.pkl` — trained machine-learning model artifacts
- `test_*.py` — project validation scripts
- `requirements.txt` — Python dependencies
