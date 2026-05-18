import tkinter as tk
from tkinter import messagebox, ttk
from src.precalculator import PreCalculator
from src.calculator import Calculator

# program

class RootApp:

    def __init__(self, root):
        self.root = root
        self.main_ui()
        self.initial_msg()
    # window
    
    def main_ui(self):
        self.root.title("loan calculator")
        self.root.geometry("1000x750")

        #button
        self.button = tk.Button(self.root, text="Enter", command=self.full_pipeline)
        self.clr_scrn_btn = tk.Button(self.root, text="Clear Screen", command=self.clear_screen)

        # labels
        self.text_box_label = tk.Label(self.root, text="log")

        self.loan_amount_label = tk.Label(self.root, text="Loan Amount")
        self.annual_interest_rate_label = tk.Label(self.root, text="Annual Interest Rate")
        self.loan_term_label = tk.Label(self.root, text="Loan Term")
        self.monthly_income_label = tk.Label(self.root, text="Monthly Income")
        self.monthly_expenses_label = tk.Label(self.root, text="Monthly Expenses")

        #Entry
        self.loan_amount_entry = tk.Entry(self.root, width=10)
        self.annual_interest_rate_entry = tk.Entry(self.root, width=10)
        self.loan_term_entry = tk.Entry(self.root, width=10)
        self.monthly_income_entry = tk.Entry(self.root, width=10)
        self.monthly_expenses_entry = tk.Entry(self.root, width=10)

        # text box
        self.text_box = tk.Text(self.root, height=30, width=100)

        # text box settings
        self.text_box.config(state="disabled")  # doesnt allow textbox to be typed in

        #grid settings
        self.grid_setting = {
            "padx": 10, 
            "pady": 5,
            "sticky": "w"
            }

        #grid placement 
            #tect box
        self.text_box.grid(row=2, column=0, columnspan=4, **self.grid_setting)
            
            #button
        self.button.grid(row=3, column=0, **self.grid_setting)
        self.clr_scrn_btn.grid(row=3, column=1, **self.grid_setting)

            #labels
        self.text_box_label.grid(row=0, column=0, **self.grid_setting)
        self.loan_amount_label.grid(row=4, column=0, **self.grid_setting)
        self.annual_interest_rate_label.grid(row=5, column=0, **self.grid_setting)
        self.loan_term_label.grid(row=6, column=0, **self.grid_setting)
        self.monthly_income_label.grid(row=7, column=0, **self.grid_setting)
        self.monthly_expenses_label.grid(row=8, column=0, **self.grid_setting)

            #Entry
        self.loan_amount_entry.grid(row=4, column=1, **self.grid_setting)
        self.annual_interest_rate_entry.grid(row=5, column=1, **self.grid_setting)
        self.loan_term_entry.grid(row=6, column=1, **self.grid_setting)
        self.monthly_income_entry.grid(row=7, column=1, **self.grid_setting)
        self.monthly_expenses_entry.grid(row=8, column=1, **self.grid_setting)
    
    def write_msg(self, message):
        self.message = message
        self.text_box.config(state="normal")
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.config(state="disabled")
        self.text_box.see(tk.END)
    
    def initial_msg(self):
        self.write_msg("program initialised")
        

    def clear_screen(self):
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", tk.END)
        self.text_box.config(state="disabled")
    
    def get_value(self, entry, data_name):
        self.entry = entry
        self.data_name = data_name
        a = entry
        a = PreCalculator.entry_fill_validator(a, data_name, self)
        if a is not None:
            a = PreCalculator.entry_numeric_validator(a, data_name, self)
            return a
        else:
            return None
        
    def get_value_all(self):
        loan_amount = self.get_value(self.loan_amount_entry.get(), "loan amount")
        annual_interest_rate = self.get_value(self.annual_interest_rate_entry.get(), "annual interest rate")
        loan_term = self.get_value(self.loan_term_entry.get(), "loan term")
        monthly_income = self.get_value(self.monthly_income_entry.get(), "monthly income")
        monthly_expenses = self.get_value(self.monthly_expenses_entry.get(), "monthly expenses")
        return loan_amount, annual_interest_rate, loan_term, monthly_income, monthly_expenses

    def full_pipeline(self):
        loan_amount, annual_interest_rate, loan_term, monthly_income, monthly_expenses = self.get_value_all()
        if all([
            loan_amount is not None,
            annual_interest_rate is not None,
            loan_term is not None,
            monthly_income is not None,
            monthly_expenses is not None
        ]):
            self.write_msg("------------")
            self.write_msg("successfully input values")
            self.write_msg("------------")
            calc = Calculator(self, loan_amount, annual_interest_rate, loan_term, monthly_income, monthly_expenses)
            calc.run()
