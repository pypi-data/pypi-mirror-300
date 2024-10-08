"""Labb 3 module. Used to read user input and for error handeling.  
"""
def input_data(data_type, prompt):
    """Prompts the user to input a string and tries to convert it to a desired data type. 

    Args:
        data_type (class object): The data type the input is excpected to be. 
        prompt (string): A string to print before the users input. 

    Returns:
        num (any): The users input string converted to the same data type as the data_type variable. 
    """
    try:
        num = input(prompt)
        num = data_type(num)
        print(type(num).__name__)
    except ValueError:
        print(f"That was not a {data_type.__name__}!")
    return num