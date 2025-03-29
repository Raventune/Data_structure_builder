import tkinter as tk
from tkinter import ttk

def convert_value(value, convert_whole_numbers, convert_floats, keep_as_string):
    """Convert value based on user-selected options for whole numbers, floats, or keep as string."""
    if keep_as_string:
        return str(value)  # Keep the value as a string
    
    if convert_whole_numbers:
        try:
            # Convert to integer if possible
            return int(value)
        except ValueError:
            pass  # Do nothing if it can't be converted to an integer
    
    if convert_floats:
        try:
            # Convert to float if possible
            return float(value)
        except ValueError:
            pass  # Do nothing if it can't be converted to a float
    
    return value  # Return original if no conversion is applied

def generate_code():
    key_value_input = entry.get()
    selected_structure = dropdown.get()
    structure_name = name_entry.get().strip()

    # Get selected options for conversion
    convert_whole_numbers = whole_number_var.get()
    convert_floats = float_var.get()
    keep_as_string = string_var.get()

    # Check if user input is empty
    if not key_value_input.strip():
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Error: Please enter values.")
        return

    # Process input (split by commas and remove extra spaces)
    items = [item.strip() for item in key_value_input.split(',') if item.strip()]

    # Apply conversion based on user's choices
    items = [convert_value(item, convert_whole_numbers, convert_floats, keep_as_string) for item in items]

    # Generate the appropriate data structure
    if selected_structure == "List":
        result = f"{structure_name} = {items}"  # List syntax with the structure name

    elif selected_structure == "Set":
        result = f"{structure_name} = {set(items)}"  # Set syntax (removes duplicates)

    elif selected_structure == "Tuple":
        result = f"{structure_name} = {tuple(items)}"  # Tuple syntax

    elif selected_structure == "Dictionary":
        # Convert items to key-value pairs
        dictionary = {}
        for pair in items:
            if isinstance(pair, str) and ":" in pair:
                key, value = pair.split(":", 1)
                dictionary[convert_value(key.strip(), convert_whole_numbers, convert_floats, keep_as_string)] = convert_value(value.strip(), convert_whole_numbers, convert_floats, keep_as_string)
            else:
                dictionary[convert_value(pair, convert_whole_numbers, convert_floats, keep_as_string)] = None  # Assign None if no value is provided
        result = f"{structure_name} = {dictionary}"

    # Display the result
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

def copy_to_clipboard():
    generated_code = output_text.get("1.0", tk.END).strip()
    
    if generated_code:
        root.clipboard_clear()
        root.clipboard_append(generated_code)
        root.update()
        copy_button.config(text="Copied!", fg="green")
        root.after(1000, lambda: copy_button.config(text="Copy to Clipboard", fg="black"))

# Set up the main window
root = tk.Tk()
root.title("Python Data Structure Generator")

# Input field
tk.Label(root, text="Enter keys/values (comma-separated, use key:value for dictionaries):").pack()
entry = tk.Entry(root, width=50)
entry.pack()

# Name field for the data structure
tk.Label(root, text="Enter a name for the data structure:").pack()
name_entry = tk.Entry(root, width=50)
name_entry.pack()

# Dropdown for selecting data structure
tk.Label(root, text="Select Data Structure:").pack()
dropdown = ttk.Combobox(root, values=["List", "Set", "Tuple", "Dictionary"])
dropdown.pack()
dropdown.current(0)

# Checkboxes for converting numbers
whole_number_var = tk.BooleanVar()
float_var = tk.BooleanVar()
string_var = tk.BooleanVar()

# Whole number conversion checkbox
tk.Checkbutton(root, text="Convert whole numbers", variable=whole_number_var).pack()

# Floating-point conversion checkbox
tk.Checkbutton(root, text="Convert floating-point numbers", variable=float_var).pack()

# Keep as string checkbox
tk.Checkbutton(root, text="Keep as strings", variable=string_var).pack()

# Generate button
generate_button = tk.Button(root, text="Generate", command=generate_code)
generate_button.pack()

# Output text box
tk.Label(root, text="Generated Code:").pack()
output_text = tk.Text(root, height=5, width=50)
output_text.pack()

# Copy to Clipboard button
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack()

# Run the GUI loop
root.mainloop()

