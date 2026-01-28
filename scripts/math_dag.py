# schedule: 0 9 * * *

def sum_nums():
    from random import randint
    print(f"** Let's take 2 random numbers and sum them **")
    x = randint(0, 100)
    y = randint(0, 100)
    print(f"x: {x}, y: {y}")
    print(f"** sum: {x+y} **")

def multiply_nums():
    from random import randint
    print(f"** Let's take 2 random numbers and multiply them **")
    x = randint(0, 100)
    y = randint(0, 100)
    print(f"x: {x}, y: {y}")
    print(f"** multiply: {x*y} **")

def divide_nums():
    from random import randint
    print(f"** Let's take 2 random numbers and divide them **")
    x = randint(1, 100)
    y = randint(1, 100)
    print(f"x: {x}, y: {y}")
    print(f"** divide: {x//y} **")