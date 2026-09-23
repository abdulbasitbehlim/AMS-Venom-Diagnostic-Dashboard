import random

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


# ------------------------------------------------------------
# 1. PAGE SETUP
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 2. SIDEBAR CONTROLS
# ------------------------------------------------------------

st.sidebar.header("Dashboard Controls")
st.sidebar.write(
    "Filter the sensor data by selecting specific snake species:"
)

# Clicking this button restarts the Streamlit script,
# which generates a fresh set of random amplitudes.
if st.sidebar.button("Generate New Random Data"):
    st.rerun()


# ------------------------------------------------------------
# 3. CREATE RANDOM DEMONSTRATION DATA
# ------------------------------------------------------------

# Each species receives a random signal amplitude.
# These numbers are only for simulation.
amp_cobra = random.randint(10, 55)
amp_krait = random.randint(10, 35)
amp_russell = random.randint(20, 65)
amp_saw = random.randint(5, 30)
amp_king = random.randint(10, 30)


# Store the information for every species in one dictionary.
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


# ------------------------------------------------------------
# 4. LET THE USER CHOOSE WHICH SPECIES TO SHOW
# ------------------------------------------------------------

selected_species = []

for species_name in snake_data:
    is_selected = st.sidebar.checkbox(species_name, value=True)

    if is_selected:
        selected_species.append(species_name)


# ------------------------------------------------------------
# 5. PREPARE THE TIME AXIS AND BASELINE NOISE
# ------------------------------------------------------------

# Create 1000 points from 0 to 100 seconds.
time = np.linspace(0, 100, 1000)

noise_level = st.sidebar.slider(
    "Sensor Baseline Noise Level",
    min_value=0.0,
    max_value=2.0,
    value=0.4,
    step=0.1
)

# Create random baseline noise for the whole signal.
baseline_noise = np.random.normal(
    0,
    noise_level,
    size=len(time)
)


# ------------------------------------------------------------
# 6. BUILD AND PLOT EACH SYNTHETIC SIGNAL
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6))

for species_name in selected_species:
    species = snake_data[species_name]

    amplitude = species["amplitude"]
    concentration = species["concentration"]
    peak_time = species["peak_time"]
    color = species["color"]
    left_width = species["w_left"]
    right_width = species["w_right"]

    # Use one width before the peak and another width after the peak.
    # This produces an asymmetric Gaussian-like signal.
    width_array = np.where(
        time < peak_time,
        left_width,
        right_width
    )

    # Gaussian equation used to create the simulated binding peak.
    distance_from_peak = time - peak_time
    squared_distance = distance_from_peak ** 2
    squared_width = width_array ** 2

    exponent = -squared_distance / (2 * squared_width)
    binding_peak = amplitude * np.exp(exponent)

    # Add the simulated peak on top of the baseline sensor noise.
    total_signal = baseline_noise + binding_peak

    ax.plot(
        time,
        total_signal,
        color=color,
        label=species_name,
        linewidth=2.5
    )

    # Show the illustrative concentration near the top of the peak.
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


# ------------------------------------------------------------
# 7. FORMAT THE GRAPH
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 8. DISPLAY THE RESULT IN STREAMLIT
# ------------------------------------------------------------

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


# Run this project locally using:
# streamlit run demo.py
