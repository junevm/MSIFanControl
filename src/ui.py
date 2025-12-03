import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio
from .config_manager import ConfigManager
from .ec import read, write
from .fan_control import apply_fan_profile

class MSIFanControlApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.github.msifancontrol",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.config_manager = ConfigManager()
        self.min_max = [100, 0, 100, 0] # CPU_MIN, CPU_MAX, GPU_MIN, GPU_MAX

    def do_activate(self):
        window = MainWindow(self)
        window.present()

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.app = app
        self.config = app.config_manager
        self.set_title("MSI Fan Control")
        self.set_default_size(400, 300)

        # Main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        self.set_child(main_box)

        # Profile Selector
        profile_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        profile_label = Gtk.Label(label="Fan Profile:")
        profile_box.append(profile_label)

        self.profile_combo = Gtk.ComboBoxText()
        self.profile_combo.append_text("Auto")
        self.profile_combo.append_text("Basic")
        self.profile_combo.append_text("Advanced")
        self.profile_combo.append_text("Cooler Booster")
        
        # Set active based on config
        current_profile = self.config.get("PROFILE")
        if current_profile >= 1 and current_profile <= 4:
            self.profile_combo.set_active(current_profile - 1)
        
        self.profile_combo.connect("changed", self.on_profile_changed)
        profile_box.append(self.profile_combo)
        main_box.append(profile_box)

        # Stats Grid
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(20)
        main_box.append(grid)

        # Headers
        headers = ["", "CURRENT", "MIN", "MAX", "FAN RPM"]
        for i, header in enumerate(headers):
            label = Gtk.Label(label=header)
            label.add_css_class("header-label")
            grid.attach(label, i, 0, 1, 1)

        # CPU Row
        grid.attach(Gtk.Label(label="CPU"), 0, 1, 1, 1)
        self.cpu_curr = Gtk.Label(label="0")
        grid.attach(self.cpu_curr, 1, 1, 1, 1)
        self.cpu_min = Gtk.Label(label="0")
        grid.attach(self.cpu_min, 2, 1, 1, 1)
        self.cpu_max = Gtk.Label(label="0")
        grid.attach(self.cpu_max, 3, 1, 1, 1)
        self.cpu_rpm = Gtk.Label(label="0")
        grid.attach(self.cpu_rpm, 4, 1, 1, 1)

        # GPU Row
        grid.attach(Gtk.Label(label="GPU"), 0, 2, 1, 1)
        self.gpu_curr = Gtk.Label(label="0")
        grid.attach(self.gpu_curr, 1, 2, 1, 1)
        self.gpu_min = Gtk.Label(label="0")
        grid.attach(self.gpu_min, 2, 2, 1, 1)
        self.gpu_max = Gtk.Label(label="0")
        grid.attach(self.gpu_max, 3, 2, 1, 1)
        self.gpu_rpm = Gtk.Label(label="0")
        grid.attach(self.gpu_rpm, 4, 2, 1, 1)

        # Battery Threshold
        battery_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        battery_box.append(Gtk.Label(label="Battery Charge Limit (%):"))
        
        self.battery_combo = Gtk.ComboBoxText()
        for i in range(50, 101, 5):
            self.battery_combo.append_text(str(i))
        
        current_limit = self.config.get("BATTERY_THRESHOLD_VALUE")
        # Find index
        try:
            idx = (current_limit - 50) // 5
            self.battery_combo.set_active(idx)
        except:
            self.battery_combo.set_active(10) # 100%

        self.battery_combo.connect("changed", self.on_battery_changed)
        battery_box.append(self.battery_combo)
        main_box.append(battery_box)

        # Start update timer
        GLib.timeout_add(1000, self.update_stats)

        # Apply initial profile
        self.on_profile_changed(self.profile_combo)

    def on_profile_changed(self, combo):
        idx = combo.get_active()
        if idx == -1: return
        
        profile_id = idx + 1
        self.config.set("PROFILE", profile_id)
        apply_fan_profile(self.config)

    def on_battery_changed(self, combo):
        text = combo.get_active_text()
        if not text: return
        val = int(text)
        self.config.set("BATTERY_THRESHOLD_VALUE", val)
        # Write to EC
        # Original: write(0xe4, config.BATTERY_THRESHOLD_VALUE + 128)
        write(0xe4, val + 128)

    def update_stats(self):
        temp_addr = self.config.get("CPU_GPU_TEMP_ADDRESS")
        rpm_addr = self.config.get("CPU_GPU_RPM_ADDRESS")

        cpu_temp = read(temp_addr[0], 1, 0)
        gpu_temp = read(temp_addr[1], 1, 0)

        # Update Min/Max
        if self.app.min_max[0] > cpu_temp: self.app.min_max[0] = cpu_temp
        if self.app.min_max[1] < cpu_temp: self.app.min_max[1] = cpu_temp
        if self.app.min_max[2] > gpu_temp: self.app.min_max[2] = gpu_temp
        if self.app.min_max[3] < gpu_temp: self.app.min_max[3] = gpu_temp

        # RPM
        try:
            cpu_rpm_raw = read(rpm_addr[0], 2, 0)
            cpu_rpm = 478000 // cpu_rpm_raw if cpu_rpm_raw > 0 else 0
        except: cpu_rpm = 0

        try:
            gpu_rpm_raw = read(rpm_addr[1], 2, 0)
            gpu_rpm = 478000 // gpu_rpm_raw if gpu_rpm_raw > 0 else 0
        except: gpu_rpm = 0

        self.cpu_curr.set_text(str(cpu_temp))
        self.cpu_min.set_text(str(self.app.min_max[0]))
        self.cpu_max.set_text(str(self.app.min_max[1]))
        self.cpu_rpm.set_text(str(cpu_rpm))

        self.gpu_curr.set_text(str(gpu_temp))
        self.gpu_min.set_text(str(self.app.min_max[2]))
        self.gpu_max.set_text(str(self.app.min_max[3]))
        self.gpu_rpm.set_text(str(gpu_rpm))

        return True
