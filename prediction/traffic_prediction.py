# ============================================================
# FUTURE TRAFFIC PREDICTION
# ============================================================

def predict_traffic(history, junction):

    # If there is no history for this junction
    if junction not in history:
        return 0

    values = history[junction]

    # If there are no traffic values
    if len(values) == 0:
        return 0

    # Current traffic
    current = values[-1]

    # If there is only one reading,
    # we cannot calculate a trend yet.
    if len(values) == 1:
        return current

    # Calculate recent traffic changes
    changes = []

    for i in range(1, len(values)):

        change = values[i] - values[i - 1]

        changes.append(change)

    # Average traffic change
    average_change = sum(changes) / len(changes)

    # Predict next traffic
    prediction = current + average_change

    # Traffic cannot be negative
    prediction = max(0, prediction)

    return round(prediction)