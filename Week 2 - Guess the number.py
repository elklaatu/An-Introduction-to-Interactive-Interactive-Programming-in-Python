#1. Define globals

#1.1 Import libraries
import math
import simplegui
import random

#1.2 Define global variables

number_range = 100
secret_number = 0
remaining_guesses = 0

#2. Define helper functions

#2.1. Restart game

def new_game():
    global num_range
    global secret_number
    global remaining_guesses
    
    secret_number = random.randrange(0,number_range)
    
    if number_range == 100:
        remaining_guesses = 7
    elif number_range == 1000:
        remaining_guesses = 10
        
    print ("Welcome to 'Guess the number'. You chose to play in a range from 0 to", number_range,". ENJOY!!!")
    print ("You've got ", remaining_guesses, " guesses left.\n")
    pass

#3. Define event handlers

#3.2. Game from 0-100

def range_100():
    global number_range
    number_range = 100
    new_game()
    pass

#3.2. Game from 0-1000

def range_1000():
    global number_range
    number_range = 1000
    new_game()
    pass

#3.3 Input number by the user

def get_input(guess):
    global secret_number
    global remaining_guesses
    
    win = False
    
    print ("You guessed: ",guess)
    remaining_guesses = remaining_guesses - 1
    print ("Number of guesses left is: ", remaining_guesses)
    
    if int(guess) == secret_number:       
        win = True
    elif int(guess) > secret_number:
        result = "You've got to go lower!\n"
    else:
        result = "Aim higher!\n"                
        
        
    if win:
        print ("Got it! YOU ROCK!!!\n")
        new_game()
        return
    elif remaining_guesses == 0:
        print ("Game over. YOU LOSE!\n")
        new_game()
        return
    else:
        print (result)
        pass

#4 Create a frame

f = simplegui.create_frame("Guess the number",200,200)

#5. Register event handlers

f.add_button("Range is(0,100)", range_100,200)
f.add_button("Range is(0,1000)", range_1000,200)
f.add_input("Enter a guess", get_input,200)

#6. Start frame and timers
new_game()
f.start()