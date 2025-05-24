import random
import string
from blns import naughty_strings

def generate_random_text(length=10):
    """
    Function to generate random text string
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_number(min_value=1, max_value=100):
    """
    Function to generate random number
    """
    return str(random.randint(min_value, max_value))

def generate_naughty_string():
    return naughty_strings[random.randint(0, len(naughty_strings)-1)]


