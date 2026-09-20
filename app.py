# ============================================================
# Q-FLOW SENTINEL
# Quantum-Enhanced Predictive & Self-Healing Urban Traffic
# Network
# ============================================================

import base64
from pathlib import Path

import pandas as pd
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random

from utils.environmental_metrics import calculate_environmental_metrics


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from prediction.traffic_prediction import (
    predict_traffic
)

from simulation.event_simulator import (
    apply_event,
    clear_event,
    get_event_description,
    get_event_impact
)

from simulation.emergency_corridor import (
    create_emergency_network,
    find_emergency_route,
    calculate_normal_travel_time,
    calculate_emergency_travel_time,
    calculate_time_saving,
    get_green_corridor
)

from optimization.traffic_optimizer import (
    calculate_optimal_green_times,
    apply_optimized_green_times,
    calculate_estimated_waiting_time,
    get_optimization_summary
)

from quantum.traffic_qubo import (
    create_qubo_model
)

from quantum.qaoa_solver import (
    run_simple_qaoa,
    decode_green_times
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Q-Flow Sentinel",
    page_icon="🚦",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "🚦 Q-Flow Sentinel"
)

st.subheader(
    "Quantum-Enhanced Predictive & Self-Healing "
    "Urban Traffic Network"
)

st.write(
    "A hybrid classical-quantum traffic optimization "
    "prototype for connected urban intersections."
)


# ============================================================
# CREATE INITIAL TRAFFIC NETWORK
# ============================================================

def create_intersections():

    return {

        "J1": {
            "traffic": 40,
            "queue": 10,
            "green_time": 30
        },

        "J2": {
            "traffic": 65,
            "queue": 18,
            "green_time": 30
        },

        "J3": {
            "traffic": 110,
            "queue": 35,
            "green_time": 30
        },

        "J4": {
            "traffic": 55,
            "queue": 15,
            "green_time": 30
        },

        "J5": {
            "traffic": 80,
            "queue": 25,
            "green_time": 30
        },

        "J6": {
            "traffic": 45,
            "queue": 12,
            "green_time": 30
        }

    }


# ============================================================
# UPDATE TRAFFIC
# ============================================================

def update_traffic(intersections):

    for junction, data in intersections.items():

        change = random.randint(
            -10,
            20
        )

        data["traffic"] += change

        data["traffic"] = max(
            0,
            data["traffic"]
        )

        data["queue"] = round(
            data["traffic"] * 0.30
        )

    return intersections


# ============================================================
# GET TRAFFIC STATUS
# ============================================================

def get_traffic_status(traffic):

    if traffic < 50:

        return "🟢 Low"

    elif traffic < 90:

        return "🟡 Medium"

    else:

        return "🔴 High"


# ============================================================
# MAP POSITIONS
# ============================================================

positions = {

    "J1": (0, 2),

    "J2": (-2, 0),

    "J3": (0, 0),

    "J4": (2, 0),

    "J5": (0, -2),

    "J6": (3, -2)

}


# ============================================================
# ROAD NETWORK
# ============================================================

roads = [

    ("J1", "J3"),

    ("J2", "J3"),

    ("J3", "J4"),

    ("J3", "J5"),

    ("J5", "J6")

]


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "intersections" not in st.session_state:

    st.session_state.intersections = (
        create_intersections()
    )


if "traffic_history" not in st.session_state:

    st.session_state.traffic_history = {

        junction: [
            data["traffic"]
        ]

        for junction, data
        in st.session_state.intersections.items()

    }


if "active_event" not in st.session_state:

    st.session_state.active_event = None


if "event_junction" not in st.session_state:

    st.session_state.event_junction = None


if "event_backup" not in st.session_state:

    st.session_state.event_backup = None


if "emergency_active" not in st.session_state:

    st.session_state.emergency_active = False


if "emergency_route" not in st.session_state:

    st.session_state.emergency_route = []


if "emergency_start" not in st.session_state:

    st.session_state.emergency_start = None


if "emergency_destination" not in st.session_state:

    st.session_state.emergency_destination = None


if "emergency_normal_time" not in st.session_state:

    st.session_state.emergency_normal_time = 0


if "emergency_time" not in st.session_state:

    st.session_state.emergency_time = 0


if "emergency_time_saving" not in st.session_state:

    st.session_state.emergency_time_saving = 0


