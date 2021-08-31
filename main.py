import pygame
import speech_recognition as sr

from speech import recognize_speech_from_mic

recognizer = sr.Recognizer()
mic = sr.Microphone()
recognizer.energy_threshold = 310
recognizer.dynamic_energy_threshold = False

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 32)
screen_width = 640 + 150
screen_height = 512 + 40
sprite_size = 128

white = (255, 255, 255)
green = (0, 255, 0)
dark_green = (100, 120, 0)
teal = (50, 120, 75)

voice_input = "You said : "
 
# create a text surface object,
# on which text is drawn on it.
text = font.render('Help the mouse', True, dark_green, white)
text2 = font.render('reach the pizza.', True, dark_green, white)

winning_text = font.render('You Won', True, green, white)
input_text = font.render('What is the', True, teal, white)
input_text2 = font.render('next number?', True, teal, white)

# create a rectangular object for the
# text surface object
textRect = text.get_rect()
textRect2 = text2.get_rect()
winningTextRect = winning_text.get_rect()
inputTextRect = input_text.get_rect()
inputTextRect2 = input_text2.get_rect()


textRect.center = (650, 30)
textRect2.center = (650, 65)
winningTextRect.center = (650, 300)
inputTextRect.center = (650, 300)
inputTextRect2.center = (650, 335)

win = False
show_input = True
show_you_said = False

button_position = (screen_width-210,(screen_height/2)-(sprite_size/2)-90)
# print(button_position)

screen = pygame.display.set_mode((screen_width,screen_height))

maze2D = [["W"]*4 for i in range(4)]
maze2D[0][0] = "M"
maze2D[3][3] = "E"
maze2D_X = 0
maze2D_Y = 0

running = True

#Title and Icon
pygame.display.set_caption("Counting")
icon = pygame.image.load('assests/icons/mouse.png')
pygame.display.set_icon(icon)

#mice
miceImg = pygame.image.load('assests/sprites/mouse.png')
miceX = 0
miceY = 0

oneImg = pygame.image.load('assests/sprites/1.png')
twoImg = pygame.image.load('assests/sprites/2.png')
threeImg = pygame.image.load('assests/sprites/3.png')
fourImg = pygame.image.load('assests/sprites/4.png')
fiveImg = pygame.image.load('assests/sprites/5.png')

startImg = pygame.image.load('assests/sprites/start.png')
pizzaImg = pygame.image.load('assests/sprites/pizza.png')
waterImg = pygame.image.load('assests/sprites/water.png')

buttonBlue = pygame.image.load('assests/sprites/buttonBlue.png')
buttonGreen = pygame.image.load('assests/sprites/buttonGreen.png') 
buttonImg = buttonBlue

def mice():
    screen.blit(miceImg,(miceX,miceY))

def draw_grid():
    for i in range(0,screen_height):
        if i % 128 == 0:
            pygame.draw.line(screen,(0,0,0),(0,i),(screen_height,i),2)
    
    for i in range(0,screen_width):
        if i % 128 == 0:
            pygame.draw.line(screen,(0,0,0),(i,0),(i,screen_width),2)

numbers = {'1':["down",None,None],'2':["right",None,None],'3':["down",None,None],'4':["right",None,None],'5':["down",None,None]}
current_number = '1'

def get_img(number):
    if number=='1':
        return oneImg
    if number=='2':
        return twoImg
    if number=='3':
        return threeImg
    if number=='4':
        return fourImg
    if number=='5':
        return fiveImg

def get_Pos(number,direction,start_X,start_Y):
    global maze2D_Y
    global maze2D_X
    if direction == "down": 
        maze2D_X = maze2D_X + 1
        if maze2D[maze2D_X][maze2D_Y] != 'M':
            maze2D[maze2D_X][maze2D_Y] = number
        numbers[number][1] = maze2D_X
        numbers[number][2] = maze2D_Y
        return (start_X,start_Y+128)
    if direction == "right":
        maze2D_Y = maze2D_Y + 1
        if maze2D[maze2D_X][maze2D_Y] != 'M':
            maze2D[maze2D_X][maze2D_Y] = number
        numbers[number][1] = maze2D_X
        numbers[number][2] = maze2D_Y
        return(start_X+128,start_Y)


def draw_maze():
    start_X = 0
    start_Y = 0
    global maze2D_Y
    global maze2D_X
    for key in numbers:
        if key != 'eat':
            img = get_img(key)
            pos = get_Pos(key,numbers[key][0],start_X,start_Y)
            start_X = pos[0]
            start_Y = pos[1]
            screen.blit(img,pos)
    maze2D_X =0
    maze2D_Y =0
    for x in range(0,4):
        for y in range(0,4):
            if maze2D[x][y] == "W":
                screen.blit(waterImg,(y*128,x*128))
    # print(maze2D)
    screen.blit(pizzaImg,(384,384))
    numbers['eat']=["right",3,3]

def draw_start():
    screen.blit(startImg,(0,0))

def draw_button():
    screen.blit(buttonImg,button_position)

def convert_transcription(transcription):
    global show_you_said
    if transcription != None:
        if transcription.lower() == 'when' or transcription.lower() == 'vadh' or transcription.lower() == 'van':
            return str(1)
        if transcription.lower() == 'tu':
            return str(2)
        if transcription.lower() == 'iit' or transcription.lower() == 'it':
            return 'eat'
        if transcription.lower() == 'free':
            return str(3)
        if transcription.lower() == 'pipe':
            return str(5)        
        else:
            return transcription
    else:
        show_you_said = False
        print('Could not hear you properly, please speak again')


def update_mouse_position():
    global miceX
    global miceY
    global current_number
    global win
    global show_input
    global buttonImg
    global buttonBlue
    global show_you_said
    global voice_input
    response = recognize_speech_from_mic(recognizer,mic);
    if response['success'] == True:
        transcription = convert_transcription(response['transcription']);
        if transcription!=None:
            if len(transcription) != 0:
                show_you_said = True
                voice_input = voice_input[0:11]+transcription
        # print(transcription)
        if current_number == transcription:
            if(current_number) == 'eat':
                win = True
                show_input = False
            miceX = numbers[str(current_number)][2]*128
            miceY = numbers[str(current_number)][1]*128
            if current_number != 'eat':
                if int(current_number) < 5:
                    current_number = str((int(current_number)+1))
                else:
                    current_number = 'eat'
    if response['success'] == False:
        show_you_said = False
        print(response['error'])
    mice()
    buttonImg = buttonBlue

def update_display():
    global voice_input
    you_said_text = font.render(voice_input,True,teal,white)
    youSaidRect = you_said_text.get_rect()
    youSaidRect.center = (650, 420)
    screen.fill((255,255,255))
    draw_start()
    draw_maze()
    mice()    
    draw_button()
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)
    if show_input:
        screen.blit(input_text, inputTextRect)
        screen.blit(input_text2, inputTextRect2)
    if win:
        screen.blit(winning_text, winningTextRect)
    if show_you_said:
        screen.blit(you_said_text, youSaidRect)
    pygame.display.update()

#Game Loop
while running:
    mouse = pygame.mouse.get_pos()
    # draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (mouse[0] > button_position[0] and mouse[0] < button_position[0]+128) and (mouse[1] > button_position[1] and mouse[1] < button_position[1]+128): 
                # print(maze2D)
                buttonImg = buttonGreen
                update_display()
                update_mouse_position()
    update_display()
    