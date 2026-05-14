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
        self.text_box = tk.Text(self.root, height=30, width=100)

        # text box settings
        self.text_box.config(state="disabled")  # doesnt allow textbox to be typed in

        #grid settings
        self.grid_setting = {
            "padx": 10, 
            "sticky": "w"
            }

        #grid
        self.text_box_label.grid(row=1, column=0, **self.grid_setting)
        self.text_box.grid(row=2, column=0, **self.grid_setting)
        self.button.grid(row=3, column=0, pady=5, **self.grid_setting)

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
