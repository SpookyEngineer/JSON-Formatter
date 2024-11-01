import json
import tkinter as tk
from tkinter import messagebox, scrolledtext, PanedWindow, PhotoImage

class JsonFormatterApp:
    def __init__(self, master):
        self.master = master
        self.result_indices = []  # Store indices of found results
        self.current_result = 0  # Track the current result index
        
        self.create_widgets()

    def create_widgets(self):
        # Create a PanedWindow to hold input and output side by side
        self.paned_window = PanedWindow(self.master, orient=tk.HORIZONTAL, sashrelief=tk.GROOVE, sashwidth=5)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the input section
        input_frame = tk.Frame(self.paned_window)
        input_label = tk.Label(input_frame, text="Paste your JSON here:")
        input_label.pack()

        # Create a scrollable text area for JSON input
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=40, height=20)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add the input frame to the paned window
        self.paned_window.add(input_frame)

        # Create a frame for the output section
        output_frame = tk.Frame(self.paned_window)
        output_label = tk.Label(output_frame, text="Formatted JSON:")
        output_label.pack()

        # Create a scrollable text area for formatted JSON output, and make it read-only
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=40, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.output_text.config(state=tk.DISABLED)  # Make the output box read-only

        # Add the output frame to the paned window
        self.paned_window.add(output_frame)

        # Create a frame to hold buttons side by side
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=5)

        # Create a button to format the JSON
        format_button = tk.Button(button_frame, text="Format JSON", command=self.format_json)
        format_button.pack(side=tk.LEFT, padx=5)

        # Create a button to copy the formatted JSON to the clipboard
        copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_button.pack(side=tk.LEFT, padx=5)

        # Create a button to clear the input JSON
        clear_button = tk.Button(button_frame, text="Clear Input", command=self.clear_input)
        clear_button.pack(side=tk.LEFT, padx=5)

        # Label to show "Copied!" message
        self.copied_label = tk.Label(self.master, text="", fg="green")
        self.copied_label.pack()

        # Create a search box
        search_frame = tk.Frame(self.master)
        search_label = tk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Create a button for the search
        search_button = tk.Button(search_frame, text="Search", command=self.search_json)
        search_button.pack(side=tk.LEFT, padx=5)

        self.result_count_label = tk.Label(search_frame, text="")
        self.result_count_label.pack(side=tk.LEFT, padx=5)

        # Create next and previous buttons for navigation
        self.prev_button = tk.Button(search_frame, text="Previous", command=self.show_previous_result, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(search_frame, text="Next", command=self.show_next_result, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Label for loop alert messages
        self.loop_alert_label = tk.Label(self.master, text="", fg="red")
        self.loop_alert_label.pack()

        search_frame.pack(pady=5, fill=tk.X)

        # Bind the Return key (Enter) to the search function
        self.search_entry.bind("<Return>", lambda event: self.search_json())

    def format_json(self):
        try:
            # Get JSON input from the text box
            json_input = self.input_text.get("1.0", tk.END)
            
            # Parse the JSON
            parsed_json = json.loads(json_input)
            
            # Pretty print the JSON with indentation
            formatted_json = json.dumps(parsed_json, indent=4)
            
            # Display the formatted JSON in the output text box
            self.output_text.config(state=tk.NORMAL)  # Enable writing to the output text box
            self.output_text.delete("1.0", tk.END)  # Clear previous content
            self.output_text.insert(tk.END, formatted_json)
            self.output_text.config(state=tk.DISABLED)  # Make output text box read-only
            
        except json.JSONDecodeError as e:
            messagebox.showerror("Invalid JSON", f"Error parsing JSON: {e}")

    def clear_input(self):
        # Clear the JSON input text box
        self.input_text.delete("1.0", tk.END)

    def copy_to_clipboard(self):
        # Copy the content of the output_text to the clipboard
        self.master.clipboard_clear()  # Clear the clipboard
        self.master.clipboard_append(self.output_text.get("1.0", tk.END))  # Append the output text content
        
        # Show "Copied!" message in the label
        self.copied_label.config(text="Copied!")
        
        # Hide the label after 2 seconds (2000 milliseconds)
        self.master.after(2000, lambda: self.copied_label.config(text=""))

    def search_json(self):
        # Clear previous highlights
        self.output_text.tag_remove("highlight", "1.0", tk.END)
        self.output_text.tag_remove("current", "1.0", tk.END)  # Remove current result highlights
        self.result_indices.clear()  # Clear previous result indices
        self.current_result = 0  # Reset current result index

        search_term = self.search_entry.get()
        
        if search_term:
            start_index = "1.0"
            while True:
                start_index = self.output_text.search(search_term, start_index, nocase=True, stopindex=tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(search_term)}c"
                self.output_text.tag_add("highlight", start_index, end_index)  # Highlight all occurrences
                self.result_indices.append((start_index, end_index))  # Store found indices
                start_index = end_index

            self.output_text.tag_config("highlight", background="yellow")
            self.result_count_label.config(text=f"Results found: {len(self.result_indices)}")
            self.update_navigation_buttons()
            self.highlight_current_result()
        else:
            self.result_count_label.config(text="")
            self.update_navigation_buttons()

    def highlight_current_result(self):
        # Highlight the current result and scroll to it
        if self.result_indices:
            # Remove previous current highlight
            self.output_text.tag_remove("current", "1.0", tk.END)  

            # Highlight all results again to ensure they are yellow
            for start, end in self.result_indices:
                self.output_text.tag_add("highlight", start, end)  # Re-highlight all results
            
            # Highlight the current result in a different color
            start_index, end_index = self.result_indices[self.current_result]
            self.output_text.tag_add("current", start_index, end_index)  # Highlight current in a different color
            self.output_text.tag_config("current", background="lightgreen")  # Current result highlight color
            self.output_text.see(start_index)  # Scroll to the current result

    def update_navigation_buttons(self):
        # Enable or disable navigation buttons based on the current result index
        self.prev_button.config(state=tk.NORMAL if self.result_indices else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.result_indices else tk.DISABLED)

    def show_next_result(self):
        # Move to the next search result
        if self.result_indices:
            self.current_result = (self.current_result + 1) % len(self.result_indices)  # Loop to the start
            
            # Check if we looped back to the start
            if self.current_result == 0:
                self.loop_alert_label.config(text="Looping back to the beginning!")
                self.master.after(2000, lambda: self.loop_alert_label.config(text=""))  # Clear alert after 2 seconds
            
            self.highlight_current_result()
            self.update_navigation_buttons()

    def show_previous_result(self):
        # Move to the previous search result
        if self.result_indices:
            self.current_result = (self.current_result - 1) % len(self.result_indices)  # Loop to the end
            
            # Check if we looped back to the end
            if self.current_result == len(self.result_indices) - 1:
                self.loop_alert_label.config(text="Looping back to the end!")
                self.master.after(2000, lambda: self.loop_alert_label.config(text=""))  # Clear alert after 2 seconds
            
            self.highlight_current_result()
            self.update_navigation_buttons()

# Create the main window
root = tk.Tk()

root.title("JSON Formatter")
root.geometry("800x600")

# Start the application
app = JsonFormatterApp(root)

root.mainloop()