if "quantum_results" not in st.session_state:

    st.session_state.quantum_results = None


# ============================================================
# AUTOMATIC EVENT CLEAR
# ============================================================

def automatically_clear_event():

    if (
        st.session_state.active_event is None
        or st.session_state.event_junction is None
        or st.session_state.event_backup is None
    ):

        return

    junction = (
        st.session_state.event_junction
    )

    original_traffic = (
        st.session_state.event_backup["traffic"]
    )

    current_traffic = (
        st.session_state.intersections[
            junction
        ]["traffic"]
    )

    if current_traffic <= original_traffic:

        st.session_state.intersections[
            junction
        ]["traffic"] = original_traffic

        st.session_state.intersections[
            junction
        ]["queue"] = (
            st.session_state.event_backup[
                "queue"
            ]
        )

        st.session_state.traffic_history[
            junction
        ].append(
            original_traffic
        )

        st.session_state.active_event = None

        st.session_state.event_junction = None

        st.session_state.event_backup = None


# ============================================================
# AUTOMATIC EVENT CHECK
# ============================================================

automatically_clear_event()


# ============================================================
# UPDATE TRAFFIC BUTTON
# ============================================================

st.header("📡 Live Traffic Monitoring")

if st.button(
    "🔄 Update Traffic"
):

    st.session_state.intersections = (
        update_traffic(
            st.session_state.intersections
        )
    )

    for junction, data in (
        st.session_state.intersections.items()
    ):

        st.session_state.traffic_history[
            junction
        ].append(
            data["traffic"]
        )

    automatically_clear_event()

    st.success(
        "✅ Traffic conditions updated."
    )


# ============================================================
# TRAFFIC TABLE
# ============================================================

traffic_table = []

for junction, data in (
    st.session_state.intersections.items()
):

    traffic_table.append({

        "Junction": junction,

        "Traffic Density": data[
            "traffic"
        ],

        "Queue Length": data[
            "queue"
        ],

        "Green Time": data[
            "green_time"
        ],

        "Status": get_traffic_status(
            data["traffic"]
        )

    })


traffic_df = pd.DataFrame(
    traffic_table
)

st.dataframe(
    traffic_df,
    use_container_width=True
)


# ============================================================
# TRAFFIC SUMMARY
# ============================================================

total_traffic = sum(

    data["traffic"]

    for data
    in st.session_state.intersections.values()

)

total_queue = sum(

    data["queue"]

    for data
    in st.session_state.intersections.values()

)

average_traffic = (

    total_traffic
    / len(
        st.session_state.intersections
    )

)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Traffic",
        total_traffic
    )


with col2:

    st.metric(
        "Total Queue",
        round(total_queue, 1)
    )


with col3:

    st.metric(
        "Average Traffic",
        round(average_traffic, 1)
    )


# ============================================================
# TRAFFIC NETWORK MAP
# ============================================================

st.header("🗺️ Traffic Network")


# ------------------------------------------------------------
# REALISTIC TRAFFIC MAP
# ------------------------------------------------------------

# Put the provided traffic map image in the same folder
# as this Streamlit app and name it:
#
# traffic_map.png
#
# Example:
# project_folder/
#     app.py
#     traffic_map.png
# ------------------------------------------------------------

MAP_FILE = Path(__file__).parent / "traffic_map.png"


