from pathlib import Path

class ReportCreator:
    def __init__(self, app, monthly_interest, monthly_payments_number, monthly_repayment_display, total_repayment_display, total_interest, monthly_cash_surplus_display, afforability_status):
        self.app = app
        self.OUTPUT_DIR = Path("IIT-assignment-4/output")
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

    # def save_html_file(self):

    # def save_sql_database(self):