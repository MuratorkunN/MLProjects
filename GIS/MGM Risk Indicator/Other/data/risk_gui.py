import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import glob
from datetime import datetime

"""
NOTE: AI GENERATED GUI
"""

class FrostRiskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Frost Risk Monitor - Bursa")
        self.root.geometry("950x700")
        self.root.configure(bg="#1a1a2e")
        
        # Data storage: {district_name: [{'date':..., 'min':..., 'max':...}, ...]}
        self.district_data = {}
        self.districts = []
        
        self.fruits = ["peach", "plum"]
        
        self.setup_styles()
        self.create_widgets()
        self.load_data()
        
        # Initial calculation
        self.update_risk_regions_list()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure("Main.TFrame", background="#1a1a2e")
        style.configure("Card.TFrame", background="#16213e", borderwidth=1, relief="flat")
        style.configure("Sidebar.TFrame", background="#12122b")
        
        style.configure("Header.TLabel", 
                        background="#1a1a2e", 
                        foreground="#ffffff", 
                        font=("Outfit", 20, "bold"))
        
        style.configure("Sub.TLabel", 
                        background="#1a1a2e", 
                        foreground="#a0a0a0", 
                        font=("Outfit", 10))

        style.configure("TLabel", 
                        background="#16213e", 
                        foreground="#e0e0e0", 
                        font=("Outfit", 11))
        
        style.configure("Risk.TLabel", 
                        background="#16213e", 
                        font=("Outfit", 18, "bold"))
        
        style.configure("Treeview", 
                        background="#16213e", 
                        foreground="white", 
                        fieldbackground="#16213e",
                        font=("Outfit", 10))
        
        style.map("Treeview", background=[('selected', '#4ecca3')])

    def create_widgets(self):
        # Layout: Sidebar (Left) and Content (Right)
        self.paned = tk.PanedWindow(self.root, orient="horizontal", bg="#1a1a2e", sashwidth=4, bd=0)
        self.paned.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ttk.Frame(self.paned, style="Sidebar.TFrame", padding="20")
        self.paned.add(sidebar, width=280)
        
        ttk.Label(sidebar, text="AT RISK REGIONS", style="Sub.TLabel", background="#12122b", foreground="#ff4757", font=("Outfit", 11, "bold")).pack(pady=(0, 10))
        
        self.risk_listbox = tk.Listbox(sidebar, bg="#16213e", fg="white", borderwidth=0, highlightthickness=0, font=("Outfit", 10), selectbackground="#ff4757")
        self.risk_listbox.pack(fill="both", expand=True)
        self.risk_listbox.bind("<<ListboxSelect>>", self.on_risk_list_select)

        # Content Area
        content = ttk.Frame(self.paned, style="Main.TFrame", padding="30")
        self.paned.add(content)
        
        # Header
        ttk.Label(content, text="Frost Risk Monitor", style="Header.TLabel").pack(pady=(0, 5))
        ttk.Label(content, text="BURSA REGION FORECAST ANALYSIS", style="Sub.TLabel").pack(pady=(0, 20))
        
        # Controls Frame
        ctrl_frame = ttk.Frame(content, style="Main.TFrame")
        ctrl_frame.pack(fill="x", pady=(0, 20))
        
        # Fruit Selection
        ttk.Label(ctrl_frame, text="Select Fruit:", style="Sub.TLabel", background="#1a1a2e").pack(side="left", padx=(0, 5))
        self.fruit_var = tk.StringVar(value=self.fruits[0])
        self.fruit_combo = ttk.Combobox(ctrl_frame, textvariable=self.fruit_var, values=self.fruits, state="readonly", width=10)
        self.fruit_combo.pack(side="left", padx=(0, 20))
        self.fruit_combo.bind("<<ComboboxSelected>>", self.on_parameters_changed)

        # Region Selection
        ttk.Label(ctrl_frame, text="Select Region:", style="Sub.TLabel", background="#1a1a2e").pack(side="left", padx=(0, 5))
        self.region_var = tk.StringVar()
        self.region_combo = ttk.Combobox(ctrl_frame, textvariable=self.region_var, state="readonly", width=20)
        self.region_combo.pack(side="left")
        self.region_combo.bind("<<ComboboxSelected>>", self.on_region_selected)
        
        # Legend (Visual Indicator)
        legend_frame = ttk.Frame(ctrl_frame, style="Main.TFrame")
        legend_frame.pack(side="right")
        ttk.Label(legend_frame, text="■ Critical", foreground="#ff6b6b", background="#1a1a2e", font=("Outfit", 9)).pack(side="left", padx=5)
        ttk.Label(legend_frame, text="■ Warning", foreground="#ffca2c", background="#1a1a2e", font=("Outfit", 9)).pack(side="left", padx=5)

        # Risk Card
        self.risk_card = ttk.Frame(content, style="Card.TFrame", padding="20")
        self.risk_card.pack(fill="x", pady=10)
        
        self.status_label = ttk.Label(self.risk_card, text="Select a region to analyze", style="Risk.TLabel")
        self.status_label.pack()
        
        self.analysis_label = ttk.Label(self.risk_card, text="", font=("Outfit", 12))
        self.analysis_label.pack(pady=5)

        # Forecast Table
        table_frame = ttk.Frame(content, style="Main.TFrame")
        table_frame.pack(fill="both", expand=True)
        
        columns = ("date", "low", "high", "risk")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        
        self.tree.heading("date", text="Date")
        self.tree.heading("low", text="Min Temp (°C)")
        self.tree.heading("high", text="Max Temp (°C)")
        self.tree.heading("risk", text="Thresholds (10% / 90%)")
        
        self.tree.column("date", anchor="center", width=120)
        self.tree.column("low", anchor="center", width=100)
        self.tree.column("high", anchor="center", width=100)
        self.tree.column("risk", anchor="center", width=200)
        
        # Define Tags for Coloring
        # Critical: Below 90% kill temp (Severe) - Red
        self.tree.tag_configure('critical', background='#4a1c1c', foreground='#ff6b6b')
        # Warning: Below 10% kill temp (Medium) - Orange/Yellow-Red
        self.tree.tag_configure('warning', background='#5c4b1e', foreground='#ffca2c')
        
        self.tree.pack(fill="both", expand=True)

    def get_limit_temperature(self, fruit, date, severity):
        md = (date.month, date.day)

        if severity == "10percent":
            if fruit == "peach":
                if (2, 20) <= md <= (3, 5): return -7.7
                if (3, 6) <= md <= (3, 15): return -6.1
                if (3, 16) <= md <= (3, 22): return -5.0
                if (3, 23) <= md <= (3, 30): return -3.8
                if (3, 31) <= md <= (4, 4): return -3.3
                if (4, 5) <= md <= (4, 12): return -2.7
                if (4, 13) <= md <= (4, 25): return -2.2
                return 15 #-15.0

            if fruit == "plum":
                if (3, 1) <= md <= (3, 10): return -2.8
                if (3, 11) <= md <= (3, 20): return -2.8
                if (3, 21) <= md <= (4, 15): return -1.1
                return 12# -18.0
            return -2

        if severity == "90percent":
            if fruit == "peach":
                if (2, 20) <= md <= (3, 5): return -17.2
                if (3, 6) <= md <= (3, 15): return -15.0
                if (3, 16) <= md <= (3, 22): return -12.7
                if (3, 23) <= md <= (3, 30): return -9.4
                if (3, 31) <= md <= (4, 4): return -6.1
                if (4, 5) <= md <= (4, 12): return -4.4
                if (4, 13) <= md <= (4, 25): return -3.8
                return 8 #-20.0

            if fruit == "plum":
                if (3, 1) <= md <= (3, 10): return -5.0
                if (3, 11) <= md <= (3, 20): return -5.0
                if (3, 21) <= md <= (4, 15): return -4.5
                return 7 #-25.0

            return -4

        return 0

    def load_data(self):
        # Look for files matching prediction-*.csv
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_pattern = os.path.join(script_dir, "prediction-*.csv")
        files = glob.glob(file_pattern)

        if not files:
            messagebox.showerror("Error", f"No prediction files found in:\n{script_dir}")
            return

        for filepath in files:
            filename = os.path.basename(filepath)
            # prediction-buyukorhan.csv -> buyukorhan
            district_key = filename.replace("prediction-", "").replace(".csv", "").title()
            
            try:
                forecasts = []
                with open(filepath, mode='r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    all_rows = list(reader) # Load all into memory to traverse backwards
                    
                    # Logic: 
                    # We want exactly 5 days: Day 0 (min0), Day 1 (min1), ... Day 4 (min4)
                    # For each 'i', find the LAST row where 'mini' is not null.
                    
                    for i in range(5):
                        key_min = f"min{i}"
                        key_max = f"max{i}"
                        found = False
                        
                        # Traverse backwards to find the last occurrence
                        for row in reversed(all_rows):
                            val_min = row.get(key_min)
                            if val_min and val_min.strip():
                                try:
                                    min_temp = float(val_min)
                                    # Get max temp if available, otherwise "-"
                                    val_max = row.get(key_max)
                                    max_temp = float(val_max) if (val_max and val_max.strip()) else "-"
                                    
                                    date_obj = datetime.strptime(row['date'], "%d.%m.%Y")
                                    
                                    forecasts.append({
                                        'date_obj': date_obj,
                                        'date_str': row['date'],
                                        'min': min_temp,
                                        'max': max_temp
                                    })
                                    found = True
                                    break # Found the last entry for this day index, stop searching
                                except ValueError:
                                    continue
                        
                        # If not found for a specific day index, we just skip it 
                        # (or you could append a placeholder if strict 5-day view is needed)

                # Sort by date because min0, min1... might result in dates out of order if there are gaps (though unlikely)
                forecasts.sort(key=lambda x: x['date_obj'])
                
                if forecasts:
                    self.district_data[district_key] = forecasts
            
            except Exception as e:
                print(f"Error loading {filename}: {e}")

        self.districts = sorted(list(self.district_data.keys()))
        self.region_combo['values'] = self.districts

    def update_risk_regions_list(self):
        """Updates the sidebar list based on selected fruit and loaded data"""
        self.risk_listbox.delete(0, tk.END)
        fruit = self.fruit_var.get()
        
        at_risk_map = [] # Tuple (district, risk_level) 0=Safe, 1=Warning, 2=Critical

        for district, forecasts in self.district_data.items():
            max_risk = 0 # 0: Safe, 1: Warning, 2: Critical
            
            for day in forecasts:
                temp = day['min']
                d_obj = day['date_obj']
                
                limit_10 = self.get_limit_temperature(fruit, d_obj, "10percent")
                limit_90 = self.get_limit_temperature(fruit, d_obj, "90percent")
                
                if temp <= limit_90:
                    max_risk = 2
                    break # Critical found, highest priority
                elif temp <= limit_10:
                    max_risk = max(max_risk, 1)
            
            if max_risk > 0:
                at_risk_map.append((district, max_risk))
        
        if not at_risk_map:
            self.risk_listbox.insert(tk.END, "No regions at risk")
            self.risk_listbox.config(state="disabled")
        else:
            self.risk_listbox.config(state="normal")
            # Sort by risk level (Critical first) then name
            at_risk_map.sort(key=lambda x: (-x[1], x[0]))
            
            for dist, risk in at_risk_map:
                icon = "🛑" if risk == 2 else "⚠️"
                self.risk_listbox.insert(tk.END, f"{icon} {dist}")

    def on_parameters_changed(self, event):
        """Called when Fruit is changed"""
        self.update_risk_regions_list()
        if self.region_var.get():
            self.update_dashboard(self.region_var.get())

    def on_risk_list_select(self, event):
        selection = self.risk_listbox.curselection()
        if selection:
            text = self.risk_listbox.get(selection[0])
            # Strip icons 🛑 or ⚠️
            if " " in text:
                region = text.split(" ", 1)[1]
                self.region_var.set(region)
                self.update_dashboard(region)

    def on_region_selected(self, event):
        self.update_dashboard(self.region_var.get())

    def update_dashboard(self, region):
        forecasts = self.district_data.get(region, [])
        fruit = self.fruit_var.get()
        
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        lowest_temp = 100
        worst_risk_level = 0 # 0 safe, 1 warning, 2 critical
        
        if not forecasts:
            self.status_label.config(text="No data available", foreground="#a0a0a0")
            self.analysis_label.config(text="")
            return

        for row in forecasts:
            temp = row['min']
            d_obj = row['date_obj']
            
            limit_10 = self.get_limit_temperature(fruit, d_obj, "10percent")
            limit_90 = self.get_limit_temperature(fruit, d_obj, "90percent")
            
            # Determine Row Status
            tag = ''
            risk_level = 0
            
            if temp <= limit_90:
                tag = 'critical'
                risk_level = 2
            elif temp <= limit_10:
                tag = 'warning'
                risk_level = 1
            
            worst_risk_level = max(worst_risk_level, risk_level)
            if temp < lowest_temp:
                lowest_temp = temp
            
            self.tree.insert("", "end", 
                             values=(row['date_str'], f"{temp}°C", f"{row['max']}°C", f"{limit_10}°C / {limit_90}°C"), 
                             tags=(tag,))

        # Update Status Card
        self.analysis_label.config(text=f"Lowest Forecast: {lowest_temp}°C")
        
        if worst_risk_level == 2:
            self.status_label.config(text="🛑 CRITICAL FROST RISK", foreground="#ff4757")
        elif worst_risk_level == 1:
            self.status_label.config(text="⚠️ MEDIUM FROST RISK", foreground="#ffca2c")
        else:
            self.status_label.config(text="✅ SAFE CONDITIONS", foreground="#2ed573")

if __name__ == "__main__":
    root = tk.Tk()
    app = FrostRiskApp(root)
    root.mainloop()