import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

def get_current_time():
    # Replace the return value with the current time for production use
    return datetime.now().replace(hour=14, minute=30)  # Example for testing purposes

def calculate_hire():
    try:
        boat_number = int(boat_number_entry.get())
        hours = int(hours_entry.get())
        minutes = int(minutes_entry.get())

        # Validate inputs
        if not 1 <= boat_number <= 10:
            raise ValueError("Boat number must be between 1 and 10.")
        if hours < 0 or minutes < 0 or minutes >= 60:
            raise ValueError("Invalid duration entered.")
        if hours == 0 and minutes == 0:
            raise ValueError("Duration cannot be zero.")

        # Check current time and calculate end time
        current_time = get_current_time()
        opening_time = current_time.replace(hour=10, minute=0, second=0, microsecond=0)
        closing_time = current_time.replace(hour=17, minute=0, second=0, microsecond=0)

        if current_time < opening_time:
            raise ValueError("Boats cannot be hired before 10:00.")
        if current_time >= closing_time:
            raise ValueError("No more boats can be hired today after 17:00.")

        end_time = current_time + timedelta(hours=hours, minutes=minutes)
        if end_time > closing_time:
            raise ValueError(f"Boat cannot be returned after 17:00. Current time: {current_time.strftime('%H:%M')}")

        # Calculate cost and update records
        cost = hours * 20 + (12 if minutes > 0 else 0)
        boat_money[boat_number - 1] += cost
        boat_hours[boat_number - 1] += hours + minutes / 60
        boat_return_times[boat_number - 1] = end_time

        output_label.config(text=f"Boat {boat_number} hired for {hours} hours and {minutes} minutes.\n"
                                 f"Cost: ${cost}\nReturn by: {end_time.strftime('%H:%M')}")

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))


def show_totals():
    total_money = sum(boat_money)
    total_hours = sum(boat_hours)
    totals_label.config(text=f"Total money: ${total_money}\nTotal hours: {total_hours:.2f} hours")

def find_next_available_boat():
    current_time = datetime.now()
    available_boats = [i + 1 for i, time in enumerate(boat_return_times) if time <= current_time]
    if available_boats:
        available_boats_label.config(text=f"Available Boats: {', '.join(map(str, available_boats))}")
    else:
        next_available_time = min(boat_return_times)
        available_boats_label.config(text=f"No boats available. Next available at: {next_available_time.strftime('%H:%M')}")

def generate_end_of_day_report():
    total_money = sum(boat_money)
    total_hours = sum(boat_hours)
    boats_not_used = boat_money.count(0)
    most_used_boat = max(range(len(boat_hours)), key=lambda i: boat_hours[i]) + 1
    most_used_hours = boat_hours[most_used_boat - 1]
    
    report = (f"End of Day Report:\n"
              f"Total money taken: ${total_money}\n"
              f"Total hours hired: {total_hours:.2f}\n"
              f"Boats not used: {boats_not_used}\n"
              f"Boat used the most: Boat {most_used_boat} (Used for {most_used_hours:.2f} hours)")
    
    report_label.config(text=report)

# Initialize data storage
boat_money = [0] * 10
boat_hours = [0] * 10
boat_return_times = [datetime.now().replace(hour=9, minute=59)] * 10

# Set up the GUI
root = tk.Tk()
root.title("River Boat Hire System")

# Input fields for boat number, hours, and minutes hired
tk.Label(root, text="Boat Number (1-10):").pack()
boat_number_entry = tk.Entry(root)
boat_number_entry.pack()

tk.Label(root, text="Hours Hired:").pack()
hours_entry = tk.Entry(root)
hours_entry.pack()

tk.Label(root, text="Minutes Hired:").pack()
minutes_entry = tk.Entry(root)
minutes_entry.pack()

# Buttons and labels for interaction
tk.Button(root, text="Calculate Hire", command=calculate_hire).pack()
output_label = tk.Label(root, text="")
output_label.pack()

tk.Button(root, text="Show Totals", command=show_totals).pack()
totals_label = tk.Label(root, text="")
totals_label.pack()

tk.Button(root, text="Find Next Available Boat", command=find_next_available_boat).pack()
available_boats_label = tk.Label(root, text="")
available_boats_label.pack()

tk.Button(root, text="Generate End of Day Report", command=generate_end_of_day_report).pack()
report_label = tk.Label(root, text="")
report_label.pack()

root.mainloop()