if MAP_FILE.exists():

    # --------------------------------------------------------
    # CONVERT IMAGE TO BASE64
    # --------------------------------------------------------

    with open(MAP_FILE, "rb") as image_file:

        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()


    image_source = (
        "data:image/png;base64,"
        + encoded_image
    )


    # --------------------------------------------------------
    # IMAGE DIMENSIONS
    # --------------------------------------------------------

    map_width = 1343
    map_height = 1144


    # --------------------------------------------------------
    # CREATE MAP FIGURE
    # --------------------------------------------------------

    fig = go.Figure()


    # --------------------------------------------------------
    # ADD REALISTIC MAP AS BACKGROUND
    # --------------------------------------------------------

    fig.add_layout_image(

        dict(

            source=image_source,

            xref="x",

            yref="y",

            x=0,

            y=map_height,

            sizex=map_width,

            sizey=map_height,

            sizing="stretch",

            opacity=1,

            layer="below"

        )

    )


    # --------------------------------------------------------
    # JUNCTION POSITIONS
    #
    # Pixel positions are based on the uploaded map.
    # --------------------------------------------------------

    map_positions = {

        "J1": (641, 128),

        "J2": (175, 519),

        "J3": (641, 519),

        "J4": (1167, 519),

        "J5": (641, 959),

        "J6": (1170, 972)

    }


    # --------------------------------------------------------
    # INVISIBLE JUNCTION MARKERS
    #
    # These preserve hover information from your original map.
    # --------------------------------------------------------

    junction_x = []

    junction_y = []

    junction_hover = []


    for junction, data in (
        st.session_state.intersections.items()
    ):

        x, y = map_positions[junction]

        junction_x.append(x)

        # Plotly Y-axis starts from bottom
        junction_y.append(
            map_height - y
        )

        junction_hover.append(

            f"<b>{junction}</b><br>"
            f"Traffic: {data['traffic']}<br>"
            f"Queue: {data['queue']}<br>"
            f"Green Time: {data['green_time']}s<br>"
            f"Status: "
            f"{get_traffic_status(data['traffic'])}"

        )


    fig.add_trace(

        go.Scatter(

            x=junction_x,

            y=junction_y,

            mode="markers",

            marker=dict(

                size=45,

                color="rgba(0,0,0,0)",

                line=dict(
                    width=0
                )

            ),

            hovertext=junction_hover,

            hoverinfo="text",

            showlegend=False

        )

    )


    # --------------------------------------------------------
    # EMERGENCY GREEN CORRIDOR
    # --------------------------------------------------------

    if (
        st.session_state.emergency_active
        and st.session_state.emergency_route
    ):

        route = (
            st.session_state.emergency_route
        )


        route_x = []

        route_y = []


        for junction in route:

            x, y = map_positions[junction]

            route_x.append(x)

            route_y.append(
                map_height - y
            )


        # ----------------------------------------------------
        # DRAW EMERGENCY ROUTE
        # ----------------------------------------------------

        fig.add_trace(

            go.Scatter(

                x=route_x,

                y=route_y,

                mode="lines+markers",

                line=dict(

                    width=12,

                    color="limegreen"

                ),

                marker=dict(

                    size=14,

                    color="limegreen",

                    line=dict(

                        width=3,

                        color="white"

                    )

                ),

                name="Emergency Green Corridor",

                hoverinfo="name"

            )

        )


    # --------------------------------------------------------
    # MAP LAYOUT
    # --------------------------------------------------------

    fig.update_xaxes(

        range=[0, map_width],

        visible=False,

        fixedrange=True

    )


    fig.update_yaxes(

        range=[0, map_height],

        visible=False,

        fixedrange=True,

        scaleanchor="x",

        scaleratio=1

    )


    fig.update_layout(

        height=650,

        margin=dict(

            l=0,

            r=0,

            t=0,

            b=0

        ),

        showlegend=True,

        legend=dict(

            bgcolor="rgba(10,25,45,0.90)",

            font=dict(

                color="white",

                size=13

            ),

            bordercolor="rgba(255,255,255,0.25)",

            borderwidth=1

        ),

        plot_bgcolor="black",

        paper_bgcolor="black",

        hoverlabel=dict(

            bgcolor="#102A43",

            font_size=14,

            font_color="white"

        )

    )


    # --------------------------------------------------------
    # DISPLAY MAP
    # --------------------------------------------------------

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={

            "displayModeBar": False,

            "scrollZoom": False,

            "doubleClick": False,

            "displaylogo": False

        }

    )


else:

    # --------------------------------------------------------
    # IMAGE NOT FOUND
    # --------------------------------------------------------

    st.error(

        "⚠️ Traffic map image not found."

    )

    st.info(

        "Please place the provided map image in the "
        "same folder as app.py and rename it to "
        "'traffic_map.png'."

    )

# ============================================================
# TRAFFIC PREDICTION
# ============================================================

st.header("🔮 Traffic Prediction")

prediction_table = []


for junction in (
    st.session_state.intersections
):

    predicted = predict_traffic(

        st.session_state.traffic_history,

        junction

    )

    prediction_table.append({

        "Junction": junction,

        "Current Traffic":
            st.session_state.intersections[
                junction
            ]["traffic"],

        "Predicted Next Traffic":
            predicted

    })


prediction_df = pd.DataFrame(
    prediction_table
)

