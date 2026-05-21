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
        self.report_creator = None
        self.last_calc = None
    
    def main_ui(self):
        self.root.title("Loan Calculator")
        self.root.geometry("1000x770")
        self.root.config(bg="#f5f5f5")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        
        log_frame = ttk.LabelFrame(self.root, text=" Results Log ", padding=10)
        log_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.text_box = tk.Text(
            log_frame,
            height=30,
            width=100,
            font=("Consolas", 9),
            bg="#ffffff",
            fg="#2c3e50",
            relief="flat",
            padx=10,
            pady=10,
            yscrollcommand=scrollbar.set,
            state="disabled"
        )
        self.text_box.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.text_box.yview)
        
        input_frame = ttk.LabelFrame(self.root, text=" Input Fields ", padding=15)
        input_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=15)
        input_frame.grid_columnconfigure(0, weight=0)
        
        ttk.Label(input_frame, text="Loan Amount").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.loan_amount_entry = ttk.Entry(input_frame, width=12)
        self.loan_amount_entry.grid(row=0, column=1, sticky="w", padx=(0, 20))
        
        ttk.Label(input_frame, text="Annual Interest Rate (%)").grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.annual_interest_rate_entry = ttk.Entry(input_frame, width=12)
        self.annual_interest_rate_entry.grid(row=0, column=3, sticky="w", padx=(0, 20))
        
        ttk.Label(input_frame, text="Loan Term (Years)").grid(row=0, column=4, sticky="w", padx=(0, 10))
        self.loan_term_entry = ttk.Entry(input_frame, width=12)
        self.loan_term_entry.grid(row=0, column=5, sticky="w", padx=(0, 20))
        
        ttk.Label(input_frame, text="Monthly Income ($)").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.monthly_income_entry = ttk.Entry(input_frame, width=12)
        self.monthly_income_entry.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        
        ttk.Label(input_frame, text="Monthly Expenses ($)").grid(row=1, column=2, sticky="w", padx=(0, 10), pady=(10, 0))
        self.monthly_expenses_entry = ttk.Entry(input_frame, width=12)
        self.monthly_expenses_entry.grid(row=1, column=3, sticky="w", padx=(0, 20), pady=(10, 0))
        
        ttk.Button(input_frame, text="⬅️ Calculate", command=self.full_pipeline).grid(row=1, column=4, sticky="w", padx=(0, 5), pady=(10, 0))
        ttk.Button(input_frame, text="🧹 Clear", command=self.clear_entry).grid(row=1, column=5, sticky="w", pady=(10, 0))
        
        action_frame = ttk.LabelFrame(self.root, text=" Actions ", padding=15)
        action_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        ttk.Button(action_frame, text="💾 Save Options", command=self.open_child_window).pack(side="left", padx=(0, 10))
        ttk.Button(action_frame, text="🧹 Clear Screen", command=self.clear_screen).pack(side="left", padx=(0, 10))
        ttk.Button(action_frame, text="🚪 Exit", command=self.exit_program).pack(side="left")
    
    def write_msg(self, message):
        self.message = message
        self.text_box.config(state="normal")
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.config(state="disabled")
        self.text_box.see(tk.END)
    
    def initial_msg(self):
        self.write_msg("✓ Program initialized")
    
    def exit_program(self):
        self.root.destroy()
    
    def clear_screen(self):
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", tk.END)
        self.text_box.config(state="disabled")

    def clear_entry(self):
        self.loan_amount_entry.delete(0, tk.END)
        self.annual_interest_rate_entry.delete(0, tk.END) 
        self.loan_term_entry.delete(0, tk.END) 
        self.monthly_income_entry.delete(0, tk.END) 
        self.monthly_expenses_entry.delete(0, tk.END) 
    
    def get_value(self, entry, data_name):
        self.entry = entry
        self.data_name = data_name
        a = entry
        a = PreCalculator.entry_fill_validator(a, data_name, self)
        if a is not None:
            a = PreCalculator.entry_numeric_validator(a, data_name, self)
        if a is not None:
            a = PreCalculator.overflow_validator(a, data_name, self)
        if a is not None:
            a = PreCalculator.entry_sign_validator(a, data_name, self)
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

            self.write_msg("✓ Successfully input values")
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
 
        self.window.title("Save Config")
        self.window.geometry("250x291")
        self.window.config(bg="#f5f5f5")
        
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        content_frame = ttk.Frame(self.window)
        content_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        content_frame.grid_columnconfigure(0, weight=1)
        
        file_frame = ttk.LabelFrame(content_frame, text=" File Operations ", padding=15)
        file_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        file_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Button(file_frame, text="📄 Save .txt", command=self.save_report_txt).grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Button(file_frame, text="📂 Retrieve .txt", command=self.retrieve_text).grid(row=1, column=0, sticky="ew", pady=(0, 8))
        ttk.Button(file_frame, text="🌐 Save .html", command=self.save_report_html).grid(row=2, column=0, sticky="ew")
        
        db_frame = ttk.LabelFrame(content_frame, text=" Database Operations ", padding=15)
        db_frame.grid(row=1, column=0, sticky="ew")
        db_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Button(db_frame, text="💾 Save to Database", command=self.save_database).grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Button(db_frame, text="⚙️ Database Settings", command=self.open_database_window).grid(row=1, column=0, sticky="ew")
 
    def save_report_txt(self):
        try:
            self.app.report_creator.save_txt_file()
            self.app.write_msg("text file successfully saved")
        except AttributeError:
            self.app.write_msg("please run calculator first")
 
    def retrieve_text(self):
        if self.app.report_creator is not None:
            self.app.report_creator.read_file_to_textbox()
        else:
            try:
                from src.utils.reportcreator import ReportCreator
                temp_reporter = ReportCreator(self.app, None, None, None, None, None, None, None)
                temp_reporter.read_file_to_textbox()
            except Exception as e:
                self.app.write_msg("Could not retrieve file. Ensure a history file exists.")
 
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
            c = self.app.last_calc
            self.app.db.insert_record(
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
 
    def save_report_txt(self):
        try:
            self.app.report_creator.save_txt_file()
            self.app.write_msg("text file successfully saved")
        except AttributeError:
            self.app.write_msg("please run calculator first")
 
    def retrieve_text(self):
        if self.app.report_creator is not None:
            self.app.report_creator.read_file_to_textbox()
        else:
            try:
                from src.utils.reportcreator import ReportCreator
                temp_reporter = ReportCreator(self.app, None, None, None, None, None, None, None)
                temp_reporter.read_file_to_textbox()
            except Exception as e:
                self.app.write_msg("Could not retrieve file. Ensure a history file exists.")
 
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
            c = self.app.last_calc 
            self.app.db.insert_record(   
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
        
        self.db = app.db 
        
        self.databaseUI.grid_rowconfigure(1, weight=1)
        self.databaseUI.grid_columnconfigure(0, weight=1)
        
        self.create_query_panel()
        self.create_display_panel()
        
        self.show_all_records()
 
    def create_query_panel(self):
        # Creates custom query actions targeting specific methods in Database
        query_frame = ttk.LabelFrame(self.databaseUI, text=" Queries & Operations ", padding=10)
        query_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=5)
        
        # Configure column weights for buttons
        query_frame.grid_columnconfigure(0, weight=1)
        query_frame.grid_columnconfigure(1, weight=1)
        query_frame.grid_columnconfigure(2, weight=1)
        query_frame.grid_columnconfigure(3, weight=1)
        
        # Connect buttons directly to your specific class methods
        ttk.Button(query_frame, text="Show All Records", command=self.show_all_records).grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(query_frame, text="Multi-Table JOIN", command=self.show_multi_table).grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(query_frame, text="Calculate Yearly Interest", command=self.show_calculated_fields).grid(row=0, column=2, padx=5, sticky="ew")
        ttk.Button(query_frame, text="View Aggregates (AVG/SUM)", command=self.show_aggregates).grid(row=0, column=3, padx=5, sticky="ew")
 
    def create_display_panel(self):
        # Builds a dynamic spreadsheet-style spreadsheet view.
        display_frame = ttk.LabelFrame(self.databaseUI, text=" Output Display Window ", padding=10)
        display_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
        
        # Configure grid weights
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbar mechanics
        scrollbar = ttk.Scrollbar(display_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.tree = ttk.Treeview(display_frame, columns=(), show="headings", yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
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