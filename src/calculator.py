import math 

class Calculator:
    
    def __init__(self, app, loan_amount, annual_interest_rate, loan_term, monthly_income, monthly_expenses):
        self.app = app
        self.loan_amount = float(loan_amount)
        self.annual_interest_rate = float(annual_interest_rate)
        self.loan_term = float(loan_term)
        self.monthly_income = float(monthly_income)
        self.monthly_expenses = float(monthly_expenses)

    def run(self):
        self.calculate_monthly_interest()
        self.calculate_monthly_payments_number()
        self.calculate_monthly_repayment()
        self.calculate_total_repayment()
        self.calculate_total_interest()
        self.calculate_monthly_cash_surplus()
        self.afforability_calculator()
        self.information_print()

    def calculate_monthly_interest(self):
        self.monthly_interest = self.annual_interest_rate/(100*12)
        return self.monthly_interest

    def calculate_monthly_payments_number(self):
        self.monthly_payments_number = self.loan_term*12
        return self.monthly_payments_number

    def calculate_monthly_repayment(self):
        self.monthly_repayment = (self.loan_amount*self.monthly_interest*((1+self.monthly_interest)**(self.monthly_payments_number))) / (((1+self.monthly_interest)**(self.monthly_payments_number))-1) 
        return self.monthly_repayment

    def calculate_total_repayment(self):
        self.total_repayment = self.monthly_repayment*self.monthly_payments_number
        return self.total_repayment

    def calculate_total_interest(self):
        self.total_interest = self.total_repayment - self.loan_amount
        return self.total_interest

    def calculate_monthly_cash_surplus(self):
        self.monthly_cash_surplus = self.monthly_income - self.monthly_expenses - self.monthly_repayment
        return self.monthly_cash_surplus

    def afforability_calculator(self):
        if self.monthly_cash_surplus >= 0:
            self.afforability_status: bool = True
        else:
            self.afforability_status: bool = False
             
    def information_print(self):
        # round up to nearest cent
        self.monthly_cash_surplus_display = math.ceil(self.monthly_cash_surplus * 100) / 100
        self.monthly_repayment_display = math.ceil(self.monthly_repayment * 100) / 100
        self.total_repayment_display = math.ceil(self.total_repayment * 100) / 100

        self.app.write_msg("----------------------")
        self.app.write_msg(f"monthly interest: [{self.monthly_interest}]")
        self.app.write_msg(f"monthly payments number: [{self.monthly_payments_number}]")
        self.app.write_msg(f"monthly repayment: [${self.monthly_repayment_display}]")
        self.app.write_msg(f"total repayment: [${self.total_repayment_display}]")
        self.app.write_msg(f"total interest: [{self.total_interest}]")
        self.app.write_msg(f"monthly cash surplus: [${self.monthly_cash_surplus_display}]")
        self.app.write_msg("----------------------")
        if self.afforability_status == True:
            self.app.write_msg("afforability status: True")
        else:
            self.app.write_msg("afforability status: False")
