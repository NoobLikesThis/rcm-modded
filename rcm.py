import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import json

class RobloxFileReplacer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Roblox File Replacer")
        self.geometry("800x600")
        self.configure(bg="#212326")

        # Directories
        local_appdata = os.getenv('LOCALAPPDATA')
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.http_dir = os.path.join(local_appdata, 'Temp', 'Roblox', 'http')
        self.preinstalled_dir = os.path.join(script_dir, 'caches', 'preinstalled')
        self.own_dir = os.path.join(script_dir, 'caches', 'Own')
        self.presets_dir = os.path.join(script_dir, 'presets')
        self.functions_file = os.path.join(script_dir, 'functions.json')

        # Ensure folders exist
        for path in (self.http_dir, self.preinstalled_dir, self.own_dir, self.presets_dir):
            os.makedirs(path, exist_ok=True)
        
        # Create functions.json if it doesn't exist with a sample structure
        if not os.path.exists(self.functions_file):
            try:
                with open(self.functions_file, 'w', encoding='utf-8') as f:
                    json.dump([
                        "ExampleHash123 - Example Function 1",
                        "AnotherHash456 - Example Function 2"
                    ], f, indent=2)
            except Exception as e:
                print(f"Could not create sample functions.json: {e}")


        # Load functions mapping
        self.functions = []
        try:
            with open(self.functions_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            # Expect data to be a list of strings like "hash - description"
            if isinstance(data, list):
                lines = data
            else: # Fallback for old plain text format or incorrect JSON root
                lines = [] 
                print(f"Warning: {self.functions_file} is not a JSON list. Treating as empty.")
        except json.JSONDecodeError:
            # Fallback to plain text if JSON parsing fails
            print(f"Warning: {self.functions_file} is not valid JSON. Attempting to read as plain text.")
            try:
                with open(self.functions_file, 'r', encoding='utf-8-sig') as f:
                    lines = [l.strip() for l in f if l.strip()]
            except Exception as e:
                lines = []
                print(f"Error reading {self.functions_file} as plain text: {e}")
        except FileNotFoundError:
            lines = []
            print(f"Warning: {self.functions_file} not found. No pre-defined functions will be loaded.")
        except Exception as e:
            lines = []
            print(f"An unexpected error occurred while loading {self.functions_file}: {e}")

        for entry in lines:
            if isinstance(entry, str) and ' - ' in entry:
                key, disp = entry.split(' - ', 1)
                self.functions.append((key.strip(), disp.strip()))
            elif isinstance(entry, str): # Handle lines without " - " if any
                self.functions.append((entry.strip(), entry.strip()))


        # Style for futuristic look
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#2e2e3d')
        style.configure('TLabel', background='#2e2e3d', foreground='#c7c7d9', font=('Segoe UI', 11))
        style.configure('TButton', background='#3a3a51', foreground='#ffffff', font=('Segoe UI Semibold', 10), padding=6)
        style.map('TButton', background=[('active', '#4f4f73')])
        style.configure('TRadiobutton', background='#2e2e3d', foreground='#c7c7d9', font=('Segoe UI', 10))
        style.map('TRadiobutton', indicatorcolor=[('selected', '#6a6aff'), ('!selected', '#3a3a51')], background=[('active', '#38384a')])
        style.configure('TListbox', background='#1e1e2a', foreground='#ffffff', font=('Consolas', 10))
        style.configure('TCombobox', background='#1e1e2a', foreground='#ffffff', fieldbackground='#1e1e2a', selectbackground='#4f4f73', font=('Segoe UI', 10))
        style.map('TCombobox', fieldbackground=[('readonly', '#1e1e2a')], foreground=[('readonly', '#ffffff')])
        style.configure('TEntry', background='#1e1e2a', foreground='#ffffff', fieldbackground='#1e1e2a', insertcolor='#ffffff', font=('Segoe UI', 10))


        # Main layout
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        # Top controls
        top = ttk.Frame(container)
        top.pack(fill='x', pady=(0,10))
        ttk.Label(top, text="Source:").pack(side='left')
        self.source_var = tk.StringVar(value='Caches')
        ttk.Radiobutton(top, text="Caches", variable=self.source_var, value='Caches', command=self.refresh_view).pack(side='left', padx=5)
        ttk.Radiobutton(top, text="Presets", variable=self.source_var, value='Presets', command=self.refresh_view).pack(side='left', padx=5)

        # Middle split
        middle = ttk.Frame(container)
        middle.pack(fill='both', expand=True)

        # List section
        list_frame = ttk.LabelFrame(middle, text="Items", style='TFrame') # Use TFrame style for LabelFrame
        list_frame.pack(side='left', fill='both', expand=True, padx=(0,10))
        self.item_list = tk.Listbox(list_frame, bg='#1e1e2a', fg='#ffffff', font=('Consolas', 10), selectbackground='#4f4f73', relief='flat', borderwidth=0, highlightthickness=0)
        self.item_list.pack(side='left', fill='both', expand=True, pady=5, padx=5)
        scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.item_list.yview)
        scroll.pack(side='right', fill='y')
        self.item_list.config(yscrollcommand=scroll.set)

        # Action buttons
        action_frame = ttk.LabelFrame(middle, text="Actions", style='TFrame') # Use TFrame style for LabelFrame
        action_frame.pack(side='right', fill='y')
        self.btn_apply = ttk.Button(action_frame, text="Apply", command=self.apply_selected)
        self.btn_apply.pack(fill='x', padx=10, pady=(10,5))
        self.btn_create = ttk.Button(action_frame, text="Create Cache", command=self.create_cache)
        self.btn_create.pack(fill='x', padx=10, pady=5)
        self.btn_clear = ttk.Button(action_frame, text="Clear HTTP Folder", command=self.clear_http_folder)
        self.btn_clear.pack(fill='x', padx=10, pady=5)

        self.refresh_view()

    def refresh_view(self):
        self.item_list.delete(0, tk.END)
        src = self.source_var.get()
        if src == 'Caches':
            # list caches
            for folder in (self.preinstalled_dir, self.own_dir):
                if os.path.exists(folder): # Ensure folder exists before listing
                    for fname in os.listdir(folder):
                        if os.path.isfile(os.path.join(folder, fname)) and ' - ' in fname:
                            disp = fname.split(' - ',1)[1]
                            self.item_list.insert(tk.END, disp)
        else:
            # list presets
            if os.path.exists(self.presets_dir): # Ensure folder exists
                for d in os.listdir(self.presets_dir):
                    if os.path.isdir(os.path.join(self.presets_dir, d)):
                        self.item_list.insert(tk.END, d)

    def apply_selected(self):
        sel = self.item_list.curselection()
        if not sel:
            messagebox.showerror("Error", "No item selected.", parent=self)
            return
        item_display_name = self.item_list.get(sel)
        if self.source_var.get() == 'Caches':
            found_cache = False
            for folder in (self.preinstalled_dir, self.own_dir):
                if os.path.exists(folder):
                    for fname in os.listdir(folder):
                        if fname.endswith(f"- {item_display_name}"): # Match by display name part
                            actual_hash = fname.split(' - ',1)[0]
                            source_path = os.path.join(folder, fname)
                            target_path = os.path.join(self.http_dir, actual_hash)
                            try:
                                shutil.copy2(source_path, target_path)
                                messagebox.showinfo("Success", f"Applied '{item_display_name}'\n(Hash: {actual_hash})\nto HTTP folder.", parent=self)
                                found_cache = True
                                return # Exit after applying
                            except Exception as e:
                                messagebox.showerror("Error", f"Failed to apply cache: {e}", parent=self)
                                return
            if not found_cache:
                 messagebox.showerror("Error", f"Cache file for '{item_display_name}' not found.", parent=self)

        else: # Apply preset
            preset_folder_path = os.path.join(self.presets_dir, item_display_name)
            if not os.path.isdir(preset_folder_path):
                messagebox.showerror("Error", f"Preset folder '{item_display_name}' not found.", parent=self)
                return
            
            count = 0
            try:
                for f_preset_name in os.listdir(preset_folder_path):
                    if ' - ' in f_preset_name: # Ensure it's a cache file format
                        key_hash = f_preset_name.split(' - ',1)[0]
                        src_path = os.path.join(preset_folder_path, f_preset_name)
                        dst_path = os.path.join(self.http_dir, key_hash)
                        shutil.copy2(src_path, dst_path)
                        count += 1
                messagebox.showinfo("Success", f"Applied {count} files from preset '{item_display_name}'.", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply preset: {e}", parent=self)


    def create_cache(self):
        if self.source_var.get() != 'Caches':
            messagebox.showerror("Error", "Switch to 'Caches' source to create a new cache file.", parent=self)
            return

        src_filepath = filedialog.askopenfilename(
            title="Select Source File for Cache",
            parent=self
        )
        if not src_filepath:
            return

        dialog = tk.Toplevel(self)
        dialog.title("Create New Cache")
        dialog.geometry("450x300") # Adjusted dialog size
        dialog.configure(bg='#212326')
        dialog.transient(self)
        dialog.grab_set()

        # --- Hash input mode ---
        hash_input_mode_var = tk.StringVar(value="dropdown")

        # Main frame for content in dialog
        content_frame = ttk.Frame(dialog, padding="10 10 10 10")
        content_frame.pack(expand=True, fill='both')
        
        # --- Hash source selection ---
        hash_source_frame = ttk.Frame(content_frame)
        hash_source_frame.pack(pady=(0,10), fill='x')
        ttk.Label(hash_source_frame, text="Hash Source:").pack(side='left', anchor='w')
        
        rb_dropdown = ttk.Radiobutton(hash_source_frame, text="Select from List", variable=hash_input_mode_var, value="dropdown")
        rb_dropdown.pack(side='left', padx=(10, 5))
        rb_custom = ttk.Radiobutton(hash_source_frame, text="Custom Hash", variable=hash_input_mode_var, value="custom")
        rb_custom.pack(side='left', padx=5)

        # --- Dropdown for function selection ---
        dropdown_frame = ttk.Frame(content_frame)
        dropdown_frame.pack(pady=5, fill='x')
        ttk.Label(dropdown_frame, text="Select Function:").pack(side='left', anchor='w', padx=(0,10))
        combo_values = [d for _, d in self.functions]
        combo_func = ttk.Combobox(dropdown_frame, values=combo_values, state='readonly', width=35)
        if combo_values:
            combo_func.current(0)
        else:
            combo_func.set("No functions defined") # Placeholder if empty
        combo_func.pack(side='left', expand=True, fill='x')

        # --- Entry for custom hash ---
        custom_hash_frame = ttk.Frame(content_frame)
        custom_hash_frame.pack(pady=5, fill='x')
        ttk.Label(custom_hash_frame, text="Custom Hash:").pack(side='left', anchor='w', padx=(0,20)) # Adjusted padding
        custom_hash_entry = ttk.Entry(custom_hash_frame, width=35)
        custom_hash_entry.pack(side='left', expand=True, fill='x')

        # --- Entry for display name ---
        display_name_frame = ttk.Frame(content_frame)
        display_name_frame.pack(pady=(5,10), fill='x')
        ttk.Label(display_name_frame, text="Display Name:").pack(side='left', anchor='w', padx=(0,15)) # Adjusted padding
        display_name_entry = ttk.Entry(display_name_frame, width=35)
        display_name_entry.pack(side='left', expand=True, fill='x')
        
        # Function to toggle input states
        def toggle_hash_inputs(*args): # Added *args for trace
            mode = hash_input_mode_var.get()
            if mode == "dropdown":
                combo_func.configure(state='readonly' if combo_values else 'disabled')
                if combo_values and not combo_func.get() and combo_funccget("state") != 'disabled':
                    combo_func.current(0)
                custom_hash_entry.configure(state='disabled')
                custom_hash_entry.delete(0, tk.END)
            else: # mode == "custom"
                combo_func.configure(state='disabled')
                custom_hash_entry.configure(state='normal')
                custom_hash_entry.focus() # Set focus to custom hash entry

        hash_input_mode_var.trace_add("write", toggle_hash_inputs) # Call toggle when var changes
        toggle_hash_inputs() # Initial call to set state

        if not combo_values: # If no functions, default to custom hash input
            hash_input_mode_var.set("custom")
            toggle_hash_inputs() # Update UI based on new default

        # --- OK/Cancel buttons ---
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(pady=(10,0), fill='x', side='bottom') # Pack at bottom
        
        # Center buttons
        center_btn_frame = ttk.Frame(btn_frame) # Sub-frame to center buttons
        center_btn_frame.pack(anchor='center')

        ok_button = ttk.Button(center_btn_frame, text="OK")
        ok_button.pack(side='left', padx=5)
        cancel_button = ttk.Button(center_btn_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side='left', padx=5)

        def on_ok():
            display_name = display_name_entry.get().strip()
            cache_hash_key = None

            if hash_input_mode_var.get() == "dropdown":
                if not combo_values:
                    messagebox.showerror("Error", "No functions available in the dropdown. Please add to functions.json or use 'Custom Hash'.", parent=dialog)
                    return
                selected_function_display = combo_func.get()
                if not selected_function_display or selected_function_display == "No functions defined":
                    messagebox.showerror("Error", "Please select a function from the dropdown.", parent=dialog)
                    return
                cache_hash_key = next((k for k, d in self.functions if d == selected_function_display), None)
            else: # Custom hash
                cache_hash_key = custom_hash_entry.get().strip()
            
            if not cache_hash_key:
                messagebox.showerror("Error", "Cache Hash is required. Please enter a custom hash or select a function.", parent=dialog)
                return
            if not display_name:
                messagebox.showerror("Error", "Display Name is required.", parent=dialog)
                return

            # Basic hash validation (alphanumeric, example)
            if not cache_hash_key.isalnum() or len(cache_hash_key) < 5: # Example simple validation
                 if not messagebox.askyesno("Confirm Hash", f"The hash '{cache_hash_key}' seems unusual. Are you sure it's correct?", parent=dialog):
                    return

            dialog.destroy() # Close dialog after validation

            final_filename = f"{cache_hash_key} - {display_name}"
            target_path = os.path.join(self.own_dir, final_filename)

            if os.path.exists(target_path):
                if not messagebox.askyesno("Confirm Overwrite", f"Cache '{final_filename}' already exists in 'Own' caches. Overwrite?", parent=self):
                    return
            
            try:
                shutil.copy2(src_filepath, target_path)
                self.refresh_view() # Refresh list to show new cache
                messagebox.showinfo("Success", f"Cache '{final_filename}' created successfully in 'Own' caches.", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create cache: {e}", parent=self)

        ok_button.config(command=on_ok)
        display_name_entry.bind("<Return>", lambda event: on_ok()) # Enter key submits
        custom_hash_entry.bind("<Return>", lambda event: on_ok())

        dialog.wait_window()


    def clear_http_folder(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to delete all files and folders within the Roblox HTTP cache folder?", parent=self):
            cleared_count = 0
            failed_count = 0
            if not os.path.exists(self.http_dir):
                messagebox.showinfo("Info", "HTTP cache folder does not exist. Nothing to clear.", parent=self)
                return

            for item_name in os.listdir(self.http_dir):
                item_path = os.path.join(self.http_dir, item_name)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    cleared_count += 1
                except Exception as e:
                    print(f"Failed to delete {item_path}: {e}")
                    failed_count += 1
            
            if failed_count > 0:
                messagebox.showwarning("Partial Success", f"Cleared {cleared_count} items. Failed to clear {failed_count} items (see console for details).", parent=self)
            else:
                messagebox.showinfo("Success", f"Successfully cleared {cleared_count} items from the HTTP cache folder.", parent=self)

if __name__=='__main__':
    app = RobloxFileReplacer()
    app.mainloop()
