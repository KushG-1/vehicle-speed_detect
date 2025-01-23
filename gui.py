import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2


class SpeedDetectionGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Speed Detection System")
        self.video_source = tk.StringVar(value="Webcam")
        self.video_path = None
        self.real_world_distance = 10  # Default: 10 meters
        self.frame_rate = 30  # Default: 30 FPS
        self.speed_limit = 60  # Default: 60 km/h
        self.setup_gui_components()

    def setup_gui_components(self):
        """Setup all GUI components."""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Video Display
        video_frame = ttk.LabelFrame(main_frame, text="Video Feed", padding=10)
        video_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.video_label = ttk.Label(video_frame, text="Video will appear here")
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # Controls
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Input Source Selection
        ttk.Label(controls_frame, text="Select Video Source:").pack(pady=5)
        source_dropdown = ttk.Combobox(controls_frame, textvariable=self.video_source, state="readonly")
        source_dropdown["values"] = ["Webcam", "Pre-Recorded Video"]
        source_dropdown.pack(pady=5)
        source_dropdown.bind("<<ComboboxSelected>>", self.on_source_change)

        # Open File Button
        self.open_file_button = ttk.Button(
            controls_frame, text="Open Video File", command=self.select_video_file, state=tk.DISABLED
        )
        self.open_file_button.pack(pady=5)

        # Settings
        self.settings_button = ttk.Button(controls_frame, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=5)

        # Start/Stop Buttons
        self.start_button = ttk.Button(controls_frame, text="Start Detection", command=None)
        self.start_button.pack(pady=5)
        self.stop_button = ttk.Button(controls_frame, text="Stop Detection", command=None)
        self.stop_button.pack(pady=5)

        # Status and Logs
        status_frame = ttk.LabelFrame(main_frame, text="Status and Logs", padding=10)
        status_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.status_label = ttk.Label(status_frame, text="Status: Stopped")
        self.status_label.pack(anchor="w")
        self.log_box = tk.Text(status_frame, height=10, width=80)
        self.log_box.pack()

    def on_source_change(self, event=None):
        if self.video_source.get() == "Pre-Recorded Video":
            self.open_file_button.config(state=tk.NORMAL)
        else:
            self.open_file_button.config(state=tk.DISABLED)
            self.video_path = None

    def select_video_file(self):
        self.video_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=(("MP4 Files", "*.mp4"), ("All Files", "*.*"))
        )
        if self.video_path:
            self.log_box.insert(tk.END, f"Selected Video: {self.video_path}\n")
            self.log_box.see(tk.END)

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")

        # Real-world Distance
        ttk.Label(settings_window, text="Real-World Distance (meters):").pack(pady=5)
        distance_entry = ttk.Entry(settings_window)
        distance_entry.insert(0, str(self.real_world_distance))
        distance_entry.pack(pady=5)

        # Frame Rate
        ttk.Label(settings_window, text="Frame Rate (FPS):").pack(pady=5)
        fps_entry = ttk.Entry(settings_window)
        fps_entry.insert(0, str(self.frame_rate))
        fps_entry.pack(pady=5)

        # Speed Limit
        ttk.Label(settings_window, text="Speed Limit (km/h):").pack(pady=5)
        speed_limit_entry = ttk.Entry(settings_window)
        speed_limit_entry.insert(0, str(self.speed_limit))
        speed_limit_entry.pack(pady=5)

        def save_settings():
            try:
                self.real_world_distance = float(distance_entry.get())
                self.frame_rate = int(fps_entry.get())
                self.speed_limit = int(speed_limit_entry.get())
                self.status_label.config(text=f"Settings Saved: {self.real_world_distance}m, {self.frame_rate}FPS, {self.speed_limit}km/h")
                settings_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")

        ttk.Button(settings_window, text="Save", command=save_settings).pack(pady=10)

    def update_image(self, frame):
        """Display video frame in the GUI."""
        if frame is not None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            img_tk = ImageTk.PhotoImage(image=img)
            self.video_label.img_tk = img_tk
            self.video_label.configure(image=img_tk)

    def update_status(self, status_text):
        """Update the status label."""
        self.status_label.config(text=f"Status: {status_text}")

    def set_start_command(self, command):
        self.start_button.config(command=command)

    def set_stop_command(self, command):
        self.stop_button.config(command=command)

    def get_video_source(self):
        """Return the video source (Webcam or Pre-Recorded Video path)."""
        return self.video_path if self.video_path else "Webcam"

    def run(self):
        self.root.mainloop()
