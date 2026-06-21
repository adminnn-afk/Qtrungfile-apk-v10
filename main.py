# ============================================
# PANEL AIM PRO – ANDROID (ĐÃ SỬA LỖI)
# ============================================
import os, sys, time, threading, math, random, json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

Window.softinput_mode = "below_target"

CFG = {
    "aim_speed": 2.5, "fov": 150, "smooth": 0.2,
    "recoil": 1.5, "color": "#FF00FF", "tol": 30,
    "auto_shoot": True, "shoot_delay": 0.1, "aim_key": "volume_down"
}
running = False
aim_active = False

class AimEngine:
    def __init__(self):
        self.cfg = CFG.copy()
    def start(self):
        global running, aim_active
        running = True
        aim_active = True
    def stop(self):
        global running, aim_active
        running = False
        aim_active = False

engine = AimEngine()

class HeadshotUI(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=8, spacing=5)
        root.canvas.before.add(Color(*get_color_from_hex('#0d1117')))
        root.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

        hdr = BoxLayout(size_hint_y=0.08)
        hdr.add_widget(Label(text="[b]PANEL AIM[/b]", markup=True, font_size='20sp', color=(0.91,0.27,0.38,1)))
        self.btn_toggle = Button(text="BẮT ĐẦU", size_hint_x=0.3, background_color=(0.06,0.2,0.38,1))
        self.btn_toggle.bind(on_press=self.toggle_engine)
        hdr.add_widget(self.btn_toggle)
        root.add_widget(hdr)

        self.lbl_status = Label(text="● DỪNG", color=(1,0.2,0.2,1), size_hint_y=0.05)
        root.add_widget(self.lbl_status)

        tabs = TabbedPanel(do_default_tab=False, tab_width=100)
        tab_aim = TabbedPanelItem(text='AIM')
        scr = ScrollView()
        grid = GridLayout(cols=2, spacing=8, padding=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        def add_slider(label, key, minv, maxv, default, step=0.1):
            grid.add_widget(Label(text=label, size_hint_y=None, height=30, color=(0.9,0.9,0.9,1)))
            s = Slider(min=minv, max=maxv, value=default, step=step, size_hint_y=None, height=40)
            s.bind(value=lambda i, v, k=key: self.update_cfg(k, v))
            grid.add_widget(s)

        add_slider("Tốc độ", "aim_speed", 0.5, 5, 2.5)
        add_slider("FOV", "fov", 30, 300, 150, 10)
        add_slider("Độ mượt", "smooth", 0.05, 1, 0.2)
        add_slider("Giảm rung", "recoil", 0.5, 4, 1.5)
        add_slider("Dung sai", "tol", 5, 100, 30, 5)
        add_slider("Trễ bắn", "shoot_delay", 0.01, 0.5, 0.1, 0.01)

        grid.add_widget(Label(text="Màu (HEX)", size_hint_y=None, height=30))
        self.txt_color = TextInput(text="#FF00FF", multiline=False, size_hint_y=None, height=40)
        self.txt_color.bind(text=lambda i, v: self.update_cfg("color", v))
        grid.add_widget(self.txt_color)

        grid.add_widget(Label(text="Auto bắn"))
        self.sw_auto = Switch(active=True)
        self.sw_auto.bind(active=lambda i, v: self.update_cfg("auto_shoot", v))
        grid.add_widget(self.sw_auto)

        scr.add_widget(grid)
        tab_aim.content = scr
        tabs.add_widget(tab_aim)

        tab_keys = TabbedPanelItem(text='PHÍM')
        box = BoxLayout(orientation='vertical', padding=10, spacing=5)
        box.add_widget(Label(text="Phím kích hoạt aim:"))
        self.txt_key = TextInput(text="volume_down", multiline=False, size_hint_y=None, height=40)
        self.txt_key.bind(text=lambda i, v: self.update_cfg("aim_key", v))
        box.add_widget(self.txt_key)
        tab_keys.content = box
        tabs.add_widget(tab_keys)

        root.add_widget(tabs)
        self.add_widget(root)

    def update_cfg(self, key, value):
        if key in ["aim_speed","smooth","recoil","shoot_delay"]:
            engine.cfg[key] = float(value)
        elif key in ["fov","tol"]:
            engine.cfg[key] = int(float(value))
        elif key == "auto_shoot":
            engine.cfg[key] = bool(value)
        else:
            engine.cfg[key] = value

    def toggle_engine(self, instance):
        if not running:
            engine.start()
            self.lbl_status.text = "● ĐANG CHẠY"
            self.lbl_status.color = (0,1,0,1)
            self.btn_toggle.text = "DỪNG"
        else:
            engine.stop()
            self.lbl_status.text = "● DỪNG"
            self.lbl_status.color = (1,0.2,0.2,1)
            self.btn_toggle.text = "BẮT ĐẦU"

class PanelApp(App):
    def build(self):
        return HeadshotUI()

if __name__ == '__main__':
    PanelApp().run()
