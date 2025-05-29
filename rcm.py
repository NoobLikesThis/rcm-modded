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
            # Fallback for old plain text format if JSON parsing fails
            try:
                with open(self.functions_file, 'r', encoding='utf-8-sig') as f: # Ensure correct encoding
                    lines = [l.strip() for l in f if l.strip()]
            except Exception:
                lines = [] # If file doesn't exist or is unreadable
                
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
            messagebox.showerror("Error", "No item selected.")
            return
        item_display_name = self.item_list.get(sel)
        
        if self.source_var.get() == 'Caches':
            found_file = False
            for folder_path in (self.preinstalled_dir, self.own_dir):
                if os.path.exists(folder_path):
                    for fname in os.listdir(folder_path):
                        if fname.endswith(f" - {item_display_name}") and os.path.isfile(os.path.join(folder_path, fname)):
                            key_hash = fname.split(' - ',1)[0]
                            src_path = os.path.join(folder_path, fname)
                            dest_path = os.path.join(self.http_dir, key_hash)
                            try:
                                shutil.copy2(src_path, dest_path)
                                messagebox.showinfo("Success", f"Replaced {key_hash} in HTTP folder.")
                                found_file = True
                                return # Exit after applying
                            except Exception as e:
                                messagebox.showerror("Error", f"Failed to apply cache: {e}")
                                return
            if not found_file:
                 messagebox.showerror("Error", f"Cache file for '{item_display_name}' not found.")

        else: # Apply preset
            preset_folder_path = os.path.join(self.presets_dir, item_display_name)
            if not os.path.isdir(preset_folder_path):
                messagebox.showerror("Error", f"Preset folder '{item_display_name}' not found.")
                return
            
            count = 0
            errors = []
            for fname in os.listdir(preset_folder_path):
                if ' - ' in fname: # Ensure it's a cache file format
                    key_hash = fname.split(' - ',1)[0]
                    src_path = os.path.join(preset_folder_path, fname)
                    dest_path = os.path.join(self.http_dir, key_hash)
                    try:
                        shutil.copy2(src_path, dest_path)
                        count += 1
                    except Exception as e:
                        errors.append(f"Failed to copy {fname}: {e}")
            
            if errors:
                messagebox.showwarning("Partial Success", f"Applied {count} files from preset '{item_display_name}'.\nErrors:\n" + "\n".join(errors))
            elif count > 0:
                messagebox.showinfo("Success", f"Applied {count} files from preset '{item_display_name}'.")
            else:
                messagebox.showinfo("Info", f"No files applied from preset '{item_display_name}'. It might be empty or files are not in correct format.")

    def create_cache(self):
        if self.source_var.get() != 'Caches':
            messagebox.showerror("Error", "Switch to Caches to create a cache.")
            return
        src_filepath = filedialog.askopenfilename(title="Select source file for cache")
        if not src_filepath:
            return

        dialog = tk.Toplevel(self)
        dialog.title("Create Cache")
        dialog.configure(bg='#212326')
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text="Select function or choose 'Custom Hash':").pack(padx=10, pady=(10,0))
        
        function_display_names = [d for _, d in self.functions]
        custom_hash_option_text = "Custom Hash..."
        combobox_values = function_display_names + [custom_hash_option_text]
        
        combo_fn_or_custom = ttk.Combobox(dialog, values=combobox_values, state='readonly', width=30)
        combo_fn_or_custom.pack(padx=10, pady=5)
        
        if self.functions:
            combo_fn_or_custom.current(0)
        elif combobox_values: # Should always be true due to custom_hash_option_text
            combo_fn_or_custom.set(custom_hash_option_text)

        custom_hash_label = ttk.Label(dialog, text="Enter Custom Hash:")
        custom_hash_entry = ttk.Entry(dialog, width=33)

        def toggle_custom_hash_ui(event=None):
            if combo_fn_or_custom.get() == custom_hash_option_text:
                custom_hash_label.pack(padx=10, pady=(5,0))
                custom_hash_entry.pack(padx=10, pady=2)
            else:
                custom_hash_label.pack_forget()
                custom_hash_entry.pack_forget()
        
        combo_fn_or_custom.bind("<<ComboboxSelected>>", toggle_custom_hash_ui)
        toggle_custom_hash_ui() # Set initial visibility

        ttk.Label(dialog, text="Enter display name (for your reference):").pack(padx=10, pady=(10,0))
        entry_display_name = ttk.Entry(dialog, width=33)
        entry_display_name.pack(padx=10, pady=5)

        def on_ok_create():
            selected_option = combo_fn_or_custom.get()
            cache_display_name = entry_display_name.get().strip()
            
            final_hash_key = None
            if selected_option == custom_hash_option_text:
                final_hash_key = custom_hash_entry.get().strip()
                if not final_hash_key:
                    messagebox.showerror("Error", "Custom hash cannot be empty when 'Custom Hash' is selected.", parent=dialog)
                    return
            else: # A pre-defined function was selected
                final_hash_key = next((k for k, d_text in self.functions if d_text == selected_option), None)

            if not final_hash_key: # Should not happen if logic is correct, but as a safeguard
                messagebox.showerror("Error", "Could not determine the hash/key.", parent=dialog)
                return
            if not cache_display_name:
                messagebox.showerror("Error", "Display name cannot be empty.", parent=dialog)
                return
            
            # It's good practice to destroy the dialog before showing a messagebox that isn't an error for this dialog
            # However, if shutil.copy2 fails, we want the dialog to persist for user to correct.
            # So, we'll destroy it only on full success.

            target_filename = f"{final_hash_key} - {cache_display_name}"
            target_path = os.path.join(self.own_dir, target_filename)

            if os.path.exists(target_path):
                if not messagebox.askyesno("Confirm Overwrite", f"Cache '{target_filename}' already exists. Overwrite?", parent=dialog):
                    return

            try:
                shutil.copy2(src_filepath, target_path)
                dialog.destroy() # Destroy on success
                self.refresh_view()
                messagebox.showinfo("Success", f"Created cache '{target_filename}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create cache: {e}", parent=dialog)
        
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=10)
        ttk.Button(buttons_frame, text="OK", command=on_ok_create).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)
        
        dialog.wait_window()


    def clear_http_folder(self):
        if messagebox.askyesno("Confirm","Are you sure you want to delete all files and folders within the Roblox HTTP cache folder?"):
            cleared_count = 0
            errors_count = 0
            if not os.path.exists(self.http_dir):
                messagebox.showinfo("Info", "HTTP cache folder does not exist. Nothing to clear.")
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
                    print(f"Error deleting {item_path}: {e}") # Log to console for debugging
                    errors_count +=1
            
            if errors_count > 0:
                messagebox.showwarning("Partial Clear", f"Cleared {cleared_count} items. Failed to clear {errors_count} items. Check console for details.")
            else:
                messagebox.showinfo("Done", f"Successfully cleared {cleared_count} items from the HTTP cache folder.")

if __name__=='__main__':
    app = RobloxFileReplacer()
    app.mainloop()
