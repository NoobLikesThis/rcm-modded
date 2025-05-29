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
            # This nested structure is from the original; if functions.json is missing,
            # this inner open will also fail.
            try:
                with open(self.functions_file, 'r', encoding='utf-8-sig') as f:
                    lines = [l.strip() for l in f if l.strip()]
            except Exception: # If all fails (e.g. file not found), lines remains empty or unassigned if not init above
                lines = [] # Ensure lines is defined as empty list
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
        item = self.item_list.get(sel)
        if self.source_var.get() == 'Caches':
            # apply cache
            # find file in caches
            for folder in (self.preinstalled_dir, self.own_dir):
                for fname in os.listdir(folder):
                    if fname.endswith(f"- {item}"):
                        key = fname.split(' - ',1)[0]
                        shutil.copy2(os.path.join(folder, fname), os.path.join(self.http_dir, key))
                        messagebox.showinfo("Success", f"Replaced {key} in HTTP folder.")
                        return
        else:
            # apply preset
            folder = os.path.join(self.presets_dir, item)
            cnt=0
            for f in os.listdir(folder):
                key = f.split(' - ',1)[0]
                shutil.copy2(os.path.join(folder, f), os.path.join(self.http_dir, key))
                cnt+=1
            messagebox.showinfo("Success", f"Applied {cnt} files from preset {item}.")

    def create_cache(self):
        if self.source_var.get() != 'Caches':
            messagebox.showerror("Error", "Switch to Caches to create a cache.")
            return
        src = filedialog.askopenfilename(title="Select source file for cache")
        if not src:
            return
        dialog = tk.Toplevel(self)
        dialog.configure(bg='#212326')
        ttk.Label(dialog, text="Select function:").pack(padx=10, pady=(10,0))
        
        combo_values = [d for _, d in self.functions]
        combo = ttk.Combobox(dialog, values=combo_values, state='readonly')
        combo.pack(padx=10, pady=5)
        # Original combo.current(0) behavior: if self.functions is empty, this line could error.
        # To preserve original behavior strictly, we call it. If functions are loaded, it's fine.
        if combo_values: # Only call current if there are values, to prevent TclError
            combo.current(0)
        
        # ---- START OF ADDED/MODIFIED CODE FOR CUSTOM HASH ----
        custom_hash_holder = [None] # Use a list to make it mutable in the inner function

        def ask_for_custom_hash_input():
            # parent=dialog makes simpledialog modal to this specific dialog
            chash = simpledialog.askstring("Custom Hash", "Enter custom hash value:", parent=dialog)
            if chash and chash.strip(): # If user entered non-whitespace string
                custom_hash_holder[0] = chash.strip()
                messagebox.showinfo("Info", f"Custom hash '{custom_hash_holder[0]}' will be used.", parent=dialog)
            elif chash is not None: # User entered an empty string or only whitespace
                 messagebox.showwarning("Warning", "Custom hash was empty. Dropdown selection will be used if available.", parent=dialog)
                 custom_hash_holder[0] = None # Ensure it's reset if invalid
            # If chash is None (user cancelled dialog), custom_hash_holder[0] remains unchanged.

        ttk.Button(dialog, text="Input Custom Hash", command=ask_for_custom_hash_input).pack(padx=10, pady=(0,5))
        # ---- END OF ADDED/MODIFIED CODE FOR CUSTOM HASH ----

        ttk.Label(dialog, text="Enter display name:").pack(padx=10, pady=(10,0)) # pady was (10,0)
        entry = ttk.Entry(dialog)
        entry.pack(padx=10, pady=5)

        def on_ok():
            # Get values from dialog widgets before it's destroyed
            selected_function_display_name = combo.get()
            display_name = entry.get().strip()
            
            # ---- START OF MODIFIED LOGIC IN on_ok ----
            final_hash_key = None
            if custom_hash_holder[0]: # Custom hash takes precedence
                final_hash_key = custom_hash_holder[0]
            else: # Fallback to dropdown if custom hash is not set
                final_hash_key = next((k for k, d in self.functions if d == selected_function_display_name), None)
            
            # Destroy dialog after getting all necessary values
            # This was originally on the same line as combo.get() and entry.get()
            dialog.destroy() 

            if not final_hash_key or not display_name:
                messagebox.showerror("Error","A valid hash (from dropdown or custom input) and a display name are required.")
                return
            
            name = f"{final_hash_key} - {display_name}"
            # ---- END OF MODIFIED LOGIC IN on_ok ----
            shutil.copy2(src, os.path.join(self.own_dir, name))
            self.refresh_view()
            messagebox.showinfo("Success", f"Created cache {name}.")

        btnf = ttk.Frame(dialog); btnf.pack(pady=10)
        ttk.Button(btnf, text="OK", command=on_ok).pack(side='left', padx=5)
        ttk.Button(btnf, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)
        dialog.transient(self); dialog.grab_set(); dialog.wait_window()


    def clear_http_folder(self):
        if messagebox.askyesno("Confirm","Delete all in HTTP folder?"):
            cnt=0
            for f in os.listdir(self.http_dir):
                p=os.path.join(self.http_dir,f)
                try: shutil.rmtree(p) if os.path.isdir(p) else os.unlink(p); cnt+=1
                except: pass
            messagebox.showinfo("Done", f"Cleared {cnt} items.")

if __name__=='__main__':
    RobloxFileReplacer().mainloop()
