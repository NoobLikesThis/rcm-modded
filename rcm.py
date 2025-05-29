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

        # Load functions mapping
        self.functions = []
        try:
            with open(self.functions_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            lines = data if isinstance(data, list) else []
        except Exception:
            try: # Fallback to reading as plain text if JSON parsing fails or file not found initially
                with open(self.functions_file, 'r', encoding='utf-8-sig') as f:
                    lines = [l.strip() for l in f if l.strip()]
            except FileNotFoundError: # If functions.json doesn't exist at all
                lines = [] # self.functions will be empty
                # Optionally, create an empty functions.json here or notify user
                # For now, just means the dropdown will be empty.
            except Exception: # Other read errors
                lines = []


        for entry_text in lines: # Renamed 'entry' to 'entry_text' to avoid conflict
            if ' - ' in entry_text:
                key, disp = entry_text.split(' - ', 1)
                self.functions.append((key.strip(), disp.strip()))

        # Style for futuristic look
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#2e2e3d')
        style.configure('TLabel', background='#2e2e3d', foreground='#c7c7d9', font=('Segoe UI', 11))
        style.configure('TButton', background='#3a3a51', foreground='#ffffff', font=('Segoe UI Semibold', 10), padding=6)
        style.map('TButton', background=[('active', '#4f4f73')])
        style.configure('TRadiobutton', background='#2e2e3d', foreground='#c7c7d9', font=('Segoe UI', 10))
        style.configure('TListbox', background='#1e1e2a', foreground='#ffffff', font=('Consolas', 10))
        # Ensure ttk.Entry and ttk.Checkbutton also fit the theme (usually automatic)
        style.configure('TEntry', fieldbackground='#1e1e2a', foreground='#ffffff', insertcolor='#ffffff', font=('Segoe UI', 10))
        style.configure('TCombobox', fieldbackground='#1e1e2a', foreground='#ffffff', selectbackground='#1e1e2a', selectforeground='#ffffff', font=('Segoe UI', 10))
        style.map('TCombobox', fieldbackground=[('readonly', '#1e1e2a')]) # Ensure readonly looks consistent
        style.configure('TCheckbutton', background='#2e2e3d', foreground='#c7c7d9', font=('Segoe UI', 10))
        style.map('TCheckbutton', indicatorcolor=[('selected', '#4f4f73'), ('!selected', '#1e1e2a')],
                  background=[('active', '#2e2e3d')])


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
        list_frame = ttk.LabelFrame(middle, text="Items")
        list_frame.pack(side='left', fill='both', expand=True, padx=(0,10))
        self.item_list = tk.Listbox(list_frame, bg='#1e1e2a', fg='#ffffff', font=('Consolas', 10), selectbackground='#4f4f73', highlightthickness=0, borderwidth=0)
        self.item_list.pack(side='left', fill='both', expand=True, pady=5, padx=5)
        scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.item_list.yview)
        scroll.pack(side='right', fill='y')
        self.item_list.config(yscrollcommand=scroll.set)

        # Action buttons
        action_frame = ttk.LabelFrame(middle, text="Actions")
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
                for fname in os.listdir(folder):
                    if os.path.isfile(os.path.join(folder, fname)) and ' - ' in fname:
                        disp = fname.split(' - ',1)[1]
                        self.item_list.insert(tk.END, disp)
        else:
            # list presets
            for d in os.listdir(self.presets_dir):
                if os.path.isdir(os.path.join(self.presets_dir, d)):
                    self.item_list.insert(tk.END, d)

    def apply_selected(self):
        sel = self.item_list.curselection()
        if not sel:
            messagebox.showerror("Error", "No item selected.")
            return
        item = self.item_list.get(sel[0]) # get expects index, curselection returns tuple
        if self.source_var.get() == 'Caches':
            # apply cache
            # find file in caches
            found = False
            for folder in (self.preinstalled_dir, self.own_dir):
                for fname in os.listdir(folder):
                    if fname.endswith(f"- {item}"): # Make sure this logic is robust
                        key = fname.split(' - ',1)[0]
                        try:
                            shutil.copy2(os.path.join(folder, fname), os.path.join(self.http_dir, key))
                            messagebox.showinfo("Success", f"Replaced {key} in HTTP folder.")
                            found = True
                            return # Exit after first find and apply
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to apply cache {fname}: {e}")
                            return
            if not found:
                 messagebox.showerror("Error", f"Cache file for '{item}' not found.")

        else:
            # apply preset
            folder = os.path.join(self.presets_dir, item)
            cnt=0
            try:
                for f in os.listdir(folder):
                    if os.path.isfile(os.path.join(folder, f)) and ' - ' in f: # Ensure it's a file and valid format
                        key = f.split(' - ',1)[0]
                        shutil.copy2(os.path.join(folder, f), os.path.join(self.http_dir, key))
                        cnt+=1
                if cnt > 0:
                    messagebox.showinfo("Success", f"Applied {cnt} files from preset {item}.")
                else:
                    messagebox.showinfo("Info", f"No valid cache files found in preset {item}.")
            except Exception as e:
                 messagebox.showerror("Error", f"Failed to apply preset {item}: {e}")


    def create_cache(self):
        if self.source_var.get() != 'Caches':
            messagebox.showerror("Error", "Switch to Caches view to create a new cache file.")
            return
        src = filedialog.askopenfilename(title="Select source file for cache")
        if not src:
            return

        dialog = tk.Toplevel(self)
        dialog.title("Create Cache File")
        dialog.configure(bg='#212326')
        dialog.resizable(False, False) # Dialogs often are not resizable

        custom_hash_var = tk.BooleanVar(value=False)

        ttk.Label(dialog, text="Select function (determines original hash):").pack(padx=10, pady=(10,0))
        # Use display names from self.functions for Combobox values
        combo_values = [d for _, d in self.functions]
        combo = ttk.Combobox(dialog, values=combo_values, state='readonly', width=40)
        combo.pack(padx=10, pady=5)
        if self.functions: # If there are functions, select the first one by default
            combo.current(0)
        # else: combobox will be empty, user must use custom hash or be told no functions available

        custom_hash_check = ttk.Checkbutton(dialog, text="Use Custom Hash", variable=custom_hash_var)
        custom_hash_check.pack(padx=10, pady=(5,0))

        custom_hash_label = ttk.Label(dialog, text="Enter Custom Hash:")
        custom_hash_label.pack(padx=10, pady=(5,0))
        custom_hash_entry = ttk.Entry(dialog, state='disabled', width=43) # Match width roughly
        custom_hash_entry.pack(padx=10, pady=5)

        ttk.Label(dialog, text="Enter display name for this cache file:").pack(padx=10, pady=(10,0))
        entry = ttk.Entry(dialog, width=43) # This is the 'entry' for display name from original code
        entry.pack(padx=10, pady=5)

        # Function to toggle input states
        def toggle_hash_input_state():
            if custom_hash_var.get():
                combo.config(state='disabled')
                custom_hash_label.config(foreground='#c7c7d9') # Active color
                custom_hash_entry.config(state='normal')
                custom_hash_entry.focus_set()
            else:
                combo.config(state='readonly' if self.functions else 'disabled') # Disable combo if no functions
                custom_hash_label.config(foreground='#888888') # Dimmed color
                custom_hash_entry.config(state='disabled')
                if self.functions:
                    combo.focus_set()
        
        custom_hash_check.config(command=toggle_hash_input_state) # Assign command here

        # Set initial state
        toggle_hash_input_state() # Call once to set initial states correctly

        def on_ok():
            cache_display_name = entry.get().strip()
            final_hash_key = ""

            if custom_hash_var.get():
                final_hash_key = custom_hash_entry.get().strip()
                if not final_hash_key:
                    messagebox.showerror("Input Error", "Custom Hash cannot be empty when 'Use Custom Hash' is checked.", parent=dialog)
                    dialog.lift()
                    custom_hash_entry.focus_set()
                    return
            else: # Use dropdown
                if not self.functions:
                    messagebox.showerror("Configuration Error", "No functions available in the dropdown. Please use a custom hash or add functions to 'functions.json'.", parent=dialog)
                    dialog.lift()
                    return

                selected_function_display_name = combo.get()
                if not selected_function_display_name:
                    messagebox.showerror("Input Error", "Please select a function from the dropdown list.", parent=dialog)
                    dialog.lift()
                    combo.focus_set()
                    return
                
                # Find the original hash (key) corresponding to the selected display name
                found_key = next((k for k, d in self.functions if d == selected_function_display_name), None)
                if not found_key:
                    # This should ideally not happen if combobox is populated correctly and readonly
                    messagebox.showerror("Internal Error", "Selected function not found in mappings. Check 'functions.json'.", parent=dialog)
                    dialog.lift()
                    return
                final_hash_key = found_key
            
            if not cache_display_name:
                messagebox.showerror("Input Error", "Display name for the cache file is required.", parent=dialog)
                dialog.lift()
                entry.focus_set()
                return
            
            # All inputs seem valid, destroy dialog before file operations
            dialog.destroy()

            # Construct filename and copy
            new_cache_filename = f"{final_hash_key} - {cache_display_name}"
            destination_path = os.path.join(self.own_dir, new_cache_filename)

            try:
                shutil.copy2(src, destination_path)
                self.refresh_view() # Refresh the list to show the new cache
                messagebox.showinfo("Success", f"Cache file '{new_cache_filename}' created successfully in 'Own' caches folder.")
            except Exception as e:
                messagebox.showerror("File Error", f"Could not create cache file: {e}")

        btn_frame = ttk.Frame(dialog) # Renamed from btnf for clarity
        btn_frame.pack(pady=10)
        
        ok_button = ttk.Button(btn_frame, text="OK", command=on_ok)
        ok_button.pack(side='left', padx=5)
        cancel_button = ttk.Button(btn_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side='left', padx=5)

        dialog.transient(self)
        dialog.grab_set()
        # Center dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        dialog.wait_window()


    def clear_http_folder(self):
        if messagebox.askyesno("Confirm","Are you sure you want to delete all files and folders within the Roblox HTTP cache folder? This cannot be undone."):
            cnt=0
            err_cnt=0
            for f_or_d in os.listdir(self.http_dir):
                p=os.path.join(self.http_dir,f_or_d)
                try: 
                    if os.path.isdir(p):
                        shutil.rmtree(p)
                    else:
                        os.unlink(p)
                    cnt+=1
                except Exception: # Catch permission errors etc.
                    err_cnt+=1
            
            if err_cnt > 0:
                messagebox.showwarning("Clearing Partially Successful", f"Cleared {cnt} items. Failed to delete {err_cnt} items (possibly in use or permission denied).")
            else:
                messagebox.showinfo("Done", f"Successfully cleared {cnt} items from the HTTP cache folder.")


if __name__=='__main__':
    app = RobloxFileReplacer()
    # Center main window
    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f'{width}x{height}+{x}+{y}')
    app.mainloop()
