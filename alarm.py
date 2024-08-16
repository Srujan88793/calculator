import tkinter as tk
from tkinter import filedialog, messagebox
import time
import threading
import pygame
from datetime import datetime
class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.alarm_time = tk.StringVar()
        self.am_pm = tk.StringVar(value="AM")
        self.alarm_tone = tk.StringVar(value="No tone selected")
        self.snooze_duration = tk.StringVar(value="5")  
        self.create_widgets()
        self.alarm_thread = None
        self.is_alarm_running = False
        self.stop_requested = threading.Event()  
        pygame.mixer.init()
    def create_widgets(self):
        time_frame = tk.Frame(self.root)
        time_frame.pack(pady=10)
        tk.Label(time_frame, text="Set Alarm Time (HH:MM)").pack(side="left", padx=5)
        self.time_entry = tk.Entry(time_frame, textvariable=self.alarm_time, width=10)
        self.time_entry.pack(side="left", padx=5)
        am_pm_menu = tk.OptionMenu(time_frame, self.am_pm, "AM", "PM")
        am_pm_menu.pack(side="left", padx=5)
        tk.Label(self.root, text="Select Alarm Tone").pack(pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_tone).pack(pady=5)
        tk.Label(self.root, textvariable=self.alarm_tone).pack(pady=5)
        tk.Label(self.root, text="Snooze Duration (minutes)").pack(pady=10)
        snooze_options = [str(i) for i in range(5, 65, 5)]  
        snooze_menu = tk.OptionMenu(self.root, self.snooze_duration, *snooze_options)
        snooze_menu.pack(pady=5)
        tk.Button(self.root, text="Set Alarm", command=self.set_alarm).pack(pady=20)
        tk.Button(self.root, text="Stop Alarm", command=self.stop_alarm).pack(pady=5)
    def browse_tone(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.alarm_tone.set(file_path)
    def set_alarm(self):
        alarm_time_str = self.alarm_time.get()
        am_pm = self.am_pm.get() 
        try:    
            alarm_time_str = f"{alarm_time_str} {am_pm}"
            self.alarm_time_obj = datetime.strptime(alarm_time_str, "%I:%M %p").time()
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter time in HH:MM format")
            return
        if not self.alarm_tone.get() or self.alarm_tone.get() == "No tone selected":
            messagebox.showerror("No Tone Selected", "Please select an alarm tone")
            return
        self.is_alarm_running = True
        self.stop_requested.clear()  
        if self.alarm_thread is None or not self.alarm_thread.is_alive():
            self.alarm_thread = threading.Thread(target=self.check_alarm)
            self.alarm_thread.start()
        messagebox.showinfo("Alarm Set", f"Alarm set for {self.alarm_time_obj.strftime('%I:%M %p')}")
    def check_alarm(self):
        while self.is_alarm_running and not self.stop_requested.is_set():
            current_time = datetime.now().time()
            if (current_time.hour == self.alarm_time_obj.hour and
                current_time.minute == self.alarm_time_obj.minute):
                self.root.after(0, self.play_alarm)  
                break  
            time.sleep(1)  
    def play_alarm(self):
        try:
            pygame.mixer.music.load(self.alarm_tone.get())
            pygame.mixer.music.play(-1) 
        except pygame.error as e:
            messagebox.showerror("Playback Error", f"Failed to play alarm tone: {e}")
        self.show_alarm_dialog()
    def show_alarm_dialog(self):
        response = messagebox.askquestion("Alarm", "Alarm ringing! Snooze?", icon='warning')
        if response == 'yes':
            self.snooze_alarm()
        else:
            self.stop_alarm()
    def snooze_alarm(self):
        snooze_duration = int(self.snooze_duration.get())
        pygame.mixer.music.stop()
        snooze_time = time.time() + snooze_duration * 60
        while time.time() < snooze_time and self.is_alarm_running and not self.stop_requested.is_set():
            time.sleep(1)
        if self.is_alarm_running and not self.stop_requested.is_set():
            self.root.after(0, self.play_alarm)  
    def stop_alarm(self):
        self.stop_requested.set()  
        self.is_alarm_running = False
        pygame.mixer.music.stop() 
        if self.alarm_thread:
            self.alarm_thread.join()
        self.alarm_time.set("")
        self.am_pm.set("AM")
        self.snooze_duration.set("5")
        self.alarm_tone.set("No tone selected") 
        self.root.update_idletasks()
if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()