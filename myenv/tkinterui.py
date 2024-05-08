import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

def create_date_entry(frame, row, column, text):
    # Calendar
    def get_selected_date():
        selected_date = cal_entry.get_date()
        selected_date_label.config(text=f"{text} Selected Date:{selected_date}" )

    # Date Entry Widget
    cal_entry = DateEntry(frame, width=12, background="darkblue", foreground="white", borderwidth=2)
    cal_entry.grid(row=row, column=column)  # Place the calendar widget in the grid

    # Create a button to get the selected date
    get_date_button = tk.Button(frame, text=f"Get {text} Date", command=get_selected_date)
    get_date_button.grid(row=row+1, column=column)  # Place the button in the grid

    # Create a label to display the selected date
    selected_date_label = tk.Label(frame, text="", font=("Helvetica", 12))
    selected_date_label.grid(row=row+2, column=column)  # Place the label in the grid

window = tk.Tk()
window.title("SEC Filing Scanner")

frame = tk.Frame(window)
frame.pack() 

# Saving Filter Information
filter_info_frame = tk.LabelFrame(frame, text="Filter Information")
filter_info_frame.grid(row=0, column=0, padx=20, pady=20)

# Get Filings Frame
get_filing_frame = tk.LabelFrame(frame, text="Results")
get_filing_frame.grid(row=1, column=0, padx=20, pady=20)

# Saving Filter Words
filter_words_label = tk.Label(filter_info_frame, text="Filter Words")
filter_words_label.grid(row=0, column=0)

filter_words_entry = tk.Entry(filter_info_frame)
filter_words_entry.grid(row=1, column=0)

# Start Date
start_date_label = tk.Label(filter_info_frame, text="Start Date")
start_date_label.grid(row=0, column=1)

create_date_entry(filter_info_frame, 1, 1, "Start")

# End Date
end_date_label = tk.Label(filter_info_frame, text="End Date")
end_date_label.grid(row=0, column=2)

create_date_entry(filter_info_frame, 1, 2, "End")

# Form Types
form_types_label = tk.Label(filter_info_frame, text="Form Type")
form_types_label.grid(row=0, column=3)

form_types_combobox = ttk.Combobox(filter_info_frame, values=[" ","10-K", "10-KT", "10KSB"])
form_types_combobox.grid(row=1, column=3)

# Get Filings Button
get_filings_button = tk.Button(get_filing_frame, text=f"Get Filings")
get_filings_button.grid(row=0,column=0)
window.mainloop()
