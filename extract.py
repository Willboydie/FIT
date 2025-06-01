from fitparse import FitFile
import json
import os


# utils
def to_seconds(timestamp):
    """Convert FIT timestamp to seconds since epoch."""
    return int(timestamp.timestamp())

def to_readable(timestamp):
    """Convert FIT timestamp to a human-readable format."""
    return timestamp.strftime("%Y-%m-%d_%H-%M-%S")

def extract_fitfile_data(fitfile):
    """Extract heart rates with respect to elapsed time from FIT file."""
    heart_rate = []
    enhanced_speed = []
    lat = []
    long = []
    distance = []
    elapsed = []
    timestamp = []

    available_metrics = set()

    # Iterate through all messages
    for idx, record in enumerate(fitfile.get_messages("record")):
        # Each record is a timestamped datapoint
        datapoint = {}
        for field in record:
            datapoint[field.name] = field.value

            if field.name == "heart_rate":
                heart_rate.append(field.value)

                available_metrics.add("heart_rate")  

            if field.name == "timestamp":
                timestamp.append(to_readable(field.value))

                # get start time elapsed time
                if idx == 0:
                    start_ = to_seconds(field.value)

                seconds = to_seconds(field.value)
                elapsed.append(seconds - start_)

            if field.name == "enhanced_speed":
                enhanced_speed.append(field.value)

            if field.name == "position_lat":
                lat.append(field.value)

            if field.name == "position_long":
                long.append(field.value)

            if field.name == "distance":
                distance.append(field.value)
    
    if heart_rate:
        available_metrics.add("heart_rate")
    if enhanced_speed:
        available_metrics.add("enhanced_speed")
    if lat and long:
        available_metrics.add("map")
    if distance:
        available_metrics.add("distance")

    data = {
        "name": f"session_{timestamp[0]}",
        "heart_rate": heart_rate,
        "enhanced_speed": enhanced_speed,
        "lat": lat,
        "long": long,
        "distance": distance,
        "elapsed": elapsed,
        "timestamp": timestamp
    }

    return data, list(available_metrics)


raw_dir = "data/FIT/raw"
for i, filename in enumerate(os.listdir(raw_dir)):
    if filename.lower().endswith(".fit"):
        fitfile = FitFile(os.path.join(raw_dir, filename))
        data, available_metrics = extract_fitfile_data(fitfile)
        with open(f"data/FIT/processed/{data['name'][:-3]}.json", "w") as f:
            json.dump(data, f, indent=4)