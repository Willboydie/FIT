import tkinter as tk
from tkinter import filedialog, messagebox
from fitparse import FitFile
import extract
import visualise
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FitViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FIT File Viewer")

        self.selected_file = None
        self.data = None
        self.canvas = None

        # UI Elements
        self.file_label = tk.Label(root, text="No file selected.")
        self.file_label.pack(pady=5)

        # Processing status label
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)
        self.file_available_metrics = []

        tk.Button(root, text="Select FIT File", command=self.select_file).pack(pady=5)

        # Unit options per graph type
        self.x_unit_options = {
            "heart_rate": ["seconds", "minutes", "hours"],
            "enhanced_speed": ["seconds", "minutes", "hours"],
            "distance": ["seconds", "minutes", "hours"],
            "map": ["default"]
        }

        self.y_unit_options = {
            "heart_rate": ["bpm (default)"],
            "enhanced_speed": ["m/s", "km/h", "500 split pace (s)"],
            "distance": ["meters", "kilometers"],
            "map": ["default"]
        }

        # Graph type dropdown label
        tk.Label(root, text="Select Graph Type:").pack(pady=(10, 0))
        self.option_var = tk.StringVar(value="select")
        self.dropdown = tk.OptionMenu(root, self.option_var, "select")  # default value
        self.dropdown.pack(pady=5)

        # X-axis units label
        tk.Label(root, text="X-axis Units:").pack(pady=(10, 0))
        self.x_unit_var = tk.StringVar(value="select")
        self.x_unit_dropdown = tk.OptionMenu(root, self.x_unit_var, "select")
        self.x_unit_dropdown.pack(pady=5)

        # Y-axis units label
        tk.Label(root, text="Y-axis Units:").pack(pady=(10, 0))
        self.y_unit_var = tk.StringVar(value="select")
        self.y_unit_dropdown = tk.OptionMenu(root, self.y_unit_var, "select")
        self.y_unit_dropdown.pack(pady=5)

        tk.Button(root, text="Show Graph", command=self.show_graph).pack(pady=5)


    def on_graph_type_change(self, selected_graph):
        self.update_units_dropdown(selected_graph)
        self.option_var.set(selected_graph)


    def update_graph_dropdown(self):
        menu = self.dropdown["menu"]
        menu.delete(0, "end")

        if not self.file_available_metrics:
            self.file_available_metrics = [] 

        for metric in self.file_available_metrics:
            menu.add_command(label=metric, command=lambda value=metric: self.on_graph_type_change(value))

        if self.file_available_metrics:
            self.option_var.set(self.file_available_metrics[0])
            self.update_units_dropdown(self.file_available_metrics[0])


    def update_units_dropdown(self, graph_type):
        # Update x-axis units
        x_menu = self.x_unit_dropdown["menu"]
        x_menu.delete(0, "end")
        for option in self.x_unit_options[graph_type]:
            x_menu.add_command(label=option, command=lambda value=option: self.x_unit_var.set(value))
        self.x_unit_var.set(self.x_unit_options[graph_type][0])

        # Update y-axis units
        y_menu = self.y_unit_dropdown["menu"]
        y_menu.delete(0, "end")
        for option in self.y_unit_options[graph_type]:
            y_menu.add_command(label=option, command=lambda value=option: self.y_unit_var.set(value))
        self.y_unit_var.set(self.y_unit_options[graph_type][0])



    def convert_units(self, data, x_unit, y_unit):
        converted = {k: v[:] if isinstance(v, list) else v for k, v in data.items()}

        if x_unit == "minutes":
            converted["elapsed"] = [t / 60 for t in converted["elapsed"]]
        elif x_unit == "hours":
            converted["elapsed"] = [t / 3600 for t in converted["elapsed"]]

        if y_unit == "km/h":
            converted["speed"] = [v * 3.6 for v in converted["speed"]]
        elif y_unit == "kilometers":
            converted["distance"] = [v / 1000 for v in converted["distance"]]
        elif y_unit == "500 split pace (s)":
            converted["speed"] = [500 / v if v > 0 else 1000 for v in converted["speed"]]
        return converted


    def select_file(self):

        file_path = filedialog.askopenfilename(
            initialdir="data/FIT/raw",
            filetypes=[("FIT files", "*.fit")]
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"Selected: {file_path.split('/')[-1]}")
            try:
                self.status_label.config(text="Extracting data...")
                self.status_label.update()
                fitfile = FitFile(self.selected_file)
                self.data, self.file_available_metrics = extract.extract_fitfile_data(fitfile)
                self.status_label.config(text="")
                self.status_label.update()
                self.update_graph_dropdown()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to extract data:\n{e}")


    def show_graph(self):
        if not self.data:
            messagebox.showwarning("No Data", "Please select a FIT file first.")
            return

        graph_type = self.option_var.get()
        x_unit = self.x_unit_var.get()
        y_unit = self.y_unit_var.get()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        try:
            data_for_plot = self.convert_units(self.data, x_unit, y_unit)

            if graph_type == "heart_rate":
                fig = visualise.plot_heart_rate(self.root, data_for_plot, x_unit, y_unit)
            elif graph_type == "enhanced_speed":
                fig = visualise.plot_speed(self.root, data_for_plot, x_unit, y_unit)
            elif graph_type == "distance":
                fig = visualise.plot_distance(self.root, data_for_plot, x_unit, y_unit)
            elif graph_type == "map":
                fig = visualise.plot_route(self.root, data_for_plot, x_unit, y_unit)
            else:
                messagebox.showerror("Invalid Option", "Unknown graph type selected.")
                return

            self.canvas = FigureCanvasTkAgg(fig, master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to plot graph:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FitViewerApp(root)
    root.mainloop()
