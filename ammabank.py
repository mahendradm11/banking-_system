import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import pyttsx3
import speech_recognition as sr
import qrcode

# Simulated Data
users = {"admin": "password123"}  # username: password
transactions = []
languages = {"English": "Hello!", "Kannada": "ನಮಸ್ಕಾರ!"}  # Multi-language support

# Functions for new features
def generate_cardless_code():
    otp = random.randint(100000, 999999)
    qr_data = f"Cardless Withdraw: OTP={otp}"
    qr = qrcode.make(qr_data)
    qr.save("cardless_qr.png")
    messagebox.showinfo("Cardless Withdraw", f"Your OTP is {otp}. QR Code saved as 'cardless_qr.png'.")

def apply_for_loan():
    def submit_loan():
        try:
            income = int(entry_income.get())
            amount = int(entry_loan_amount.get())
            if amount < (income * 10):
                messagebox.showinfo("Loan Approved", "Your loan has been approved!")
            else:
                messagebox.showerror("Loan Rejected", "Your loan exceeds eligibility.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for income and loan amount.")
    
    loan_window = tk.Toplevel()
    loan_window.title("Loan Application")
    tk.Label(loan_window, text="Monthly Income:").grid(row=0, column=0)
    entry_income = tk.Entry(loan_window)
    entry_income.grid(row=0, column=1)
    tk.Label(loan_window, text="Loan Amount:").grid(row=1, column=0)
    entry_loan_amount = tk.Entry(loan_window)
    entry_loan_amount.grid(row=1, column=1)
    tk.Button(loan_window, text="Submit", command=submit_loan).grid(row=2, columnspan=2)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand your command."

def assist_user():
    user_command = recognize_speech()
    if "balance" in user_command:
        speak("Your balance is Rs. 50,000")
    elif "loan" in user_command:
        speak("You can apply for a loan in the loan section.")
    else:
        speak("How can I assist you further?")

# Banking System Class
class BankingSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Automated Banking System")
        self.root.geometry("800x600")
        self.logged_in_user = None

        # Login screen
        self.show_login_screen()

    def show_login_screen(self):
        """Display login screen."""
        self.clear_screen()
        tk.Label(self.root, text="Welcome to AI Automated Banking System", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Login", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.show_register_screen).pack(pady=5)

    def show_register_screen(self):
        """Display registration screen."""
        self.clear_screen()
        tk.Label(self.root, text="Register", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack()
        tk.Button(self.root, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.show_login_screen).pack()

    def show_dashboard(self):
        """Display dashboard."""
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.logged_in_user}!", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Expense Tracker", command=self.show_expense_tracker).pack(pady=10)
        tk.Button(self.root, text="Loan Eligibility Checker", command=apply_for_loan).pack(pady=10)
        tk.Button(self.root, text="Cardless Withdraw", command=generate_cardless_code).pack(pady=10)
        tk.Button(self.root, text="AI Assistance", command=assist_user).pack(pady=10)
        tk.Button(self.root, text="Fraud Detection", command=self.fraud_detection).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def show_expense_tracker(self):
        """Simple expense tracker."""
        self.clear_screen()
        tk.Label(self.root, text="Expense Tracker", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Enter expense description").pack()
        self.expense_desc_entry = tk.Entry(self.root)
        self.expense_desc_entry.pack()
        tk.Label(self.root, text="Enter expense amount").pack()
        self.expense_amount_entry = tk.Entry(self.root)
        self.expense_amount_entry.pack()
        tk.Button(self.root, text="Add Expense", command=self.add_expense).pack(pady=10)
        tk.Button(self.root, text="Back to Dashboard", command=self.show_dashboard).pack(pady=10)

        # Show transaction history
        tk.Label(self.root, text="Transaction History:").pack()
        self.history = scrolledtext.ScrolledText(self.root, width=50, height=10)
        self.history.pack(pady=5)
        self.update_history()

    def fraud_detection(self):
        """Simple fraud detection simulation."""
        self.clear_screen()
        tk.Label(self.root, text="Fraud Detection", font=("Arial", 14)).pack(pady=10)
        fraud_detected = random.choice([True, False])
        if fraud_detected:
            messagebox.showwarning("Fraud Alert", "Suspicious transaction detected!")
        else:
            messagebox.showinfo("All Clear", "No suspicious activity detected.")
        tk.Button(self.root, text="Back to Dashboard", command=self.show_dashboard).pack()

    def login(self):
        """Handle login."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in users and users[username] == password:
            self.logged_in_user = username
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        """Handle registration."""
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        if username in users:
            messagebox.showerror("Error", "User already exists!")
        else:
            users[username] = password
            messagebox.showinfo("Success", "User registered successfully!")
            self.show_login_screen()

    def add_expense(self):
        """Add expense to transaction history."""
        desc = self.expense_desc_entry.get()
        amount = self.expense_amount_entry.get()
        if desc and amount.isdigit():
            transactions.append(f"{desc}: ₹{amount}")
            self.update_history()
        else:
            messagebox.showerror("Error", "Enter valid details.")

    def update_history(self):
        """Update transaction history."""
        self.history.delete(1.0, tk.END)
        for t in transactions:
            self.history.insert(tk.END, t + "\n")

    def logout(self):
        """Handle logout."""
        self.logged_in_user = None
        self.show_login_screen()

    def clear_screen(self):
        """Clear the screen for new views."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystemApp(root)
    root.mainloop()

