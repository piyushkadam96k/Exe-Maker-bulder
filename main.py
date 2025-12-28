import customtkinter as ctk
import tkinter as tk
import webbrowser

from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import sys
import datetime
import json

from PIL import Image

# Set theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ExeMakerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Kadam Exe Maker Pro")
        self.geometry("1000x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Set App Icon
        icon_file = os.path.abspath("app_icon.ico")
        if os.path.exists(icon_file):
            self.iconbitmap(icon_file)

        # Variables
        self.script_path = tk.StringVar()
        self.app_name = tk.StringVar()
        
        # Default to app_icon.ico if it exists
        default_icon = icon_file if os.path.exists(icon_file) else ""
        self.icon_path = tk.StringVar(value=default_icon)
        
        self.splash_path = tk.StringVar()
        self.asset_folder = tk.StringVar()
        self.hidden_imports = tk.StringVar()
        self.version_str = tk.StringVar() # e.g. 1.0.0.0
        
        self.one_file_var = tk.BooleanVar(value=True)
        self.no_console_var = tk.BooleanVar(value=False)

        self.create_widgets()

    def open_github(self):
        webbrowser.open("https://github.com/piyushkadam96k")

    def create_widgets(self):
        # --- Main Container ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # 1. Header & Toolbar
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.header_frame, text="Kadam Exe Maker", font=("Segoe UI", 28, "bold", "italic"), text_color="#3B8ED0").grid(row=0, column=0, sticky="w")
        
        # Toolbar Buttons
        self.load_btn = ctk.CTkButton(self.header_frame, text="Load Config", width=100, fg_color="#444", command=self.load_config)
        self.load_btn.grid(row=0, column=1, padx=10)
        self.save_btn = ctk.CTkButton(self.header_frame, text="Save Config", width=100, fg_color="#444", command=self.save_config)
        self.save_btn.grid(row=0, column=2, padx=(0, 10))

        self.github_btn = ctk.CTkButton(self.header_frame, text="GitHub", width=80, fg_color="#333", command=self.open_github)
        self.github_btn.grid(row=0, column=3)

        # 2. Input Section (Card)
        self.input_card = ctk.CTkFrame(self.main_frame)
        self.input_card.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.input_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.input_card, text="Python Script", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(10, 5))
        self.script_entry = ctk.CTkEntry(self.input_card, textvariable=self.script_path, placeholder_text="Select your .py file...", height=35)
        self.script_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(15, 5), pady=(0, 15))
        ctk.CTkButton(self.input_card, text="Browse", width=100, height=35, command=self.browse_script).grid(row=1, column=2, sticky="e", padx=(5, 15), pady=(0, 15))


        # 3. Settings Card
        self.settings_card = ctk.CTkFrame(self.main_frame)
        self.settings_card.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        self.settings_card.grid_columnconfigure((1, 3), weight=1) 

        ctk.CTkLabel(self.settings_card, text="Build Configuration", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(10, 5))

        # Row 1: App Name & Version
        ctk.CTkLabel(self.settings_card, text="App Name:").grid(row=1, column=0, sticky="w", padx=(15, 5), pady=5)
        ctk.CTkEntry(self.settings_card, textvariable=self.app_name, placeholder_text="Name (Optional)").grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        ctk.CTkLabel(self.settings_card, text="Version:").grid(row=1, column=2, sticky="w", padx=(15, 5), pady=5)
        ctk.CTkEntry(self.settings_card, textvariable=self.version_str, placeholder_text="e.g. 1.0.0.0").grid(row=1, column=3, columnspan=2, sticky="ew", padx=(5, 15), pady=5)

        # Row 2: Icon & Splash
        ctk.CTkLabel(self.settings_card, text="Icon (.ico):").grid(row=2, column=0, sticky="w", padx=(15, 5), pady=5)
        ctk.CTkEntry(self.settings_card, textvariable=self.icon_path).grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ctk.CTkButton(self.settings_card, text="Find", width=50, command=self.browse_icon, fg_color="#555").grid(row=2, column=2, padx=(5, 5), pady=5)

        ctk.CTkLabel(self.settings_card, text="Splash Img:").grid(row=2, column=3, sticky="w", padx=(15, 5), pady=5)
        ctk.CTkEntry(self.settings_card, textvariable=self.splash_path, placeholder_text="Image file").grid(row=2, column=4, sticky="ew", padx=5, pady=5)
        ctk.CTkButton(self.settings_card, text="Find", width=50, command=self.browse_splash, fg_color="#555").grid(row=2, column=5, padx=(5, 15), pady=5)

        # Row 3: Include Folder
        ctk.CTkLabel(self.settings_card, text="Add Folder:").grid(row=3, column=0, sticky="w", padx=(15, 5), pady=5)
        self.asset_entry = ctk.CTkEntry(self.settings_card, textvariable=self.asset_folder, placeholder_text="Entire folder bundling")
        self.asset_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        ctk.CTkButton(self.settings_card, text="Find", width=50, command=self.browse_asset_folder, fg_color="#555").grid(row=3, column=2, padx=(5, 5), pady=5)
        ctk.CTkLabel(self.settings_card, text="(Auto-creates unique build folder)", font=("Segoe UI", 10), text_color="gray").grid(row=3, column=3, columnspan=3, sticky="w", padx=5)

        # Row 4: Hidden Imports
        ctk.CTkLabel(self.settings_card, text="Hidden Imports:").grid(row=4, column=0, sticky="w", padx=(15, 5), pady=(5, 15))
        ctk.CTkEntry(self.settings_card, textvariable=self.hidden_imports, placeholder_text="module1, module2...").grid(row=4, column=1, columnspan=5, sticky="ew", padx=(5, 15), pady=(5, 15))

        # Row 5: Switches
        self.check_frame = ctk.CTkFrame(self.settings_card, fg_color="transparent")
        self.check_frame.grid(row=5, column=0, columnspan=6, sticky="ew", padx=15, pady=(0, 15))
        
        self.onefile_sw = ctk.CTkSwitch(self.check_frame, text="One File", variable=self.one_file_var)
        self.onefile_sw.pack(side="left", padx=(0, 20))
        self.noconsole_sw = ctk.CTkSwitch(self.check_frame, text="No Console (GUI Only)", variable=self.no_console_var)
        self.noconsole_sw.pack(side="left")

        # 4. Action Section
        self.convert_btn = ctk.CTkButton(self.main_frame, text="BUILD PRO EXECUTABLE", font=("Segoe UI", 16, "bold"), height=50, fg_color="#10B981", hover_color="#059669", command=self.start_conversion)
        self.convert_btn.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, height=10, mode="indeterminate")
        self.progress_bar.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        self.progress_bar.set(0)

        # 5. Logs
        ctk.CTkLabel(self.main_frame, text="Build Output:", font=("Consolas", 12, "bold")).grid(row=6, column=0, sticky="w", padx=5, pady=(10, 0))
        self.log_box = ctk.CTkTextbox(self.main_frame, font=("Consolas", 11), fg_color="#1E1E1E", text_color="#D4D4D4", activate_scrollbars=True)
        self.log_box.grid(row=7, column=0, sticky="nsew", pady=(5, 0))
        self.log_box.configure(state="disabled")

    # --- Browsing ---
    def browse_script(self):
        path = filedialog.askopenfilename(filetypes=[("Python Scripts", "*.py")])
        if path:
            self.script_path.set(path)
            if not self.app_name.get():
                self.app_name.set(os.path.splitext(os.path.basename(path))[0])

    def browse_icon(self):
        # Allow images as well
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.ico;*.png;*.jpg;*.jpeg;*.webp")])
        if path: self.icon_path.set(path)

    def browse_splash(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if path: self.splash_path.set(path)

    def browse_asset_folder(self):
        path = filedialog.askdirectory()
        if path: self.asset_folder.set(path)

    # --- Config ---
    def save_config(self):
        data = {
            "app_name": self.app_name.get(),
            "icon_path": self.icon_path.get(),
            "splash_path": self.splash_path.get(),
            "asset_folder": self.asset_folder.get(),
            "hidden_imports": self.hidden_imports.get(),
            "version": self.version_str.get(),
            "one_file": self.one_file_var.get(),
            "no_console": self.no_console_var.get()
        }
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Config", "*.json")])
        if f:
            with open(f, "w") as file:
                json.dump(data, file)
            messagebox.showinfo("Saved", "Configuration saved!")

    def load_config(self):
        f = filedialog.askopenfilename(filetypes=[("JSON Config", "*.json")])
        if f:
            try:
                with open(f, "r") as file:
                    data = json.load(file)
                self.app_name.set(data.get("app_name", ""))
                self.icon_path.set(data.get("icon_path", ""))
                self.splash_path.set(data.get("splash_path", ""))
                self.asset_folder.set(data.get("asset_folder", ""))
                self.hidden_imports.set(data.get("hidden_imports", ""))
                self.version_str.set(data.get("version", ""))
                self.one_file_var.set(data.get("one_file", True))
                self.no_console_var.set(data.get("no_console", False))
                messagebox.showinfo("Loaded", "Configuration loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {e}")

    # --- Build Logic ---
    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def start_conversion(self):
        script = self.script_path.get()
        if not script or not os.path.exists(script):
            messagebox.showerror("Error", "Please select a valid Python script.")
            return

        self.convert_btn.configure(state="disabled", text="Building...")
        self.progress_bar.start()
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0", "end")
        self.log_box.configure(state="disabled")

        # Command Construction
        cmd = ["pyinstaller", "--noconfirm", "--clean"]

        # 1. Output Folder Logic (Unified)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        name_clean = self.app_name.get().strip() or "MyApp"
        
        # Parent "Kadam_Builds" folder next to script
        base_dir = os.path.dirname(script)
        builds_dir = os.path.join(base_dir, "Kadam_Builds")
        
        # Specific folder for this build: Kadam_Builds/MyApp_Timestamp/
        unified_output_dir = os.path.join(builds_dir, f"{name_clean}_{timestamp}")
        
        # Temp folder for build artifacts: Kadam_Builds/MyApp_Timestamp/temp
        temp_dir = os.path.join(unified_output_dir, "temp")
        
        # Ensure directories exist (PyInstaller usually creates them, but good to be safe)
        os.makedirs(unified_output_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        
        # Configure PyInstaller paths
        cmd.extend(["--distpath", unified_output_dir])  # EXE goes here
        cmd.extend(["--workpath", temp_dir])             # Temp build files go here
        cmd.extend(["--specpath", unified_output_dir])   # Spec file goes here

        # 2. Basic Options
        if name_clean: cmd.extend(["--name", name_clean])
        if self.one_file_var.get(): cmd.append("--onefile")
        if self.no_console_var.get(): cmd.append("--noconsole")

        # 3. Assets/Icon
        user_icon = self.icon_path.get()
        if user_icon:
            icon_to_use = user_icon
            # Auto-convert if not .ico
            if not user_icon.lower().endswith(".ico"):
                try:
                    self.log(f"Auto-converting icon: {os.path.basename(user_icon)} -> .ico")
                    img = Image.open(user_icon)
                    temp_ico_path = os.path.join(temp_dir, "converted_icon.ico")
                    img.save(temp_ico_path, format="ICO", sizes=[(256, 256)])
                    icon_to_use = temp_ico_path
                except Exception as e:
                    self.log(f"WARNING: Icon conversion failed: {e}")
                    # Fallback to original, though pyinstaller might error if it's not ico
                    icon_to_use = user_icon
            
            cmd.extend(["--icon", icon_to_use])

        if self.splash_path.get(): cmd.extend(["--splash", self.splash_path.get()])
        
        if self.asset_folder.get():
            folder_path = self.asset_folder.get().replace("/", os.sep)
            folder_name = os.path.basename(folder_path)
            cmd.extend(["--add-data", f"{folder_path};{folder_name}"])

        if self.hidden_imports.get():
            for imp in self.hidden_imports.get().split(","):
                if imp.strip(): cmd.extend(["--hidden-import", imp.strip()])

        # 4. Version (Basic file generation)
        if self.version_str.get():
            # Creating a minimal version file is complex programmatically without a template.
            # passing generic --version-file might require a valid file struct.
            # For robustness, we will skip file generation in this MVP unless requested strictly, 
            # as malformed version files break builds.
            # We log that we are skipping it for safety in this version.
            self.log("INFO: Version string received. (Note: Full file versioning requires a resource structure, skipping for stability).")

        cmd.append(script)
        
        # Run
        threading.Thread(target=self.run_pyinstaller, args=(cmd, unified_output_dir), daemon=True).start()

    def run_pyinstaller(self, cmd, dist_path):
        self.log(f"Output Directory: {dist_path}")
        self.log(f"Command: {' '.join(cmd)}\n")
        self.log("-" * 60)
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            for line in process.stdout:
                self.after(0, self.log, line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.after(0, lambda: self.conversion_success(dist_path))
            else:
                self.after(0, self.conversion_failed)
        except Exception as e:
             self.after(0, self.log, f"ERROR: {str(e)}")
             self.after(0, self.conversion_failed)

    def conversion_success(self, dist_path):
        self.progress_bar.stop()
        self.progress_bar.set(1)
        self.log("-" * 60)
        self.log(f"SUCCESS! Built in: {dist_path}")
        self.convert_btn.configure(state="normal", text="BUILD PRO EXECUTABLE")
        messagebox.showinfo("Success", f"Build Complete!\nFolder: {os.path.basename(dist_path)}")
        os.startfile(dist_path)

    def conversion_failed(self):
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.log("-" * 60)
        self.log("FAILED. Check logs.")
        self.convert_btn.configure(state="normal", text="BUILD PRO EXECUTABLE")
        messagebox.showerror("Error", "Build Failed.")

if __name__ == "__main__":
    app = ExeMakerApp()
    app.mainloop()
