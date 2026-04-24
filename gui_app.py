import tkinter as tk
from tkinter import messagebox
import hashlib
import main  # Your existing logging logic
import config

class SmartLockerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Locker Secure Access")
        self.root.geometry("300x400")
        self.pin_display = ""

        # UI Elements
        self.label = tk.Label(root, text="Enter PIN", font=("Arial", 14))
        self.label.pack(pady=20)

        self.display = tk.Entry(root, show="*", justify='center', font=("Arial", 18))
        self.display.pack(pady=10)

        # Keypad Grid
        buttons_frame = tk.Frame(root)
        buttons_frame.pack()

        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            'C', '0', '✓'
        ]

        row, col = 0, 0
        for btn in buttons:
            action = lambda x=btn: self.on_click(x)
            tk.Button(buttons_frame, text=btn, width=5, height=2, command=action).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def on_click(self, key):
        if key == 'C':
            self.pin_display = ""
        elif key == '✓':
            self.submit_pin()
        else:
            self.pin_display += key
        
        self.display.delete(0, tk.END)
        self.display.insert(0, self.pin_display)

    def submit_pin(self):
        if self.pin_display == config.SECRET_PIN:
            messagebox.showinfo("Access Granted", "Welcome, Admin!")
            main.add_access_log("SUCCESSFUL_LOGIN", "Correct PIN entered via GUI.")
        else:
            messagebox.showerror("Access Denied", "Incorrect PIN!")
            key_fingerprint = hashlib.sha256(config.SECRET_KEY.encode()).hexdigest()[:16]
            #print(f"🔑 Key Fingerprint: {}")
            main.add_access_log("FAILED_ATTEMPT", f"GUI Login failed: {key_fingerprint}")
        
        self.pin_display = ""
        self.display.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartLockerGUI(root)
    root.mainloop()