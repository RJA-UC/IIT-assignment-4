import tkinter as tk
from tkinter import messagebox, ttk 
from src.precalculator import PreCalculator
from src.calculator import Calculator
from src.utils.reportcreator import ReportCreator, Database

# program

class RootApp:

    def __init__(self, root):
        self.root = root
        self.main_ui()
        self.initial_msg()
        self.db = Database()
    # window
    
    def main_ui(self):
        self.root.title("loan calculator")
        self.root.geometry("1000x750")

        #button
        self.button = tk.Button(self.root, text="Enter", command=self.full_pipeline)
        self.clr_scrn_btn = tk.Button(self.root, text="Clear Screen", command=self.clear_screen)
        self.open_child_window_btn = tk.Button(self.root, text="Save options", command=self.open_child_window)
        

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
        self.open_child_window_btn.grid(row=3, column=2, **self.grid_setting)

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
    
    def open_child_window(self):
        ChildWindow(self.root, self)

    def full_pipeline(self):
        loan_amount, annual_interest_rate, loan_term, monthly_income, monthly_expenses = self.get_value_all()
        if all([
            loan_amount is not None,
            annual_interest_rate is not None,
            loan_term is not None,
            monthly_income is not None,
            monthly_expenses is not None
        ]):

            self.write_msg("successfully input values")
            calc = Calculator(self, loan_amount, annual_interest_rate, loan_term, monthly_income, monthly_expenses)
            calc.run()

            self.last_calc = {
                "loan_amount": loan_amount,
                "annual_rate": annual_interest_rate,
                "loan_years": loan_term,
                "monthly_repayment": calc.monthly_repayment_display,
                "total_repayment": calc.total_repayment_display,
                "total_interest": calc.total_interest,
                "affordability": calc.afforability_status
            }

            self.report_creator = ReportCreator(self, calc.monthly_interest, calc.monthly_payments_number, calc.monthly_repayment_display, calc.total_repayment_display, calc.total_interest, calc.monthly_cash_surplus_display, calc.afforability_status)
            

class ChildWindow:
    def __init__(self, parent, app):
        self.window = tk.Toplevel(parent)
        self.app = app

        self.window.title("save config")
        self.window.geometry("300x450")

        self.CHILD_BUTTON_SETTINGS = {
            "width": 20,
            "height": 3,
            "font": ("Arial", 16)
        }

        save_text_btn = tk.Button(self.window, text="save .txt file", **self.CHILD_BUTTON_SETTINGS, command=self.save_report_txt)
        save_html_btn = tk.Button(self.window, text="save .html file", **self.CHILD_BUTTON_SETTINGS, command=self.save_report_html)
        save_database_btn = tk.Button(self.window, text="save database", **self.CHILD_BUTTON_SETTINGS, command=self.save_database)
        open_database_windows = tk.Button(self.window, text="database settings", **self.CHILD_BUTTON_SETTINGS, command=self.open_database_window)
        # database_opt_btn = tk.Button(self.window, text="save database", **self.CHILD_BUTTON_SETTINGS, command=self.save_database)

        self.window.grid_columnconfigure(0, weight=1)
        self.CHILD_GRID_SETTINGS = {
            "padx": 10,
            "pady": 10,
            "sticky":"n"
        }
        # grid
        save_text_btn.grid(row=0, column=0, **self.CHILD_GRID_SETTINGS)
        save_html_btn.grid(row=1, column=0, **self.CHILD_GRID_SETTINGS)
        save_database_btn.grid(row=2, column=0, **self.CHILD_GRID_SETTINGS)
        open_database_windows.grid(row=3, column=0, **self.CHILD_GRID_SETTINGS)

    def save_report_txt(self):
        try:
            self.app.report_creator.save_txt_file()
            self.app.write_msg("text file successfully saved")
        except AttributeError:
            self.app.write_msg("please run calculator first")

    def save_report_html(self):
        try:
            self.app.report_creator.save_html_file()
            self.app.write_msg("html file successfully created")
        except AttributeError:
            self.app.write_msg("please run calculator first")
    
    def open_database_window(self):
        DatabaseApp(self.window, self.app)

    def save_database(self):
        try:
            c = self.app.last_calc  # ✅ get stored values
            self.app.db.insert_record(   # ✅ correct db reference
                c["loan_amount"],
                c["annual_rate"],
                c["loan_years"],
                c["monthly_repayment"],
                c["total_repayment"],
                c["total_interest"],
                c["affordability"]
            )
            self.app.write_msg("database successfully saved")
        except AttributeError:
            self.app.write_msg("please run calculator first")

