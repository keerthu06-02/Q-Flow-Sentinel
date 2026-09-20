# 🚦 Q-Flow Sentinel

## Quantum-Enhanced Predictive & Self-Healing Urban Traffic Network

Q-Flow Sentinel is a hybrid classical-quantum urban traffic optimization prototype designed to monitor, predict, optimize, and respond to changing traffic conditions across connected urban intersections.

The system combines classical traffic analysis with a quantum optimization component to explore improved traffic signal timings.

# 📌 Project Overview

Urban traffic networks can experience rapidly changing traffic conditions because of congestion, accidents, road closures, traffic surges, and emergency vehicle movement.

Q-Flow Sentinel provides a simulation-based solution that combines:

* Live traffic monitoring
* Traffic prediction
* Dynamic event simulation
* Emergency vehicle routing
* Emergency Green Corridor
* Classical traffic signal optimization
* Quantum QUBO/QAOA-style optimization
* Classical vs Quantum comparison
* Environmental analysis
* Interactive Streamlit dashboard

The project is designed as a working prototype for demonstrating how quantum optimization can be integrated with a classical traffic management system.

# 🎯 Problem Statement

The project addresses the problem of optimizing traffic signals across multiple connected intersections while responding to changing traffic conditions.

The system considers traffic density and queue conditions when calculating signal timings.

It also supports special situations such as:

* Traffic congestion
* Accidents
* Road closures
* Traffic surges
* Emergency vehicle arrival

The objective is to demonstrate how a hybrid classical-quantum system can be used for adaptive urban traffic optimization.

# 💡 Key Features

## 1. 📡 Live Traffic Monitoring

The system simulates traffic conditions at six connected intersections:
J1
J2
J3
J4
J5
J6

##  2. 🔮 Traffic Prediction

Q-Flow Sentinel stores previous traffic values for each junction.

The prediction module uses recent traffic history to estimate the next traffic level.

The prediction system calculates the average change in traffic and uses it to estimate the next traffic condition.

##  3. 🚨 Dynamic Event Simulation

The system can simulate unexpected traffic events.

Available events include:
🚧 Accident

An accident increases traffic and queue conditions.

🚫 Road Closure

A road closure produces a larger traffic impact and can block an emergency route.

🚗 Traffic Surge

A traffic surge increases the traffic density and queue.

🔄 Automatic Event Recovery

Events do not require a manual clear button.

The system stores the original traffic condition before an event occurs.

When the simulated traffic returns to the original level, the system automatically restores the original traffic and queue values.

This demonstrates a basic self-healing traffic behavior.

## 4. Emergency Green Corridor

Q-Flow Sentinel provides an emergency vehicle routing system.

The user selects:

Emergency Vehicle Start
Emergency Vehicle Destination

The system then searches the connected traffic network for a route.

The emergency routing system uses the network structure to determine a route between the selected intersections.

When an emergency corridor is activated, the selected route is highlighted on the traffic map.

🚧 Road Closure Awareness

If a road closure event is active, the affected junction is treated as blocked.

The emergency routing system avoids the closed junction.

If no safe route exists, the system displays:

No safe emergency route is available.

The system does not intentionally route the emergency vehicle through the closed junction.

🚑 Emergency Travel-Time Analysis

The system calculates:

Normal travel time
Emergency travel time
Estimated time saving

The emergency travel-time calculation is based on the simulated traffic conditions and the selected route.

This provides a visual representation of the emergency green corridor and its estimated effect on travel time.

## 5. Classical Traffic Signal Optimization

The classical optimization module calculates traffic pressure using:

Traffic Pressure =
Traffic Density + (2 × Queue Length)

The calculated traffic pressure is used to determine optimized green-light durations.

The classical optimizer provides:

Current green time
Optimized green time
Change in green time

The system can also apply the calculated classical timings to the simulated traffic network.

⏱️ Waiting-Time Estimation

The project estimates traffic waiting time using:

Traffic density
Queue length
Green-light duration

The dashboard displays estimated waiting-time values before and after optimization.

This allows the effect of classical signal optimization to be observed in the simulation.

## 6. Quantum Traffic Optimization

The quantum module converts traffic signal timing decisions into a QUBO representation.

QUBO stands for:

Quadratic Unconstrained Binary Optimization

The system creates possible green-light timing choices and represents them using binary variables.

The available green-light options are:

15 seconds
30 seconds
45 seconds
60 seconds

The quantum optimization module evaluates these choices using a quantum circuit.

🧮 QUBO Model

The QUBO model uses traffic pressure as part of the optimization objective.

For each junction, the system considers:

Traffic Density
Queue Length
Green-Light Duration

Traffic pressure is calculated as:

Pressure = Traffic + (2 × Queue)

The QUBO model also includes a penalty for selecting multiple green-light options for the same junction.

The resulting binary optimization problem represents possible signal timing decisions.