st.dataframe(
    prediction_df,
    use_container_width=True
)


# ============================================================
# DYNAMIC EVENT SIMULATION
# ============================================================

st.header("🚨 Dynamic Event Simulation")

event_options = [

    "None",

    "🚧 Accident",

    "🚫 Road Closure",

    "🚗 Traffic Surge"

]


selected_event = st.selectbox(

    "Select an event",

    event_options

)


event_junction = st.selectbox(

    "Select affected junction",

    list(
        st.session_state.intersections.keys()
    )

)


if st.button(
    "🚨 Trigger Event"
):

    if selected_event == "None":

        st.warning(
            "Please select an event."
        )

    else:

        # ----------------------------------------------------
        # SAVE ORIGINAL VALUES
        # ----------------------------------------------------

        original_data = (
            st.session_state.intersections[
                event_junction
            ]
        )

        st.session_state.event_backup = {

            "traffic":
                original_data["traffic"],

            "queue":
                original_data["queue"]

        }

        # ----------------------------------------------------
        # APPLY EVENT
        # ----------------------------------------------------

        event_name = selected_event

        apply_event(

            st.session_state.intersections,

            event_junction,

            event_name

        )

        st.session_state.active_event = (
            event_name
        )

        st.session_state.event_junction = (
            event_junction
        )

        st.session_state.traffic_history[
            event_junction
        ].append(

            st.session_state.intersections[
                event_junction
            ]["traffic"]

        )

        st.success(

            f"✅ {get_event_description(event_name)} "
            f"applied at {event_junction}."

        )

        st.info(

            f"Impact: "
            f"{get_event_impact(event_name)}"

        )


# ============================================================
# ACTIVE EVENT DISPLAY
# ============================================================

if st.session_state.active_event:

    st.warning(

        f"🚨 Active event: "
        f"{st.session_state.active_event} "
        f"at "
        f"{st.session_state.event_junction}"

    )

    st.info(

        "The event will automatically clear "
        "when traffic returns to the original level."

    )


# ============================================================
# EMERGENCY GREEN CORRIDOR
# ============================================================

st.header("🚑 Emergency Green Corridor")

st.write(

    "Select an emergency vehicle starting junction "
    "and destination. The system finds a safe route "
    "while avoiding closed junctions."

)


emergency_start = st.selectbox(

    "Emergency Vehicle Start",

    list(
        st.session_state.intersections.keys()
    ),

    key="emergency_start_select"

)


emergency_destination = st.selectbox(

    "Emergency Vehicle Destination",

    list(
        st.session_state.intersections.keys()
    ),

    key="emergency_destination_select"

)


if st.button(
    "🚑 Activate Emergency Corridor"
):

    # --------------------------------------------------------
    # FIND BLOCKED JUNCTIONS
    # --------------------------------------------------------

    blocked_junctions = []

    if (
        st.session_state.active_event
        == "🚫 Road Closure"
    ):

        blocked_junctions.append(
            st.session_state.event_junction
        )


    # --------------------------------------------------------
    # FIND SAFE ROUTE
    # --------------------------------------------------------

    route = find_emergency_route(

        emergency_start,

        emergency_destination,

        blocked_junctions

    )


    # --------------------------------------------------------
    # NO ROUTE
    # --------------------------------------------------------

    if not route:

        st.session_state.emergency_active = False

        st.session_state.emergency_route = []

        st.session_state.emergency_start = None

        st.session_state.emergency_destination = None

        st.session_state.emergency_normal_time = 0

        st.session_state.emergency_time = 0

        st.session_state.emergency_time_saving = 0


        if blocked_junctions:

            st.error(

                f"""❌ No safe emergency route is available.

🚧 The route is blocked by
{', '.join(blocked_junctions)}.

The system will NOT send the emergency vehicle
through the closed junction."""

            )

        else:

            st.error(

                """❌ No safe emergency route is available.

The selected junctions are not connected."""

            )


    # --------------------------------------------------------
    # ROUTE FOUND
    # --------------------------------------------------------

    else:

        st.session_state.emergency_active = True

        st.session_state.emergency_route = route

        st.session_state.emergency_start = (
            emergency_start
        )

        st.session_state.emergency_destination = (
            emergency_destination
        )


        # ----------------------------------------------------
        # CALCULATE TRAVEL TIMES
        # ----------------------------------------------------

        normal_time = (
            calculate_normal_travel_time(

                st.session_state.intersections,

                route

            )
        )


        emergency_time = (
            calculate_emergency_travel_time(

                st.session_state.intersections,

                route

            )
        )


        time_saving = (
            calculate_time_saving(

                normal_time,

                emergency_time

            )
        )


        st.session_state.emergency_normal_time = (
            normal_time
        )

        st.session_state.emergency_time = (
            emergency_time
        )

        st.session_state.emergency_time_saving = (
            time_saving
        )


        st.success(
            "🚑 Emergency green corridor activated."
        )


