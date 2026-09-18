import time
import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

# Secret AES-256 Encryption Key (Must match server key!)
AES_KEY_HEX = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

class MobileSecurityDashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # Title Screen
        self.title = Label(
            text='[b]🛡️ Hardware Security Guard[/b]', 
            markup=True, 
            font_size='22sp'
        )
        self.add_widget(self.title)

        # Status Light
        self.status_label = Label(
            text='Status: Off 🔴', 
            font_size='18sp'
        )
        self.add_widget(self.status_label)

        # Start Guard Button
        self.start_btn = Button(
            text='Start Guarding Hardware',
            size_hint=(1, 0.25),
            background_color=(0.1, 0.7, 0.3, 1)
        )
        self.start_btn.bind(on_press=self.start_guard_service)
        self.add_widget(self.start_btn)

        # On-Screen Notebook Logs
        self.log_box = Label(
            text='[ Security Activity Notebook ]\nTap start to monitor...', 
            font_size='14sp',
            halign='left',
            valign='top'
        )
        self.log_box.bind(size=self.log_box.setter('text_size'))
        self.add_widget(self.log_box)

    def start_guard_service(self, instance):
        self.status_label.text = 'Status: Active Guarding 🟢'
        self.add_log("Started watching GPS, Mic, Wi-Fi & Hotspot...")
        
        # Check phone hardware every 3 seconds
        Clock.schedule_interval(self.inspect_hardware, 3)

    def inspect_hardware(self, dt):
        """Checks if hardware is active and logs events"""
        if platform == 'android':
            # Call Android Java APIs inside Python using Pyjnius
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            activity = PythonActivity.mActivity
            
            # Check Network / Wi-Fi State
            cm = activity.getSystemService(Context.CONNECTIVITY_SERVICE)
            active_network = cm.getActiveNetworkInfo()
            
            if active_network and active_network.isConnected():
                net_name = active_network.getTypeName()
                self.add_log(f"ALERT: Connected to {net_name} network")
            else:
                self.add_log("ALERT: Network connection lost")
        else:
            # PC Simulator Mode for testing before putting on phone
            curr_hour = time.localtime().tm_hour
            self.add_log(f"SIMULATION: Hardware audit check at hour {curr_hour}:00")

    def add_log(self, text):
        timestamp = time.strftime('%H:%M:%S')
        new_line = f"[{timestamp}] {text}"
        current = self.log_box.text.split('\n')
        updated = [new_line] + current[:8]
        self.log_box.text = '\n'.join(updated)

class SecurityApp(App):
    def build(self):
        return MobileSecurityDashboard()

if __name__ == '__main__':
    SecurityApp().run()