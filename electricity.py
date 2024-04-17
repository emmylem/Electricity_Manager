#!/usr/bin/env python3


import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import random

class ElectricityManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Electricity Usage Tracker")

        # Default values for total units and total days
        self.total_units = random.randint(10, 30)  # Random total units between 10 and 30
        self.total_days = random.randint(15, 30)   # Random total days between 15 and 30

        # Remaining units, remaining days, and usage history
        self.remaining_units = self.total_units
        self.remaining_days = self.total_days
        self.usage_history = []

        # Load saved data
        self.load_data()

        # Labels and entry for customization options
        self.label_total_units = tk.Label(master, text="Total Units:")
        self.label_total_units.grid(row=0, column=0, padx=10, pady=5)
        self.entry_total_units = tk.Entry(master)
        self.entry_total_units.insert(0, str(self.total_units))
        self.entry_total_units.grid(row=0, column=1, padx=10, pady=5)

        self.label_total_days = tk.Label(master, text="Total Days:")
        self.label_total_days.grid(row=1, column=0, padx=10, pady=5)
        self.entry_total_days = tk.Entry(master)
        self.entry_total_days.insert(0, str(self.total_days))
        self.entry_total_days.grid(row=1, column=1, padx=10, pady=5)

        self.label_units_used = tk.Label(master, text="Units Used:")
        self.label_units_used.grid(row=2, column=0, padx=10, pady=5)
        self.entry_units_used = tk.Entry(master)
        self.entry_units_used.grid(row=2, column=1, padx=10, pady=5)

        # Buttons for actions
        self.button_submit = tk.Button(master, text="Submit", command=self.submit)
        self.button_submit.grid(row=0, column=2, padx=10, pady=5)

        self.button_visualize = tk.Button(master, text="Visualize Usage", command=self.visualize)
        self.button_visualize.grid(row=0, column=3, padx=10, pady=5)

        self.button_reset = tk.Button(master, text="Reset", command=self.confirm_reset)
        self.button_reset.grid(row=0, column=4, padx=10, pady=5)

        # Smart meter button
        self.button_smart_meter = tk.Button(master, text="Smart Meter", command=self.smart_meter)
        self.button_smart_meter.grid(row=1, column=2, columnspan=3, padx=10, pady=5)

        # Energy-saving tips button
        self.button_energy_saving_tips = tk.Button(master, text="Energy Saving Tips", command=self.energy_saving_tips)
        self.button_energy_saving_tips.grid(row=2, column=2, columnspan=3, padx=10, pady=5)

        # Message label
        self.label_message = tk.Label(master, text="")
        self.label_message.grid(row=3, column=0, columnspan=5, padx=10, pady=5)

        # Protocol for saving data on window close
        master.protocol("WM_DELETE_WINDOW", self.save_data)

        # Check remaining units on startup
        self.check_remaining_units()

    def submit(self):
        try:
            self.total_units = int(self.entry_total_units.get())
            self.total_days = int(self.entry_total_days.get())
            units_used = float(self.entry_units_used.get())

            if units_used < 0:
                messagebox.showerror("Error", "Please enter a valid number of units.")
            elif units_used > self.remaining_units:
                messagebox.showerror("Error", "Not enough units remaining.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.remaining_units -= units_used
                self.remaining_days -= 1
                self.usage_history.append((timestamp, units_used))
                self.label_message.config(text=f"{units_used} units used. Remaining units: {self.remaining_units}, Remaining days: {self.remaining_days}")
                self.check_remaining_units()  # Check remaining units after usage
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for total units, total days, and units used.")

    def visualize(self):
        if not self.usage_history:
            messagebox.showinfo("No Data", "No usage data available.")
            return

        timestamps, usage = zip(*self.usage_history)
        plt.figure(figsize=(8, 6))
        plt.plot(timestamps, usage, marker='o', linestyle='-')
        plt.title("Electricity Usage Over Time")
        plt.xlabel("Timestamp")
        plt.ylabel("Units Used")
        plt.xticks(rotation=45)
        plt.grid(True)

        # Displaying the plot in a Tkinter window
        fig_canvas = FigureCanvasTkAgg(plt.gcf(), master=self.master)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().grid(row=4, column=0, columnspan=5, padx=10, pady=5)

    def save_data(self):
        with open("electricity_data.txt", "w") as file:
            file.write(f"Total Units: {self.total_units}\n")
            file.write(f"Total Days: {self.total_days}\n")
            file.write(f"Remaining Units: {self.remaining_units}\n")
            file.write(f"Remaining Days: {self.remaining_days}\n")
            file.write("Timestamp,Units Used\n")
            for timestamp, usage in self.usage_history:
                file.write(f"{timestamp},{usage}\n")

    def load_data(self):
        try:
            with open("electricity_data.txt", "r") as file:
                lines = file.readlines()
                self.total_units = int(lines[0].split(": ")[1])
                self.total_days = int(lines[1].split(": ")[1])
                self.remaining_units = float(lines[2].split(": ")[1])
                self.remaining_days = int(lines[3].split(": ")[1])
                self.usage_history = []
                for line in lines[5:]:
                    timestamp, usage = line.strip().split(",")
                    self.usage_history.append((timestamp, float(usage)))
        except FileNotFoundError:
            pass

    def check_remaining_units(self):
        if self.remaining_units < 3:
            messagebox.showwarning("Low Units", "Your remaining units are running low.")
        if self.remaining_days == 0:
            messagebox.showinfo("Daily Goal Exceeded", "You have exceeded your daily usage goal.")

    def confirm_reset(self):
        response = messagebox.askquestion("Reset Confirmation", "Are you sure you want to reset your stats?")
        if response == "yes":
            self.reset()

    def reset(self):
        self.remaining_units = self.total_units
        self.remaining_days = self.total_days
        self.usage_history = []
        self.label_message.config(text="Usage data has been reset.")
        self.save_data()  # Save the reset data

        # Reload the GUI with updated values
        self.entry_total_units.delete(0, tk.END)
        self.entry_total_units.insert(0, str(self.total_units))
        self.entry_total_days.delete(0, tk.END)
        self.entry_total_days.insert(0, str(self.total_days))

    def smart_meter(self):
        # Prompt user for smart meter options
        choice = messagebox.askyesno("Smart Meter", "Do you want to generate random usage data?")
        if choice:
            self.generate_random_data()
        else:
            self.custom_usage_data()

    def generate_random_data(self):
        # Generate random usage data
        units_used = round(random.uniform(0.5, 5.0), 2)  # Random units used between 0.5 and 5.0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.remaining_units -= units_used
        self.remaining_days -= 1
        self.usage_history.append((timestamp, units_used))
        self.label_message.config(text=f"{units_used} units used. Remaining units: {self.remaining_units}, Remaining days: {self.remaining_days}")
        self.check_remaining_units()  # Check remaining units after usage

    def custom_usage_data(self):
        # Prompt user to input custom usage data
        units_used = simpledialog.askfloat("Custom Usage Data", "Enter units used:")
        if units_used is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.remaining_units -= units_used
            self.remaining_days -= 1
            self.usage_history.append((timestamp, units_used))
            self.label_message.config(text=f"{units_used} units used. Remaining units: {self.remaining_units}, Remaining days: {self.remaining_days}")
            self.check_remaining_units()  # Check remaining units after usage

    def energy_saving_tips(self):
        # Implement your energy-saving tips algorithm here based on the usage history
        # You can provide suggestions such as reducing usage during peak hours, turning off lights when not in use, etc.
        messagebox.showinfo("Energy Saving Tips", "Here are some energy-saving tips:\n1. Turn off lights and appliances when not in use.\n2. Use energy-efficient LED bulbs.\n3. Set thermostat to an energy-saving temperature.")

def main():
    root = tk.Tk()
    app = ElectricityManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