# ============================================================
# EMERGENCY ROUTE RESULTS
# ============================================================

if (
    st.session_state.emergency_active
    and st.session_state.emergency_route
):

    st.subheader(
        "🚑 Emergency Route"
    )

    st.write(

        " → ".join(
            st.session_state.emergency_route
        )

    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(

            "Normal Travel Time",

            f"{st.session_state.emergency_normal_time} units"

        )


    with col2:

        st.metric(

            "Emergency Travel Time",

            f"{st.session_state.emergency_time} units"

        )


    with col3:

        st.metric(

            "Time Saving",

            f"{st.session_state.emergency_time_saving} units"

        )


    st.info(

        "🚦 Selected junctions are operating as "
        "an emergency green corridor."

    )


# ============================================================
# TRAFFIC SIGNAL OPTIMIZATION
# ============================================================

st.header(
    "⚙️ Classical Traffic Signal Optimization"
)

st.write(

    "The classical optimization engine analyzes "
    "traffic pressure and calculates improved "
    "green-light timings for each junction."

)


optimized_times = (
    calculate_optimal_green_times(

        st.session_state.intersections

    )
)


optimization_summary = (
    get_optimization_summary(

        st.session_state.intersections,

        optimized_times

    )
)


optimization_df = pd.DataFrame(
    optimization_summary
)


st.dataframe(

    optimization_df,

    use_container_width=True

)


# ============================================================
# CLASSICAL WAITING TIME COMPARISON
# ============================================================

current_waiting_time = (
    calculate_estimated_waiting_time(

        st.session_state.intersections

    )
)


optimized_intersections = {

    junction: data.copy()

    for junction, data
    in st.session_state.intersections.items()

}


optimized_intersections = (
    apply_optimized_green_times(

        optimized_intersections,

        optimized_times

    )
)


optimized_waiting_time = (
    calculate_estimated_waiting_time(

        optimized_intersections

    )
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(

        "Current Estimated Waiting",

        f"{current_waiting_time} units"

    )


with col2:

    st.metric(

        "Optimized Estimated Waiting",

        f"{optimized_waiting_time} units"

    )


with col3:

    improvement = (

        current_waiting_time
        - optimized_waiting_time

    )

    st.metric(

        "Estimated Improvement",

        f"{round(improvement, 2)} units"

    )


# ============================================================
# APPLY CLASSICAL OPTIMIZATION
# ============================================================

if st.button(
    "⚙️ Apply Classical Optimized Signal Timings"
):

    st.session_state.intersections = (
        apply_optimized_green_times(

            st.session_state.intersections,

            optimized_times

        )
    )

    st.success(

        "✅ Classical optimized signal timings "
        "have been applied."

    )

    st.rerun()


# ============================================================
# QUANTUM TRAFFIC OPTIMIZATION
# ============================================================

st.header(
    "⚛️ Quantum Traffic Optimization"
)

st.write(

    "The quantum optimization module converts "
    "traffic conditions into a QUBO model and "
    "evaluates a quantum circuit to select "
    "signal timing choices."

)


# ============================================================
# RUN QUANTUM OPTIMIZATION
# ============================================================

if st.button(
    "⚛️ Run Quantum Optimization"
):

    with st.spinner(

        "Running quantum traffic optimization..."

    ):

        quantum_results = {}


        # ----------------------------------------------------
        # PROCESS EACH JUNCTION
        # ----------------------------------------------------

        for junction, data in (
            st.session_state.intersections.items()
        ):

            junction_data = {

                junction: {

                    "traffic":
                        data["traffic"],

                    "queue":
                        data["queue"]

                }

            }


            # ------------------------------------------------
            # CREATE QUBO
            # ------------------------------------------------

            model = create_qubo_model(

                junction_data

            )


            # ------------------------------------------------
            # RUN QUANTUM CIRCUIT
            # ------------------------------------------------

            result = run_simple_qaoa(

                model,

                shots=32

            )


            # ------------------------------------------------
            # DECODE RESULT
            # ------------------------------------------------

            timings = decode_green_times(

                result["bitstring"],

                model["variables"],

                model["green_time_options"]

            )


            selected_time = timings.get(

                junction

            )


            # ------------------------------------------------
            # STORE RESULT
            # ------------------------------------------------

            quantum_results[junction] = {

                "green_time":
                    selected_time,

                "cost":
                    result["cost"],

                "bitstring":
                    result["bitstring"],

                "gamma":
                    result["gamma"],

                "beta":
                    result["beta"]

            }


        st.session_state.quantum_results = (
            quantum_results
        )


        st.success(

            "✅ Quantum optimization completed successfully."

        )


# ============================================================
# DISPLAY QUANTUM RESULTS
# ============================================================

if st.session_state.quantum_results:

    st.subheader(

        "⚛️ Quantum Signal Timing Results"

    )


    quantum_table = []


    for junction, result in (
        st.session_state.quantum_results.items()
    ):

        quantum_table.append({

            "Junction":
                junction,

            "Quantum Green Time":
                result["green_time"],

            "QUBO Cost":
                result["cost"],

            "Quantum Bitstring":
                result["bitstring"],

            "Gamma":
                round(
                    result["gamma"],
                    3
                ),

            "Beta":
                round(
                    result["beta"],
                    3
                )

        })


    quantum_df = pd.DataFrame(

        quantum_table

    )


    st.dataframe(

        quantum_df,

        use_container_width=True

    )


# ============================================================
# CLASSICAL VS QUANTUM COMPARISON
# ============================================================

st.header(
    "📊 Classical vs Quantum Comparison"
)

st.write(
    "This section compares the signal timings and "
    "estimated waiting time produced by the classical "
    "and quantum optimization approaches."
)


# ============================================================
# CHECK WHETHER QUANTUM RESULTS EXIST
# ============================================================

if st.session_state.quantum_results:

    comparison_table = []

    for junction, data in (
        st.session_state.intersections.items()
    ):

        # ----------------------------------------------------
        # CLASSICAL TIMING
        # ----------------------------------------------------

        classical_time = optimized_times.get(
            junction,
            data["green_time"]
        )

        # ----------------------------------------------------
        # QUANTUM TIMING
        # ----------------------------------------------------

        quantum_data = (
            st.session_state.quantum_results.get(
                junction
            )
        )

        if quantum_data:

            quantum_time = (
                quantum_data["green_time"]
            )

        else:

            quantum_time = None


        # ----------------------------------------------------
        # ADD TO COMPARISON TABLE
        # ----------------------------------------------------

        comparison_table.append({

            "Junction":
                junction,

            "Current Green Time":
                data["green_time"],

            "Classical Green Time":
                classical_time,

            "Quantum Green Time":
                quantum_time

        })


    comparison_df = pd.DataFrame(
        comparison_table
    )


    st.dataframe(
        comparison_df,
        use_container_width=True
    )


    # ========================================================
    # WAITING TIME COMPARISON
    # ========================================================

    classical_intersections = {

        junction: data.copy()

        for junction, data
        in st.session_state.intersections.items()

    }


    classical_intersections = (
        apply_optimized_green_times(
            classical_intersections,
            optimized_times
        )
    )


    classical_waiting = (
        calculate_estimated_waiting_time(
            classical_intersections
        )
    )


    # --------------------------------------------------------
    # CREATE QUANTUM INTERSECTION COPY
    # --------------------------------------------------------

    quantum_intersections = {

        junction: data.copy()

        for junction, data
        in st.session_state.intersections.items()

    }


    for junction, result in (
        st.session_state.quantum_results.items()
    ):

        quantum_time = result[
            "green_time"
        ]

        if quantum_time is not None:

            quantum_intersections[
                junction
            ]["green_time"] = quantum_time


    quantum_waiting = (
        calculate_estimated_waiting_time(
            quantum_intersections
        )
    )


    # ========================================================
    # DISPLAY METRICS
    # ========================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Classical Estimated Waiting",
            f"{classical_waiting} units"
        )


    with col2:

        st.metric(
            "Quantum Estimated Waiting",
            f"{quantum_waiting} units"
        )


    with col3:

        difference = (
            classical_waiting
            - quantum_waiting
        )

        st.metric(
            "Difference",
            f"{round(difference, 2)} units"
        )


    # ========================================================
    # BAR CHART
    # ========================================================

    comparison_chart = go.Figure()


    comparison_chart.add_trace(

        go.Bar(

            name="Classical",

            x=[
                "Estimated Waiting Time"
            ],

            y=[
                classical_waiting
            ]

        )

    )


    comparison_chart.add_trace(

        go.Bar(

            name="Quantum",

            x=[
                "Estimated Waiting Time"
            ],

            y=[
                quantum_waiting
            ]

        )

    )


    comparison_chart.update_layout(

        title="Classical vs Quantum Estimated Waiting",

        barmode="group",

        yaxis_title="Waiting Time"

    )


    st.plotly_chart(

        comparison_chart,

        use_container_width=True

    )


else:

    st.info(

        "ℹ️ Run Quantum Optimization first "
        "to generate the comparison."

    )


# ============================================================
# END
# ============================================================

# ============================================================
# ENVIRONMENTAL ANALYSIS
# ============================================================

st.header("Environmental Analysis")

# ------------------------------------------------------------
# Get current traffic network
# ------------------------------------------------------------

current_intersections = st.session_state.intersections

# ------------------------------------------------------------
# Current traffic environmental metrics
# ------------------------------------------------------------

current_environment = calculate_environmental_metrics(
    current_intersections
)

# ------------------------------------------------------------
# Use classical results if they exist
# Otherwise use current traffic data
# ------------------------------------------------------------

if "classical_intersections" in locals():

    classical_environment = calculate_environmental_metrics(
        classical_intersections
    )

else:

    classical_environment = calculate_environmental_metrics(
        current_intersections
    )


# ------------------------------------------------------------
# Use quantum results if they exist
# Otherwise use current traffic data
# ------------------------------------------------------------

if "quantum_intersections" in locals():

    quantum_environment = calculate_environmental_metrics(
        quantum_intersections
    )

else:

    quantum_environment = calculate_environmental_metrics(
        current_intersections
    )


# ============================================================
# DISPLAY ENVIRONMENTAL METRICS
# ============================================================

st.subheader("Environmental Metrics")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Throughput",
        f"{quantum_environment['Throughput']} vehicles"
    )

