from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def plot_heart_rate(root, data, x_unit, y_unit):
    """Plot heart rate data over elapsed time."""
    fig = Figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(data["elapsed"], data["heart_rate"], color="crimson", label="Heart Rate")
    ax.set_title("Heart Rate Over Time")
    ax.set_xlabel(f"Elapsed Time ({x_unit})")
    ax.set_ylabel(f"Heart Rate ({y_unit})")
    ax.legend()
    return fig

def plot_speed(root, data, x_unit, y_unit):
    fig = Figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(data["elapsed"], data["enhanced_speed"], color="royalblue", label="Enhanced Speed")
    ax.set_title("Enhanced Speed Over Time")
    ax.set_xlabel(f"Elapsed Time ({x_unit})")
    ax.set_ylabel(f"Speed ({y_unit})")
    ax.legend()
    if y_unit == "500 split pace (s)":
        ax.set_ylim(bottom=0, top=500)  # Adjust y-axis for pace
        ax.invert_yaxis()
    return fig

def plot_distance(root, data, x_unit, y_unit):
    fig = Figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(data["elapsed"], data["distance"], color="green", label="Distance")
    ax.set_title("Distance Over Time")
    ax.set_xlabel(f"Elapsed Time ({x_unit})")
    ax.set_ylabel(f"Distance ({y_unit})")
    ax.legend()
    return fig

def plot_route(root, data, x_unit, y_unit):
    fig = Figure(figsize=(12, 12), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(data["long"], data["lat"], color="purple", label="Route")
    ax.set_title("Route Map")
    ax.set_xlabel(f"Longitude ({x_unit})")
    ax.set_ylabel(f"Latitude ({y_unit})")
    ax.legend()
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')
    return fig
