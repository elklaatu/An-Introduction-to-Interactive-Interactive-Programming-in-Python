# Implementation of classic arcade game Pong

import simplegui
import random

#1.1 Initialize globals
#Screen & Paddles width and height
width = 600
half_width = width / 2
height = 400   
half_height = height / 2
ball_radius = 20
pad_width = 8
pad_height = 100
left = False
right = True

#Paddles: Height and Velocity
paddle1_pos = height / 2.5
paddle2_pos = height / 2.5
paddle1_vel = 0
paddle2_vel = 0
paddle_vel = 5

#Initializing ball in the middle of the table
ball_pos = [half_width, half_height]
#Ball Velocity
ball_vel = [0,2]

#Spawn Ball Function: 
def spawn_ball(direction):
    #Update Globals
    global ball_pos, ball_vel
    ball_pos = [half_width, half_height]	
    ball_vel[0] = -random.randrange(120,240) / 100 
#if direction is RIGHT, the ball's velocity is upper right, else upper left
    if direction == True:
        ball_vel[0] *= -1
    ball_vel[1] = -random.randrange(60, 180) / 100

#Event Handlers
def new_game():
    #Update paddle position
    global paddle1_pos, paddle2_pos
    #Update Score
    global score1, score2
    score1 = 0
    score2 = 0
    spawn_ball(0)
    paddle1_pos = height / 2.5
    paddle2_pos = height / 2.5
    

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    #Draw Midline and Gutters
    c.draw_line([half_width, 0],[half_width, height], 1, "white")
    c.draw_line([pad_width, 0],[pad_width, height], 1, "white")
    c.draw_line([width - pad_width, 0],[width - pad_width, height], 1, "white")
        
    #Update Ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    #If-Statements for Position and Ball Spawning
    if ball_pos[0] <= (ball_radius + pad_width) or ball_pos[0] >= (width - pad_width - ball_radius):        
        ball_vel[0] *= -1
        
        if (ball_pos[0] > half_width):             
            if (ball_pos[1] < paddle2_pos or ball_pos[1] > paddle2_pos + pad_height):
                score1 += 1 
                spawn_ball(left) 
            else: ball_vel[0] += .1 * ball_vel[0]
            
        if (ball_pos[0] < half_width):
            if (ball_pos[1] < paddle1_pos or ball_pos[1] > paddle1_pos + pad_height ):
                score2 += 1
                spawn_ball(right)
            else: ball_vel[0] += .1 * ball_vel[0]
        
    if ball_pos[1] <= ball_radius or ball_pos[1] >= (height - ball_radius):
        ball_vel[1] *= -1
 
    
    #Draw Ball
    c.draw_circle(ball_pos, ball_radius, 2, "White", "Blue")
    
    #Update Paddle Position
    global paddle1_vel, paddle2_vel
    #Keep Paddles in the screen
    if (paddle1_pos <= height - pad_height and paddle1_vel > 0) or (paddle1_pos >= 0 and paddle1_vel < 0) :
        paddle1_pos += paddle1_vel    
    elif (paddle2_pos <= height - pad_height and paddle2_vel > 0) or (paddle2_pos >= 0 and paddle2_vel < 0) :
        paddle2_pos += paddle2_vel  
    
    #Draw Paddles
    c.draw_polygon([[0, paddle1_pos], [pad_width, paddle1_pos],[pad_width, (paddle1_pos) + pad_height ],[0, (paddle1_pos) + pad_height]],1, "green", "white") 
    c.draw_polygon([[width, paddle2_pos], [width - pad_width, paddle2_pos], [width - pad_width, paddle2_pos + pad_height], [width, paddle2_pos + pad_height]],1, "green", "white")
    #Draw Scores
    c.draw_text(str(score1), [225, 100], 60, "Blue")    
    c.draw_text(str(score2), [350, 100], 60, "Red")
#Key Controls        
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle_vel
    #Player 1    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -paddle_vel     
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = paddle_vel  
    #Player 2
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = paddle_vel    
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -paddle_vel 

#Key controls        
def keyup(key):
    global paddle1_vel, paddle2_vel, paddle_vel
    
    #Player 1
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        
    #Player 2
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
      
#Create frame

frame = simplegui.create_frame("Pong", width, height)
frame.set_canvas_background('Green')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Play again!", new_game, 200)

# Start Frame
new_game()
frame.start()