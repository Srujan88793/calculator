import tkinter as tk
from tkinter import simpledialog, messagebox
from tkcalendar import Calendar # type: ignore
import datetime
class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Calendar with Reminders")
        self.root.geometry("400x350")
        self.create_widgets()
    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, padx=10, pady=10, bg="#f7f7f7")
        self.main_frame.pack(fill="both", expand=True)
        self.header_frame = tk.Frame(self.main_frame, bg="#f7f7f7")
        self.header_frame.pack(pady=10)
        self.cal = Calendar(self.main_frame, selectmode='day', year=datetime.datetime.now().year, 
         month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.cal.pack(pady=20)
        self.button_frame = tk.Frame(self.main_frame, bg="#f7f7f7")
        self.button_frame.pack(pady=10)
        self.reminder_button = tk.Button(self.button_frame, text="Set Reminder", command=self.set_reminder, bg="#2196F3", fg="white", font=("Arial", 12))
        self.reminder_button.pack(side="left", padx=5)
        self.show_reminder_button = tk.Button(self.button_frame, text="Show Reminders", command=self.show_reminders, bg="#FF5722", fg="white", font=("Arial", 12))
        self.show_reminder_button.pack(side="left", padx=5)
        self.reminders = {}
    def set_reminder(self):
        date = self.cal.selection_get()
        reminder_text = simpledialog.askstring("Input", f"Enter reminder for {date}:")
        if reminder_text:
            if date in self.reminders:
                self.reminders[date].append(reminder_text)
            else:
                self.reminders[date] = [reminder_text]
            messagebox.showinfo("Success", f"Reminder set for {date}")
    def show_reminders(self):
        date = self.cal.selection_get()
        if date in self.reminders:
            reminders = "\n".join(self.reminders[date])
            messagebox.showinfo(f"Reminders for {date}", reminders)
        else:
            messagebox.showinfo("No Reminders", f"No reminders set for {date}")
if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()