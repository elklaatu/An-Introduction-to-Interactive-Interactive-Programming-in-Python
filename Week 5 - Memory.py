#IMPLEMENTATION OF THE GAME MEMORY

#1. Import libraries
import simplegui
import random

click1 = 0
click2 = 0

#2. Helper functions to initialize globals
def new_game():
    global cards, exposed, turns, state
    state = 0
    turns = 0
    cards = [i%8 for i in range(16)]
    exposed = [False for i in range(16)]
    
    random.shuffle(cards)
    label.set_text("Turns = " + str(turns))
    
#3. Define event handlers
def mouseclick(pos):
    # 3.1 Game logic
    global state, exposed, click1, click2, turns, cards
    player_pick = int(pos[0] / 50)
    if state == 0:
        state = 1
        click1 = player_pick
        exposed[click1] = True
    elif state == 1:
        if not exposed[player_pick]:
            state = 2
            click2 = player_pick
            exposed[click2] = True
            turns += 1
    elif state == 2:
        if not exposed[player_pick]:
            if cards[click1] == cards[click2]:
                pass
            else:
                exposed[click1] = False
                exposed[click2] = False
            click1 = player_pick
            exposed[click1] = True
            state = 1       
    label.set_text("Turns = " + str(turns))
    pass
    
#3.2 Draw cards logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(cards[i]), (50*i+10, 60), 40, "White")
        else:
             canvas.draw_polygon([(50*i, 0), (50*i, 100)], 6, "Blue")
    pass

#4. Create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

#5. Register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# 6. Start functions and frame
new_game()
frame.start()