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
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Generate a list of random numbers.")
    
    # Define the arguments with names like `size`, `start`, and `end`
    parser.add_argument('--size', type=int, required=True, help="Number of random numbers to generate.")
    parser.add_argument('--start', type=int, required=True, help="Start range of random numbers.")
    parser.add_argument('--end', type=int, required=True, help="End range of random numbers.")
    
    # Parse the arguments
    args = parser.parse_args()

    # Use the arguments to generate random numbers
    random_numbers = [random.randint(args.start, args.end) for _ in range(args.size)]
    
    # Print the random numbers
    print(random_numbers)