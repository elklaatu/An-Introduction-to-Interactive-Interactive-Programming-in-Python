#1. import Libraries

import time
import simplegui

#2. Define global variables
counter = 0
width = 250
height = 250
interval = 100
user_stops = 0
user_points = 0
stop = True

#Helper function

def format(t):
    t_sec = (t) % 10
    seconds = int(t / 10) % 10
    minutes = int(t / 600) % 600
    min_ten = int(t / 100) % 6
    text_string = str(minutes) + ":" + str(min_ten) + str(seconds) + "." + str(t_sec)
    return text_string
pass

#3. Define event handlers for buttons

def start():
    global stop
    stop = False
    clockwatch.start()
    
def stop():
    global stop, user_stops, user_points
    if stop == False :
        if counter % 10 == 0 and counter != 0:
            user_points += 1
            user_stops += 1
        elif counter != 0 :
            user_stops += 1
    stop = True
    clockwatch.stop()

def reset():
    global counter, user_stops, user_points
    stop = True
    counter = 0
    user_stops = 0
    user_points = 0
    clockwatch.stop()
    
def timer():
    global counter
    counter += 1

def draw(canvas):
    text = format(counter)
    canvas.draw_text(text, (65, 130), 50, "orange")
    canvas.draw_text(str(user_points) + '/' + str(user_stops), (190,30), 20, "white")
    
#4. Create Frame
frame = simplegui.create_frame("The Stopwatch Game", width, height)
frame.set_canvas_background('blue')

#5. Register event handlers

clockwatch = simplegui.create_timer(interval, timer)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.set_draw_handler(draw)

#6. Start Frame
frame.start()