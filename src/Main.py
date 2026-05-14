import tkinter as tk

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
        self.button = tk.Button(self.root, text="Click Me", command=self.show_result)

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
        self.loan_term_label_entry = tk.Entry(self.root, width=10)
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

        #grid
        self.text_box_label.grid(row=0, column=0, **self.grid_setting)
        self.text_box.grid(row=2, column=0, columnspan=2, **self.grid_setting)
        self.button.grid(row=3, column=0, **self.grid_setting)
            
            #labels
        self.loan_amount_label.grid(row=4, column=0, **self.grid_setting)
        self.annual_interest_rate_label.grid(row=5, column=0, **self.grid_setting)
        self.loan_term_label.grid(row=6, column=0, **self.grid_setting)
        self.monthly_income_label.grid(row=7, column=0, **self.grid_setting)
        self.monthly_expenses_label.grid(row=8, column=0, **self.grid_setting)

            #Entry
        self.loan_amount_entry.grid(row=4, column=1, **self.grid_setting)
        self.annual_interest_rate_entry.grid(row=5, column=1, **self.grid_setting)
        self.loan_term_label_entry.grid(row=6, column=1, **self.grid_setting)
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

    def show_result(self):
        self.write_msg("hello")


def main():
    # program
    root = tk.Tk()
    RootApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