class DatabaseApp:
    def __init__(self, parent, app):
        self.databaseUI = tk.Toplevel(parent)
        self.app = app
        
        self.databaseUI.geometry("1000x500")
        self.databaseUI.title("Database Settings")
        
        # Re-use the database connection already initialized in RootApp
        self.db = app.db 
        
        # Build UI layout (Only queries and data display)
        self.create_query_panel()
        self.create_display_panel()
        
        # Load up any existing records right out of the gate
        self.show_all_records()

    def create_query_panel(self):
        # Creates custom query actions targeting specific methods in Database
        query_frame = ttk.LabelFrame(self.databaseUI, text=" Queries & Operations ", padding=10)
        query_frame.pack(fill="x", padx=15, pady=5)
        
        # Connect buttons directly to your specific class methods
        ttk.Button(query_frame, text="Show All Records", command=self.show_all_records).pack(side="left", padx=5)
        ttk.Button(query_frame, text="Multi-Table JOIN", command=self.show_multi_table).pack(side="left", padx=5)
        ttk.Button(query_frame, text="Calculate Yearly Interest", command=self.show_calculated_fields).pack(side="left", padx=5)
        ttk.Button(query_frame, text="View Aggregates (AVG/SUM)", command=self.show_aggregates).pack(side="left", padx=5)

    def create_display_panel(self):
        # Builds a dynamic spreadsheet-style spreadsheet view.
        display_frame = ttk.LabelFrame(self.databaseUI, text=" Output Display Window ", padding=10)
        display_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Scrollbar mechanics
        scrollbar = ttk.Scrollbar(display_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(display_frame, columns=(), show="headings", yscrollcommand=scrollbar.set)
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

    def reset_tree_headers(self, columns):
        # Cleans out old structures in the view to match new data structures dynamically.
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

    def show_all_records(self):
        headers = ("ID", "User ID", "Loan Amt", "Rate (%)", "Years", "Monthly Rep", "Total Rep", "Total Int", "Affordability")
        self.reset_tree_headers(headers)
        for row in self.db.retrieve_records():
            self.tree.insert("", "end", values=row)

    def show_multi_table(self):
        headers = ("User Name", "Loan Amount ($)", "Monthly Repayment ($)")
        self.reset_tree_headers(headers)
        for row in self.db.multi_table_query():
            self.tree.insert("", "end", values=row)

    def show_calculated_fields(self):
        headers = ("Loan Base ($)", "Interest Rate (%)", "Estimated Yearly Interest ($)")
        self.reset_tree_headers(headers)
        for row in self.db.calculated_field():
            self.tree.insert("", "end", values=row)

    def show_aggregates(self):
        headers = ("Total Database Records", "Average Monthly Repayment ($)", "Cumulative Interest Handled ($)")
        self.reset_tree_headers(headers)
        row = self.db.aggregate_query()
        
        # Clean formatting just in case the data engine passes empty Null/None values
        cleaned_row = (
            row[0] if row[0] else 0,
            f"${row[1]:,.2f}" if row[1] else "$0.00",
            f"${row[2]:,.2f}" if row[2] else "$0.00"
        )
        self.tree.insert("", "end", values=cleaned_row)