## 7. Quantum Circuit

The project uses:

Qiskit
Qiskit Aer

to run the quantum circuit.

The quantum solver:

Creates the quantum circuit.
Initializes qubits.
Applies quantum gates.
Measures the qubits.
Collects measurement results.
Evaluates the resulting bitstrings.
Decodes the selected green-light timing.

The result contains information such as:

Quantum green time
QUBO cost
Quantum bitstring
Gamma
Beta

The current implementation uses a simplified quantum circuit to demonstrate the quantum optimization workflow.

## 8. Classical vs Quantum Comparison

After quantum optimization is executed, the dashboard displays a comparison between the classical and quantum approaches.

The comparison includes:

Junction
Current Green Time
Classical Green Time
Quantum Green Time

The system also calculates estimated waiting time for:

Classical Optimization
Quantum Optimization

The results are displayed using dashboard metrics and a chart.

This allows the user to observe the differences between the two optimization approaches within the simulation.

## 9. Environmental Analysis

Q-Flow Sentinel also includes environmental analysis.

The system calculates environmental metrics based on the simulated traffic conditions.

The dashboard displays:

Throughput
Estimated fuel consumption
Estimated CO₂ emissions

The environmental results can be compared between:

Current
Classical
Quantum

This helps demonstrate how traffic optimization can also be analyzed from an environmental perspective.

## 10. Interactive Traffic Map

The dashboard contains a traffic network map.

The project supports a custom map image named:

traffic_map.png

The image should be placed in the same folder as:

app.py

Example:

Q_Flow_Sentinel/
│
├── app.py
├── traffic_map.png
└── ...

The application loads the image and displays traffic information on top of the map.

Emergency routes are highlighted when an emergency corridor is activated.

## PROJECT ARCHITECTURE
Q_Flow_Sentinel
│
├── app.py
│
├── prediction
│   └── traffic_prediction.py
│
├── simulation
│   ├── traffic_network.py
│   ├── event_simulator.py
│   └── emergency_corridor.py
│
├── optimization
│   └── traffic_optimizer.py
│
├── quantum
│   ├── traffic_qubo.py
│   └── qaoa_solver.py
│
├── utils
│   └── environmental_metrics.py
│
├── data
│
└── traffic_map.png

## INSTALLATION

### Step 1: Install Python

Install Python 3.x on your computer.

Verify the installation:
python --version

### Step 2: Open the Project Folder

Open a terminal inside the project folder.

Example:
cd Q_Flow_Sentinel

### Step 3: Install Required Packages

Run:
pip install streamlit pandas networkx plotly qiskit qiskit-aer

If your project contains additional dependencies, install them as required.
▶️ Running the Application

From the project folder, run:
streamlit run app.py

Streamlit will start the application and provide a local web address.
Open the displayed address in a browser.

## How to Use the Dashboard

### Step 1 — Monitor Traffic

Open the application.
The traffic table displays the current condition of all six intersections.

Click:
🔄 Update Traffic
to simulate changing traffic conditions.

### Step 2 — View Traffic Prediction

Scroll to:
🔮 Traffic Prediction
The system displays the current and predicted traffic values.

### Step 3 — Simulate an Event

Go to:
🚨 Dynamic Event Simulation

Select:
Accident
Road Closure
Traffic Surge

Then select the affected junction.
Click:
🚨 Trigger Event

The traffic condition changes according to the selected event.
The event can then recover automatically when the simulated traffic returns toward its original condition.

### Step 4 — Test Emergency Routing

Go to:
🚑 Emergency Green Corridor

Select:
Emergency Vehicle Start
Emergency Vehicle Destination

Click:
🚑 Activate Emergency Corridor
The system calculates a route.
If a road closure blocks the route, the system attempts to find an alternative safe route.

### Step 5 — Run Classical Optimization

Go to:
⚙️ Classical Traffic Signal Optimization
The system calculates optimized green-light timings.

You can view:
Current Green Time
Optimized Green Time
Change

You can also apply the classical optimized timings using:
⚙️ Apply Classical Optimized Signal Timings
Step 6 — Run Quantum Optimization

Go to:
⚛️ Quantum Traffic Optimization

Click:
⚛️ Run Quantum Optimization
The system creates a QUBO model and runs the quantum circuit.
The dashboard then displays:

Junction
Quantum Green Time
QUBO Cost
Quantum Bitstring
Gamma
Beta

### Step 7 — Compare Results

After running quantum optimization, go to:
📊 Classical vs Quantum Comparison
The system displays the green-light timings and estimated waiting times from both approaches.
A comparison chart is also displayed.

### Step 8 — View Environmental Analysis

Scroll to:
Environmental Analysis
The dashboard displays:

Throughput
Fuel Consumption
CO₂ Emissions

Finally the system also provides a comparison between current, classical, and quantum configurations.




