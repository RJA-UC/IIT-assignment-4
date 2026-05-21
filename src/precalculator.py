class PreCalculator:

    @staticmethod
    def entry_fill_validator(number, data_name: str, app):
        try:
            if number == "":
                raise ValueError
            else:
                return number
        except ValueError:
            app.write_msg(f"no value detected in [{data_name}]")
            return None
    
    @staticmethod
    def entry_numeric_validator(number, data_name: str, app):
        try:
            float(number)
            return number
        except ValueError:
            app.write_msg(f"non numeric value inputted in [{data_name}]")
            return None

    @staticmethod
    def entry_sign_validator(number, data_name: str, app):
        try:
            number = float(number)
            if number < 0:
                raise ValueError
            else: 
                return number
        except ValueError:
            app.write_msg(f"invalid number inputted in [{data_name}]")
            return None
    
    @staticmethod
    def overflow_validator(number, data_name: str, app):
        try:
            number = float(number)
            max_number = 9999999
            if number > max_number:
                raise ValueError
            else:
                return number
        except ValueError:
            app.write_msg(f"value inputted in [{data_name}] is too large")
            return None