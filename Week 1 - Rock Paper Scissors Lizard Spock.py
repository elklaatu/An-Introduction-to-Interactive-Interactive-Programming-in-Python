#Import dependencies
import random

#Define CPU function

def number_to_name(number):
    if number == 0:
        result = 'rock'
    elif number == 1:
        result = 'Spock'
    elif number == 2:
        result = 'paper'
    elif number == 3:
        result = 'lizard'
    elif number == 4:
        result = 'scissors'
    return result

#Define player function
    
def name_to_number(name):
    if name == 'rock':
        result = 0
    elif name == 'Spock':
        result = 1
    elif name == 'paper':
        result = 2
    elif name == 'lizard':
        result = 3
    elif name == 'scissors':
        result = 4
    return result

#Define game function

def rpsls(name):
    player_number = name_to_number(name)
    cpu_number = random.randrange(0, 5)
    
#Print Players' choices

    print ("Player chooses", name)
    print ("Computer chooses", number_to_name(cpu_number))

#Math Module

    if (cpu_number + 1) % 5 == player_number:
        print ("Player wins!")
    elif (cpu_number + 2) % 5 == player_number:
        print ("Player wins!")
    elif cpu_number == player_number:
        print ("Player and computer tie!")
    else:
        print ("Computer wins!")

#Prints space in the results
        
    print ("")

#Function test
    
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")