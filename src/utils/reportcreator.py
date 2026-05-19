from pathlib import Path
import sqlite3

class ReportCreator:
    def __init__(self, app, monthly_interest, monthly_payments_number, monthly_repayment_display, total_repayment_display, total_interest, monthly_cash_surplus_display, afforability_status):
        self.app = app
        self.OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.monthly_interest = monthly_interest
        self.monthly_payments_number = monthly_payments_number
        self.monthly_repayment_display = monthly_repayment_display
        self.total_repayment_display = total_repayment_display
        self.total_interest = total_interest
        self.monthly_cash_surplus_display = monthly_cash_surplus_display
        self.afforability_status = afforability_status
    
    def save_txt_file(self):
        file_path = self.OUTPUT_DIR  / "loan_report.txt"
        with file_path.open("a") as file:
            file.write("----------------------\n")
            file.write(f"monthly interest: [{self.monthly_interest}]\n")
            file.write(f"monthly payments number: [{self.monthly_payments_number}]\n")
            file.write(f"monthly repayment: [${self.monthly_repayment_display}]\n")
            file.write(f"total repayment: [${self.total_repayment_display}]\n")
            file.write(f"total interest: [{self.total_interest}]\n")
            file.write(f"monthly cash surplus: [${self.monthly_cash_surplus_display}]\n")
            file.write(f"afforability statu: [{self.afforability_status}]\n")
            file.write("----------------------\n")

    def save_html_file(self):
        file_path = self.OUTPUT_DIR / "loan_report.html"
        with file_path.open("a") as file:
            html = f"""<!DOCTYPE html>
            <html>
            <head>
                <title>Loan Affordability Report</title>
            </head>

            <body>

                <h1>Loan Affordability Report</h1>

                <table border="1" cellpadding="8">
                    <tr>
                        <th>Category</th>
                        <th>Value</th>
                    </tr>

                    <tr>
                        <td>Monthly Interest</td>
                        <td>{self.monthly_interest}</td>
                    </tr>

                    <tr>
                        <td>Monthly Payments Number</td>
                        <td>{self.monthly_payments_number}</td>
                    </tr>

                    <tr>
                        <td>Monthly Repayment</td>
                        <td>${self.monthly_repayment_display}</td>
                    </tr>

                    <tr>
                        <td>Total Repayment</td>
                        <td>${self.total_repayment_display}</td>
                    </tr>

                    <tr>
                        <td>Total Interest</td>
                        <td>{self.total_interest}</td>
                    </tr>

                    <tr>
                        <td>Monthly Cash Surplus</td>
                        <td>${self.monthly_cash_surplus_display}</td>
                    </tr>

                    <tr>
                        <td>Affordability Status</td>
                        <td>{self.afforability_status}</td>
                    </tr>

                </table>

            </body>
            </html>"""
            file.write(html)
    


class Database:
    def __init__(self):
        self.OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.OUTPUT_DIR / "loan_calculator.db")  
        self.cursor = self.conn.cursor()
        self.create_tables()  

    def create_tables(self):
        # Table 1 - users (needed for multi-table query)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Table 2 - loan records
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS loan_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                loan_amount REAL,
                annual_rate REAL,
                loan_years INTEGER,
                monthly_repayment REAL,
                total_repayment REAL,
                total_interest REAL,
                affordability TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def insert_record(self, loan_amount, annual_rate, loan_years,
                      monthly_repayment, total_repayment, total_interest, affordability):
        # Default to user_id = 1 (create a default user if needed)
        self.cursor.execute("""
            INSERT INTO users (name) VALUES (?)
        """, ("Default User",))
        user_id = self.cursor.lastrowid  # get the new user's id

        self.cursor.execute("""
            INSERT INTO loan_records 
                (user_id, loan_amount, annual_rate, loan_years, 
                 monthly_repayment, total_repayment, total_interest, affordability)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, loan_amount, annual_rate, loan_years,
              monthly_repayment, total_repayment, total_interest, affordability))
        self.conn.commit()

    def retrieve_records(self):
        self.cursor.execute("SELECT * FROM loan_records")
        return self.cursor.fetchall()  # returns list of tuples

    def multi_table_query(self):
        self.cursor.execute("""
            SELECT users.name, loan_records.loan_amount, loan_records.monthly_repayment
            FROM loan_records
            JOIN users ON users.id = loan_records.user_id
        """)
        return self.cursor.fetchall()

    def calculated_field(self):
        self.cursor.execute("""
            SELECT loan_amount, annual_rate,
                   (loan_amount * annual_rate / 100) AS estimated_yearly_interest
            FROM loan_records
        """)
        return self.cursor.fetchall()

    def aggregate_query(self):
        self.cursor.execute("""
            SELECT COUNT(*) AS total_records,
                   AVG(monthly_repayment) AS avg_repayment,
                   SUM(total_interest) AS total_interest_paid
            FROM loan_records
        """)
        return self.cursor.fetchone()  # only one row for aggregates

    def close(self):
        self.conn.close()