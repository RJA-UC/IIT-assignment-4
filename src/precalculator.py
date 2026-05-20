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