with col2:

    st.metric(
        "Estimated Fuel",
        f"{quantum_environment['Fuel Consumption']} L"
    )

with col3:

    st.metric(
        "Estimated CO₂",
        f"{quantum_environment['CO2 Emissions']} kg"
    )


# ============================================================
# ENVIRONMENTAL COMPARISON
# ============================================================

environment_comparison = pd.DataFrame({

    "Metric": [
        "Throughput",
        "Fuel Consumption",
        "CO2 Emissions"
    ],

    "Current": [
        current_environment["Throughput"],
        current_environment["Fuel Consumption"],
        current_environment["CO2 Emissions"]
    ],

    "Classical": [
        classical_environment["Throughput"],
        classical_environment["Fuel Consumption"],
        classical_environment["CO2 Emissions"]
    ],

    "Quantum": [
        quantum_environment["Throughput"],
        quantum_environment["Fuel Consumption"],
        quantum_environment["CO2 Emissions"]
    ]
})


st.dataframe(
    environment_comparison,
    use_container_width=True
)

# ============================================================
# SYSTEM SUMMARY
# ============================================================

st.header("Q-Flow Sentinel System Summary")

st.write(
    "Q-Flow Sentinel combines traffic monitoring, traffic prediction, "
    "dynamic event handling, emergency routing, classical optimization, "
    "quantum optimization, and environmental analysis."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Intersections",
        len(current_intersections)
    )

with col2:
    active_event = st.session_state.get("active_event")
    if active_event:
        st.metric("Active Event", active_event)
    else:
        st.metric("Active Event", "None")

with col3:
    if "quantum_results" in st.session_state:
        st.metric("Quantum Optimization", "Completed")
    else:
        st.metric("Quantum Optimization", "Not Run")

st.success(
    "Hybrid quantum-classical traffic optimization system is ready."
)


# ============================================================
# END
# ============================================================