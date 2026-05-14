class PreCalculator:

    @staticmethod
    def entry_fill_validator(number, data_name: str, app):
        if number == "":
            app.write_msg(f"no value detected in [{data_name}]")
            return None
        else:
            return number
    
    @staticmethod
    def entry_numeric_validator(number, data_name: str, app):
        if number.replace(".", "", 1).isnumeric():
            return float(number)
        else:
            app.write_msg(f"non numeric value inputted in [{data_name}]")
            return None
            
