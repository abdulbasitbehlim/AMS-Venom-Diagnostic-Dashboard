# AMS Venom Diagnostic Dashboard

A Streamlit-based **educational simulation** of illustrative electronic signal traces for a conceptual snake-venom antigen / scFv biosensor workflow.

> **Important:** This project is not clinically validated and must not be used for snakebite diagnosis, treatment, triage, or patient-care decisions. The amplitudes, concentration labels, timing and peak shapes are synthetic demonstration values rather than experimentally calibrated measurements.

## Features

- **Interactive Dashboard** with clean, wide layout
- **Randomized Venom Data** for 5 major snake species:
  - Spectacled Cobra
  - Common Krait
  - Russell's Viper
  - Saw Scaled Viper
  - King Cobra
- **Species Filtering** via checkboxes in the sidebar
- **Adjustable Sensor Noise** level using a slider
- **Generate New Random Data** button for fresh simulations
- **Annotated Concentration Labels** on the signal peaks
- **Live Sensor Feed Graph** showing Antigen-scFv Binding Kinetics

## Requirements

- Python 3.10 or higher
- streamlit
- numpy
- matplotlib

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abdulbasitbehlim/AMS-Venom-Diagnostic-Dashboard.git
   cd AMS-Venom-Diagnostic-Dashboard
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

```bash
streamlit run demo.py
```

The app will open automatically in your default web browser.

## Project Structure

```
AMS-Venom-Diagnostic-Dashboard/
├── demo.py              # Main Streamlit application
├── README.md            # Project documentation
├── LICENSE              # MIT License
├── .gitignore           # Git ignore rules
└── requirements.txt     # Python dependencies
```

## How It Works

- Each snake species is assigned a random amplitude within an **illustrative simulation range**.
- The displayed concentration is derived from amplitude (`amplitude × 2 ng/mL`) only as a demonstration mapping; it is **not a validated calibration curve**.
- A variable-width Gaussian peak is generated for each selected species to illustrate a possible electronic signal shape.
- Baseline noise is added and can be controlled by the user.
- The resulting signals are plotted with annotations showing the calculated concentration.

## Notes

- Data is randomly generated every time the app runs or when the "Generate New Random Data" button is clicked.
- No output should be interpreted as evidence of envenomation, venom concentration, species identification, or clinical status.
- You can selectively enable/disable individual snake species using the sidebar checkboxes.
- Adjust the "Sensor Baseline Noise Level" slider to see how noise affects the signal clarity.

## Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to fork this repository and submit a pull request.

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
