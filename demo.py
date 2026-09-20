import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# Web App Configuration and Header
st.set_page_config(page_title="AMS Venom Diagnostic Dashboard", layout="wide")
st.title("🐍 AMS Venom Signal Simulation Dashboard")
st.warning(
    "Educational simulation only — not clinically validated and not intended for "
    "snakebite diagnosis, treatment, triage, or patient-care decisions."
)
st.markdown("""
This dashboard generates **synthetic illustrative signals** inspired by a conceptual
antigen–scFv biosensor workflow. The amplitudes, concentrations, peak shapes and timing
used here are simulated for demonstration and are **not calibrated measurements from a
validated AMS Venomics diagnostic device**.
""")

# Sidebar for User Interaction
st.sidebar.header("Dashboard Controls")
st.sidebar.write("Filter the sensor data by selecting specific snake species:")

# Add a button so the user can easily force new random data without restarting the whole app
if st.sidebar.button("Generate New Random Data"):
    st.rerun()

# Generate Random Data
# We use random.randint to select a random amplitude between a specific range.
# Concentration is calculated from amplitude only as an illustrative demo mapping; it is not a validated calibration curve.
amp_cobra = random.randint(10, 55)
amp_krait = random.randint(10, 35)
amp_russell = random.randint(20, 65)
amp_saw = random.randint(5, 30)
amp_king = random.randint(10, 30)

snake_data = {
    "Spectacled Cobra": {"amplitude": amp_cobra, "concentration": f"{amp_cobra * 2} ng/mL", "peak_time": 20, "w_left": 2, "w_right": 8, "color": "blue"},
    "Common Krait": {"amplitude": amp_krait, "concentration": f"{amp_krait * 2} ng/mL", "peak_time": 40, "w_left": 5, "w_right": 2, "color": "green"},
    "Russell's Viper": {"amplitude": amp_russell, "concentration": f"{amp_russell * 2} ng/mL", "peak_time": 60, "w_left": 1.5, "w_right": 1.5, "color": "red"}, 
    "Saw Scaled Viper": {"amplitude": amp_saw, "concentration": f"{amp_saw * 2} ng/mL", "peak_time": 75, "w_left": 8, "w_right": 4, "color": "orange"},
    "King Cobra": {"amplitude": amp_king, "concentration": f"{amp_king * 2} ng/mL", "peak_time": 90, "w_left": 3, "w_right": 10, "color": "purple"}
}

# Create checkboxes in the sidebar for each species (all checked by default)
selected_species = []
for species in snake_data.keys():
    if st.sidebar.checkbox(species, value=True):
        selected_species.append(species)

# Data Generation (Mathematical Logic)
time = np.linspace(0, 100, 1000)
# Add a slider to let the user adjust baseline noise
noise_level = st.sidebar.slider("Sensor Baseline Noise Level", min_value=0.0, max_value=2.0, value=0.4, step=0.1)
baseline_noise = np.random.normal(0, noise_level, size=len(time))

# Plotting the Graph
fig, ax = plt.subplots(figsize=(12, 6))

for species in selected_species:
    params = snake_data[species]
    amp = params["amplitude"]
    conc = params["concentration"]
    pt = params["peak_time"]
    color = params["color"]
    w_left = params["w_left"]
    w_right = params["w_right"]
    
    # Create the unexpected, variable Gaussian nature
    width_array = np.where(time < pt, w_left, w_right)
    variable_gaussian = amp * np.exp(-((time - pt)**2) / (2 * width_array**2))
    
    # Add binding peak to baseline noise
    total_signal = baseline_noise + variable_gaussian
    
    # Plotting
    ax.plot(time, total_signal, color=color, label=f'{species}', linewidth=2.5)
    
    # Annotate random concentration directly above the random peak
    ax.annotate(f'{conc}', 
                 xy=(pt, amp + noise_level + 1), 
                 ha='center', va='bottom', color=color, fontweight='bold', fontsize=11)

# Formatting the graph
ax.set_title('Synthetic Sensor Signal Simulation', fontsize=14, pad=15)
ax.set_xlabel('Time (seconds)', fontsize=12)
ax.set_ylabel('Electronic Signal (Arbitrary Units)', fontsize=12)
if selected_species:
    ax.legend(loc='upper right', title="Simulated Species")
ax.grid(True, linestyle='--', alpha=0.6)

# Render the plot in the Streamlit Web App
st.pyplot(fig)

# Add a success message below the graph
if selected_species:
    st.info("Simulation complete: illustrative signal traces generated for the selected species.")
else:
    st.info("Select at least one species to display simulated signal traces.")

# Run locally with: streamlit run demo.py