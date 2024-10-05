import random
import string


def hello():
    print("Hi from Madras Techie")

def height():
    print("We are all tall")    

def weight():
    print("We are all weight")

def location():
    print("We are worldly beings")    

def job():
    print("We work on the best possible works suitable for us")

def sports():
    print("We play our best suitable sports")    

def generate_random_password():
    length=12    
    characters = string.ascii_letters + string.digits + string.punctuation        
    password = ''.join(random.choice(characters) for i in range(length))
    
    print(password)

def random_number():
    random_numbers = [random.randint(start, end) for _ in range(size)]
    
    print(random_numbers)