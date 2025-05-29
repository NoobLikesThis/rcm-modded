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
        if not os.path.exists(self.functions_file):
            # Create a dummy functions.json if it doesn't exist
            dummy_data = [
                "00000000000000000000000000000000 - Example Function 1",
                "11111111111111111111111111111111 - Example Function 2"
            ]
            with open(self.functions_file, 'w', encoding='utf-8') as f:
                json.dump(dummy_data, f, indent=2)
            messagebox.showinfo("Setup", f"Created a dummy functions.json. Please edit it with actual hashes and descriptions at:\n{self.functions_file}")

        try:
            with open(self.functions_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            lines = data if isinstance(data, list) else []
        except Exception as e:
            messagebox.showerror("Error loading functions.json", f"Could not load functions.json: {e}\nAssuming it's line-based.")
            lines = [] # Fallback if JSON parsing fails after attempting to read
            try:
                with open(self.functions_file, 'r', encoding='utf-8-sig') as f:
                    lines = [l.strip() for l in f if l.strip()]
            except Exception as e_fallback:
                 messagebox.showerror("Fatal Error", f"Could not read functions.json at all: {e_fallback}")


        for entry in lines:
            if ' - ' in entry:
                key, disp = entry.split(' - ', 1)
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
        style.configure('Combobox.TEntry', fieldbackground='#1e1e2a', foreground='#ffffff', insertcolor='#ffffff') # Style for Combobox entry
        style.map('TCombobox', fieldbackground=[('readonly', '#1e1e2a')], foreground=[('readonly', '#ffffff')])
        style.configure('TEntry', fieldbackground='#1e1e2a', foreground='#ffffff', insertcolor='#ffffff')


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
        self.item_list = tk.Listbox(list_frame, bg='#1e1e2a', fg='#ffffff', font=('Consolas', 10), selectbackground='#4f4f73')
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
            self.item_list.config(bg='#1e1e2a', fg='#ffffff') # Reset color in case it was changed
            # list caches
            for folder in (self.preinstalled_dir, self.own_dir):
                if os.path.exists(folder):
                    for fname in os.listdir(folder):
                        if os.path.isfile(os.path.join(folder, fname)) and ' - ' in fname:
                            disp = fname.split(' - ',1)[1]
                            self.item_list.insert(tk.END, disp)
        else:
            # list presets
            self.item_list.config(bg='#1a2a1a', fg='#ccffcc') # Different color for presets if desired
            if os.path.exists(self.presets_dir):
                for d in os.listdir(self.presets_dir):
                    if os.path.isdir(os.path.join(self.presets_dir, d)):
                        self.item_list.insert(tk.END, d)

    def apply_selected(self):
        sel = self.item_list.curselection()
        if not sel:
            messagebox.showerror("Error", "No item selected.")
            return
        item_display_name = self.item_list.get(sel)
        
        if self.source_var.get() == 'Caches':
            # apply cache
            found = False
            for folder in (self.preinstalled_dir, self.own_dir):
                if os.path.exists(folder):
                    for fname in os.listdir(folder):
                        # Match based on the display name part
                        if fname.endswith(f"- {item_display_name}") and os.path.isfile(os.path.join(folder, fname)):
                            key = fname.split(' - ',1)[0]
                            try:
                                shutil.copy2(os.path.join(folder, fname), os.path.join(self.http_dir, key))
                                messagebox.showinfo("Success", f"Replaced '{key}' in HTTP folder with cache '{item_display_name}'.")
                                found = True
                                return # Exit after first match
                            except Exception as e:
                                messagebox.showerror("Error", f"Could not copy file: {e}")
                                return
            if not found:
                 messagebox.showerror("Error", f"Cache file for '{item_display_name}' not found.")

        else: # Presets
            preset_folder_path = os.path.join(self.presets_dir, item_display_name)
            if not os.path.isdir(preset_folder_path):
                messagebox.showerror("Error", f"Preset folder '{item_display_name}' not found.")
                return
            
            cnt = 0
            errors = []
            for f in os.listdir(preset_folder_path):
                if ' - ' in f: # Ensure it's a correctly named cache file
                    key = f.split(' - ',1)[0]
                    try:
                        shutil.copy2(os.path.join(preset_folder_path, f), os.path.join(self.http_dir, key))
                        cnt+=1
                    except Exception as e:
                        errors.append(f"Could not copy {f}: {e}")
                
            if errors:
                messagebox.showwarning("Partial Success", f"Applied {cnt} files from preset '{item_display_name}'.\nErrors:\n" + "\n".join(errors))
            elif cnt > 0:
                messagebox.showinfo("Success", f"Applied {cnt} files from preset '{item_display_name}'.")
            else:
                messagebox.showinfo("Info", f"No valid cache files found in preset '{item_display_name}'.")


    def create_cache(self):
        if self.source_var.get() != 'Caches':
            messagebox.showerror("Error", "Switch to Caches view to create a new cache.")
            return

        src_file_path = filedialog.askopenfilename(title="Select source file for cache")
        if not src_file_path:
            return

        dialog = tk.Toplevel(self)
        dialog.title("Create New Cache")
        dialog.geometry("400x350")
        dialog.configure(bg='#2e2e3d')
        dialog.transient(self)
        dialog.grab_set()

        # --- Hash Source Selection ---
        hash_source_var = tk.StringVar(value="dropdown")

        hash_choice_frame = ttk.Frame(dialog, padding=(10,5))
        hash_choice_frame.pack(fill='x')
        ttk.Label(hash_choice_frame, text="Hash Source:").pack(side='left', padx=(0,10))
        
        rb_dropdown = ttk.Radiobutton(hash_choice_frame, text="From Dropdown", variable=hash_source_var, value="dropdown")
        rb_dropdown.pack(side='left', padx=5)
        rb_custom = ttk.Radiobutton(hash_choice_frame, text="Custom Input", variable=hash_source_var, value="custom")
        rb_custom.pack(side='left', padx=5)

        # --- Function Dropdown ---
        func_frame = ttk.Frame(dialog, padding=(10,5))
        func_frame.pack(fill='x')
        func_label = ttk.Label(func_frame, text="Select Function (Hash):")
        func_label.pack(side='left', padx=(0,10))
        
        # Ensure self.functions has items, provide a default if not
        function_display_values = [d for _, d in self.functions] if self.functions else ["No functions defined"]
        
        combo_func = ttk.Combobox(func_frame, values=function_display_values, state='readonly', width=30)
        combo_func.pack(side='left', expand=True, fill='x')
        if self.functions: # Only set current if there are functions
            combo_func.current(0)
        elif not function_display_values: # No functions at all
            combo_func.config(state='disabled')


        # --- Custom Hash Input ---
        custom_hash_frame = ttk.Frame(dialog, padding=(10,5))
        custom_hash_frame.pack(fill='x')
        custom_hash_label = ttk.Label(custom_hash_frame, text="Enter Custom Hash:")
        custom_hash_label.pack(side='left', padx=(0,10))
        
        entry_custom_hash = ttk.Entry(custom_hash_frame, width=33) #ttk.Entry for styling
        entry_custom_hash.pack(side='left', expand=True, fill='x')

        # --- Display Name Input ---
        display_name_frame = ttk.Frame(dialog, padding=(10,5))
        display_name_frame.pack(fill='x')
        ttk.Label(display_name_frame, text="Enter Display Name:").pack(side='left', padx=(0,10))
        
        entry_display_name = ttk.Entry(display_name_frame, width=30) #ttk.Entry for styling
        entry_display_name.pack(side='left', expand=True, fill='x')
        entry_display_name.focus() # Focus on display name initially

        # --- Toggle input fields based on radio button ---
        def toggle_hash_input_fields():
            if hash_source_var.get() == "dropdown":
                combo_func.config(state='readonly' if self.functions else 'disabled')
                func_label.config(foreground='#c7c7d9') # Active color
                entry_custom_hash.config(state='disabled')
                custom_hash_label.config(foreground='#777777') # Dimmed color
            else: # custom
                combo_func.config(state='disabled')
                func_label.config(foreground='#777777') # Dimmed color
                entry_custom_hash.config(state='normal')
                custom_hash_label.config(foreground='#c7c7d9') # Active color
        
        rb_dropdown.config(command=toggle_hash_input_fields)
        rb_custom.config(command=toggle_hash_input_fields)
        toggle_hash_input_fields() # Initial call to set states

        # --- OK/Cancel Buttons ---
        def on_ok():
            display_name = entry_display_name.get().strip()
            final_hash = ""

            if not display_name:
                messagebox.showerror("Error", "Display name is required.", parent=dialog)
                return

            if hash_source_var.get() == "dropdown":
                if not self.functions:
                    messagebox.showerror("Error", "No functions defined in functions.json. Cannot select from dropdown.", parent=dialog)
                    return
                selected_function_display = combo_func.get()
                # Find the actual hash (key) from the display name
                final_hash = next((k for k, d in self.functions if d == selected_function_display), None)
                if not final_hash:
                    messagebox.showerror("Error", "Selected function is invalid or not found.", parent=dialog)
                    return
            else: # custom
                final_hash = entry_custom_hash.get().strip()
                if not final_hash:
                    messagebox.showerror("Error", "Custom hash is required when 'Custom Input' is selected.", parent=dialog)
                    return
                # Basic hash validation (e.g., 32 hex characters, or just non-empty)
                if not all(c in "0123456789abcdefABCDEF" for c in final_hash) or len(final_hash) != 32 : # Example for MD5
                     if not messagebox.askyesno("Warning", f"The custom hash '{final_hash}' does not look like a standard 32-character hex hash. Continue anyway?", parent=dialog):
                        return


            # Construct filename
            filename = f"{final_hash} - {display_name}"
            destination_path = os.path.join(self.own_dir, filename)

            if os.path.exists(destination_path):
                if not messagebox.askyesno("Confirm", f"Cache '{filename}' already exists. Overwrite?", parent=dialog):
                    return
            
            try:
                shutil.copy2(src_file_path, destination_path)
                messagebox.showinfo("Success", f"Created cache '{filename}' in 'Own' caches.", parent=self) # parent=self so it appears on main window
                self.refresh_view()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create cache: {e}", parent=dialog)

        btn_frame = ttk.Frame(dialog, padding=(10,10))
        btn_frame.pack(fill='x', side='bottom')
        
        ok_button = ttk.Button(btn_frame, text="OK", command=on_ok)
        ok_button.pack(side='right', padx=5)
        cancel_button = ttk.Button(btn_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side='right', padx=5)
        
        dialog.wait_window()


    def clear_http_folder(self):
        if messagebox.askyesno("Confirm","Are you sure you want to delete all files and folders inside the Roblox HTTP cache folder? This cannot be undone."):
            cnt_files = 0
            cnt_folders = 0
            errors = []
            for item in os.listdir(self.http_dir):
                item_path = os.path.join(self.http_dir, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                        cnt_files += 1
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        cnt_folders +=1
                except Exception as e:
                    errors.append(f"Could not delete {item_path}: {e}")
            
            if errors:
                messagebox.showwarning("Partial Clear", f"Cleared {cnt_files} files and {cnt_folders} folders.\nEncountered errors:\n" + "\n".join(errors))
            else:
                messagebox.showinfo("Done", f"Successfully cleared {cnt_files} files and {cnt_folders} folders from the HTTP cache.")


if __name__=='__main__':
    app = RobloxFileReplacer()
    app.mainloop()
