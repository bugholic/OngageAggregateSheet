import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from threading import Timer
    
    
def browse_file(entry):
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
    except Exception as e:
        result_label.config(text=f"Error browsing file: {str(e)}")

def copy_data():
    try:
        # Load the first Excel sheet
        sheet1_path = entry_sheet1.get()
        sheet1_df = pd.read_excel(sheet1_path)

        # Load the second Excel sheet
        sheet2_path = entry_sheet2.get()
        sheet2_df = pd.read_excel(sheet2_path)

        # Specify the common column name (ID in this example)
        common_column_sheet1 = 'CID'
        common_column_sheet2 = 'EVENT ID'

        # Find common IDs between both sheets
        # sheet2Id = sheet2_df[common_column_sheet2].values
        # removedSpaces = sheet2Id.replace.drop_duplicates().str.replace(" ", "")
        common_ids = set(sheet1_df[common_column_sheet1].values) & set(sheet2_df[common_column_sheet2].values)

        # Check if there are common IDs
        if common_ids:
            total_steps = len(common_ids)
            progress_bar['maximum'] = total_steps
            
            column_mapping = {
                'Sent': 'Count',
                'Opens': 'G_OPEN',
                'Unique Opens': 'Open',
                'Clicks': 'G_CLICK',
                'Unique Clickers': 'Clicks',
                'Unsubscribes': 'Unsub',
                'Soft Bounces': 'Soft Bounces',
                'Hard Bounces': 'Hard Bounces',
                'Failed': 'Failed',
                'Complaints': 'Complaints',
                # Add more mappings as needed
            }
            
            # Iterate over common IDs and copy data from sheet1 to sheet2
            for step, common_id in enumerate(common_ids, 1):
                progress_bar['value'] = step
                root.update_idletasks()  # Update the GUI

                # Get the row with the common ID from sheet1
                selected_row_from_sheet1 = sheet1_df[sheet1_df[common_column_sheet1] == common_id]

                # Check if there are any rows with the common ID in sheet2
                if not sheet2_df[sheet2_df[common_column_sheet2] == common_id].empty:
                    # Get the row index in sheet2_df
                    sheet2_index = sheet2_df[sheet2_df[common_column_sheet2] == common_id].index[0]

                    # Iterate over columns and copy data from sheet1 to sheet2 using the mapping
                    for col_sheet1, col_sheet2 in column_mapping.items():
                        result_label.config(text= f"Relax \n Data Copy In Process {sheet2_index}%")
                        sheet2_df.at[sheet2_index, col_sheet2] = selected_row_from_sheet1.at[selected_row_from_sheet1.index[0], col_sheet1]

            # Save the updated sheet2
            sheet2_df.to_excel(sheet2_path, index=False)
            result_label.config(text="Data for common IDs copied successfully.")
        else:
            result_label.config(text="No common IDs found between both sheets.")
    except Exception as e:
        result_label.config(text=f"Error copying data: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Coded By AYUV🥇")

# Create and place widgets
label_sheet1 = tk.Label(root, text="Main Data Sheet:")
label_sheet1.grid(row=0, column=0, padx=10, pady=5, sticky="e")

entry_sheet1 = tk.Entry(root, width=40)
entry_sheet1.grid(row=0, column=1, padx=10, pady=5)


button_browse_sheet1 = tk.Button(root, text="Browse", command=lambda: browse_file(entry_sheet1))
button_browse_sheet1.grid(row=0, column=2, pady=5)

label_sheet2 = tk.Label(root, text="Data Entry Sheet:")
label_sheet2.grid(row=1, column=0, padx=10, pady=5, sticky="e")

entry_sheet2 = tk.Entry(root, width=40)
entry_sheet2.grid(row=1, column=1, padx=10, pady=5)

button_browse_sheet2 = tk.Button(root, text="Browse", command=lambda: browse_file(entry_sheet2))
button_browse_sheet2.grid(row=1, column=2, pady=5)

button_copy_data = tk.Button(root, text="Copy Data", command=copy_data)
button_copy_data.grid(row=2, column=1, pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
progress_bar.grid(row=3, column=0, columnspan=3, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=3, pady=10)

result_label.config(text= "Select Files To Start")
root.mainloop()