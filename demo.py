import random

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="AMS Venom Diagnostic Dashboard",
    layout="wide"
)

st.title("🐍 AMS Venom Signal Simulation Dashboard")

st.warning(
    "Educational simulation only — not clinically validated and not intended "
    "for snakebite diagnosis, treatment, triage, or patient-care decisions."
)

st.markdown(
    """
This dashboard generates **synthetic illustrative signals** inspired by a conceptual
antigen–scFv biosensor workflow. The amplitudes, concentrations, peak shapes and timing
used here are simulated for demonstration and are **not calibrated measurements from a
validated AMS Venomics diagnostic device**.
"""
)

st.sidebar.header("Dashboard Controls")
st.sidebar.write(
    "Filter the sensor data by selecting specific snake species:"
)

if st.sidebar.button("Generate New Random Data"):
    st.rerun()

amp_cobra = random.randint(10, 55)
amp_krait = random.randint(10, 35)
amp_russell = random.randint(20, 65)
amp_saw = random.randint(5, 30)
amp_king = random.randint(10, 30)

snake_data = {
    "Spectacled Cobra": {
        "amplitude": amp_cobra,
        "concentration": f"{amp_cobra * 2} ng/mL",
        "peak_time": 20,
        "w_left": 2,
        "w_right": 8,
        "color": "blue"
    },
    "Common Krait": {
        "amplitude": amp_krait,
        "concentration": f"{amp_krait * 2} ng/mL",
        "peak_time": 40,
        "w_left": 5,
        "w_right": 2,
        "color": "green"
    },
    "Russell's Viper": {
        "amplitude": amp_russell,
        "concentration": f"{amp_russell * 2} ng/mL",
        "peak_time": 60,
        "w_left": 1.5,
        "w_right": 1.5,
        "color": "red"
    },
    "Saw Scaled Viper": {
        "amplitude": amp_saw,
        "concentration": f"{amp_saw * 2} ng/mL",
        "peak_time": 75,
        "w_left": 8,
        "w_right": 4,
        "color": "orange"
    },
    "King Cobra": {
        "amplitude": amp_king,
        "concentration": f"{amp_king * 2} ng/mL",
        "peak_time": 90,
        "w_left": 3,
        "w_right": 10,
        "color": "purple"
    }
}

selected_species = []

for species_name in snake_data:
    is_selected = st.sidebar.checkbox(species_name, value=True)

    if is_selected:
        selected_species.append(species_name)

time = np.linspace(0, 100, 1000)

noise_level = st.sidebar.slider(
    "Sensor Baseline Noise Level",
    min_value=0.0,
    max_value=2.0,
    value=0.4,
    step=0.1
)

baseline_noise = np.random.normal(
    0,
    noise_level,
    size=len(time)
)

fig, ax = plt.subplots(figsize=(12, 6))

for species_name in selected_species:
    species = snake_data[species_name]

    amplitude = species["amplitude"]
    concentration = species["concentration"]
    peak_time = species["peak_time"]
    color = species["color"]
    left_width = species["w_left"]
    right_width = species["w_right"]

    # Use different widths on each side to create an asymmetric peak.
    width_array = np.where(
        time < peak_time,
        left_width,
        right_width
    )

    distance_from_peak = time - peak_time
    squared_distance = distance_from_peak ** 2
    squared_width = width_array ** 2

    exponent = -squared_distance / (2 * squared_width)
    binding_peak = amplitude * np.exp(exponent)

    total_signal = baseline_noise + binding_peak

    ax.plot(
        time,
        total_signal,
        color=color,
        label=species_name,
        linewidth=2.5
    )

    label_height = amplitude + noise_level + 1

    ax.annotate(
        concentration,
        xy=(peak_time, label_height),
        ha="center",
        va="bottom",
        color=color,
        fontweight="bold",
        fontsize=11
    )

ax.set_title(
    "Synthetic Sensor Signal Simulation",
    fontsize=14,
    pad=15
)

ax.set_xlabel("Time (seconds)", fontsize=12)
ax.set_ylabel("Electronic Signal (Arbitrary Units)", fontsize=12)

if selected_species:
    ax.legend(
        loc="upper right",
        title="Simulated Species"
    )

ax.grid(
    True,
    linestyle="--",
    alpha=0.6
)

st.pyplot(fig)

if selected_species:
    st.info(
        "Simulation complete: illustrative signal traces generated "
        "for the selected species."
    )
else:
    st.info(
        "Select at least one species to display simulated signal traces."
    )

# Run locally with: streamlit run demo.py
