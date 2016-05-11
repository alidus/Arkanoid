import pygame, os
from random import *
from time import *
from pygame.locals import *
from math import *
from map_editor import *
import ctypes, fade_in_out
user32 = ctypes.windll.user32
you_died = False
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
FPS = 60
ball_max_speed = 10
music = True
debug = False
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
DisplaySurface = pygame.display.set_mode(screen_size, FULLSCREEN)
pygame.display.set_caption("arcanoid")
ProgramExit = False
white = (255,255,255)
black = (0,0,0)
game_speed = [1,1]
max_game_speed = 1.25
info_text_size = 20


class Button:
    def __init__(self, button_box, text, bg, text_colour):
        self.button_box = button_box
        self.x = self.button_box[0]
        self.y = self.button_box[1]
        self.width = self.button_box[2]
        self.height = self.button_box[3]
        self.text = text
        self.bg = bg
        self.text_colour = text_colour


    def draw(self, surface, alpha):
        button_box = pygame.Surface((self.width, self.height))
        button_box.set_alpha(alpha)
        if isinstance(self.bg, tuple):
            button_box.fill(self.bg)
        else:
            button_box.blit(self.bg, (0, 0))
        surface.blit(button_box, (self.x, self.y))
        message(self.text, self.x + self.width / 2, self.y + self.height / 2, self.text_colour,
                     False, (0,0,0,0), True, round(self.height * 0.6))


def pressed_illusion(button_box, end_time):
    if pygame.time.get_ticks() <= end_time:
        illusion_rect = Rect((button_box[0], button_box[1]), (button_box[2], button_box[3]))
        illusion_surface = pygame.Surface((illusion_rect.width, illusion_rect.height))
        illusion_surface.fill((255, 255, 255))
        illusion_surface.set_alpha(100)
        DisplaySurface.blit(illusion_surface, illusion_rect)


def message(msg, x, y, colour, bg = False, background_color = (0, 0, 0, 0), centered=False, size=30):
    font = pygame.font.Font("res\\FreeSansBold.ttf", size)
    if bg:
        screen_text = font.render(msg, True, colour, background_color)
    else:
        screen_text = font.render(msg, True, colour)
    text_rect = screen_text.get_rect()
    if centered:
        text_rect.centerx = x
        text_rect.centery = y
    else:
        text_rect.x = x
        text_rect.y = y
    DisplaySurface.blit(screen_text, text_rect)

def setup_def_barnball():
    global barconf, ballconf
    barconf = [(screen_size[0]-100)/2,          #0 X
               screen_size[1] - 30 - 10,        #1 Y
               180,                             #2 Width
               20,                              #3 Hight
               15,                              #4 Speed
               white,                           #5 Color
               10,                              #6 Hitpower
               0.7]                             #7 Speedpower
    ballconf = [barconf[0]+barconf[2]/2,        #0 X
               barconf[1]-barconf[3]*10,         #1 Y
               25,                            #2 Size
               randint(-5,5),                   #3 X_speed
               8]                               #4 Y_speed
def data_initialization():
    global musiclist, blocklist, background, blandwa_hits, bar_hits, balllightlist, bar_image,  ball_image, you_died_image, ball_light,\
        barskins, ballskins, backgroundlist, you_died_sound, b_hit_mixer_sound, theme, bar_hit_mixer_sound, map_list,\
        you_win_image, ending_alpha_change, you_win_sound, message_map_color, maps_directory, bg_blinking, menu_music, main_menu_background
    musiclist, blocklist, barskins, ballskins, backgroundlist, balllightlist, blandwa_hits, bar_hits, map_list = [], [], [], [], [], [], [], [], []
    for file in os.listdir('res\\'+theme+'\\pics\\balls\\'):
        ballskins.append('res\\'+theme+'\\pics\\balls\\'+str(file))
    for file in os.listdir('res\\'+theme+'\\pics\\bars\\'):
        barskins.append('res\\'+theme+'\\pics\\bars\\'+str(file))
    for file in os.listdir('res\\'+theme+'\\pics\\balls_lightning\\'):
        balllightlist.append('res\\'+theme+'\\pics\\balls_lightning\\'+str(file))
    for file in os.listdir('res\\'+theme+'\pics\\blocks\\'):
        blocklist.append(pygame.image.load('res\\'+theme+'\pics\\blocks\\'+str(file)).convert())
    for file in os.listdir('res\\'+theme+'\\sounds\music\\'):
        musiclist.append('res\\'+theme+'\\sounds\music\\'+str(file))
    for file in os.listdir('res\\'+theme+'\\pics\\backgrounds\\'):
        backgroundlist.append('res\\'+theme+'\\pics\\backgrounds\\'+str(file))
    for file in os.listdir('res\\' + theme + '\\sounds\\blandwa_hit\\'):
        blandwa_hits.append('res\\' + theme + '\\sounds\\blandwa_hit\\' + str(file))
    for file in os.listdir('res\\' + theme + '\\sounds\\bar_hit\\'):
        bar_hits.append('res\\' + theme + '\\sounds\\bar_hit\\' + str(file))
    for map_name in os.listdir('maps\\'):
        map_list.append('maps\\' + str(map_name))
    bar_image = pygame.transform.scale(pygame.image.load(choice(barskins)), (barconf[2],barconf[3])).convert()
    ball_image = pygame.transform.scale(pygame.image.load(choice(ballskins)), (ballconf[2],ballconf[2])).convert_alpha()
    background = pygame.transform.scale(pygame.image.load(choice(backgroundlist)), (screen_size[0], screen_size[1])).convert()
    ball_light = pygame.transform.scale(pygame.image.load(choice(balllightlist)), (ballconf[2]*2,ballconf[2]*2)).convert_alpha()
    you_died_sound = 'res\\'+theme+'\sounds\you_died.mp3'
    you_win_sound = 'res\\'+theme+'\sounds\you_win.mp3'
    you_died_image = pygame.transform.scale(pygame.image.load('res\\'+theme+'\pics\you_died.png'),(screen_size[0], screen_size[1])).convert()
    you_win_image = pygame.transform.scale(pygame.image.load('res\\'+theme+'\\pics\win\\victory.png'),(screen_size[0], screen_size[1])).convert()
    main_menu_background = pygame.transform.scale(pygame.image.load('res\main_menu_bg.jpg'), (screen_size[0], screen_size[1])).convert()
    config_data = parse_config(open('res\\' + theme + '\config.txt', 'r'))
    menu_music = 'res\menu_music.mp3'
    maps_directory = 'maps\\'
    ending_alpha_change = config_data[0]
    message_map_color_raw = config_data[1]
    message_map_color = tuple(parse_color_from_string(message_map_color_raw))
    bg_blinking = int(config_data[2])
    print('Data iniciallised')
button_state = 0 # 0 - both up, 1 - left pressed, 2 - right pressed, 3 - left pressed after right, 4 - right pressed after left

def parse_color_from_string(str):
    color = []
    color.append(str[1:str.find(',')])
    new_str = str[len(color[0])+2:]
    color.append(new_str[:new_str.find(',')])
    new_str = new_str[len(color[1])+1:]
    color.append(new_str[:new_str.find(')')])
    for element in range(len(color)):
        color[element] = int(color[element])
    return color

def parse_config(file):
    config_data = []
    for line in file:
            config_data.append(line[line.find('=')+1:])
    return tuple(config_data)

def bar_ball_hit_logic(diff):
    if -1 <= diff <= 1:

        ballconf[4] /= game_speed[0]
        ballconf[4] = -ballconf[4] * game_speed[1]
        game_speed[0] = game_speed[1]
        new_ball_x_speed = ballconf[3] - barconf[6]*diff + barconf[4]*barconf[7]
        if new_ball_x_speed < -ball_max_speed*game_speed[1]:
            ballconf[3] = -ball_max_speed * game_speed[1]
        elif new_ball_x_speed > ball_max_speed*game_speed[1]:
            ballconf[3] = ball_max_speed * game_speed[1]
        else:
            ballconf[3]= new_ball_x_speed * game_speed[1]
        return 0
    else:
        return 1
def ball_logic():
    global ProgramExit, you_died
    right_wall_x = screen_size[0]-ballconf[2]
    if ballconf[0]>=right_wall_x:
        pygame.mixer.Sound(choice(blandwa_hits)).play()
        ballconf[3] = -ballconf[3]
        ballconf[0] = right_wall_x
    elif ballconf[0] < 0:
        pygame.mixer.Sound(choice(blandwa_hits)).play()
        ballconf[3] = -ballconf[3]
        ballconf[0] = 1
    if ballconf[1] < 0:
        pygame.mixer.Sound(choice(blandwa_hits)).play()
        ballconf[4] = -ballconf[4]
        ballconf[1] = 1
    if barconf[1] <= ballconf[1]+ballconf[2] <= barconf[1]+ballconf[4]:
        diff = -((ballconf[0]+ballconf[2]/2) - (barconf[0]+barconf[2]/2))/((barconf[2]+ballconf[2])/2*1.1)
        if bar_ball_hit_logic(diff):
            you_died = True
        else:
            pygame.mixer.Sound(choice(bar_hits)).play()

    ballconf[0] += ballconf[3]
    ballconf[1] += ballconf[4]


def quit_logic(event):
    global ProgramExit
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        ProgramExit = True


class ButtonBoxes:
    def __init__(self):
        self.space_between_buttons = screen_size[1] / 10
        self.exit_button_box = (screen_size[0] - screen_size[0] / 15, screen_size[1] - screen_size[1] / 10,
                                screen_size[0] / 20, screen_size[0] / 25, 'exit')
        self.start_game_box = (screen_size[0]/2 - screen_size[0] / 10, screen_size[1]/2 - self.space_between_buttons,
                               screen_size[0] / 5, screen_size[0] / 25, 'start_game')
        self.theme_choose_box = (screen_size[0] / 2 - screen_size[0] / 10, screen_size[1] / 2,
                                 screen_size[0] / 5, screen_size[0] / 25, 'change_theme')
        self.map_editor_button = (screen_size[0] / 2 - screen_size[0] / 10, screen_size[1] - screen_size[1] / 10,
                                  screen_size[0] / 5, screen_size[0] / 25, 'map_editor')
        self.change_map_button = (screen_size[0] / 2 - screen_size[0] / 10, screen_size[1] / 2 + self.space_between_buttons,
                                 screen_size[0] / 5, screen_size[0] / 25, 'change_map')
        self.boxes_list = (self.exit_button_box, self.start_game_box, self.theme_choose_box, self.map_editor_button,
                           self.change_map_button)

    def tap_check(self, event, button_boxes_list):
        global menu_active, theme_number, theme, ProgramExit, current_map_number, map_name, game_map
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos_x = event.pos[0]
            pos_y = event.pos[1]
            for box in self.boxes_list:      # Проверка на нажатие кнопки и выполенине соответствующего кнопке действия
                if box[0] <= pos_x <= box[0] + box[2] and box[1] <= pos_y <= box[1] + box[3]:
                    if box[4] == 'exit':
                        ProgramExit = True
                        return button_boxes_list[0]
                    elif box[4] == 'start_game':
                        DisplaySurface.fill((0, 0, 0))
                        message('Loading', screen_size[0]/2, screen_size[1]/2, (255, 255, 255), centered=True)
                        pygame.display.update()
                        menu_active = False
                        data_initialization()
                        return button_boxes_list[1]
                    elif box[4] == 'change_theme':
                        if theme_number < len(list_of_themes)-1:
                            theme_number += 1
                        else:
                            theme_number = 0
                        theme = list_of_themes[theme_number]
                        current_map_number = 0
                        map_name = "Randomed map"
                        return button_boxes_list[2]
                    elif box[4] == 'map_editor':
                        map_editor = MapEditor(screen_size, DisplaySurface, debug)
                        DisplaySurface.fill((0, 0, 0))
                        message('Loading', screen_size[0] / 2, screen_size[1] / 2, (255, 255, 255))
                        pygame.display.update()
                        data_initialization()
                        determine_map_list_for_current_theme()
                        return button_boxes_list[3]
                    elif box[4] == 'change_map':
                        determine_map_list_for_current_theme()
                        number_of_maps = len(current_theme_map_list)
                        if current_map_number < number_of_maps:
                            current_map_number += 1
                        else:
                            current_map_number = 0
                        if current_map_number == 0:
                            map_name = "Randomed map"
                        else:
                            theme_name_len = len(list_of_themes[theme_number])
                            map_name = str(current_theme_map_list[current_map_number-1])[5:-theme_name_len-5]
                        return button_boxes_list[4]


def determine_map_list_for_current_theme():
    global current_theme_map_list
    current_theme_map_list.clear()
    for game_map in map_list:
        h_map = game_map[game_map.index('.') + 1:]
        map_theme = h_map[:h_map.index('.')]
        if map_theme == list_of_themes[theme_number]:
            current_theme_map_list.append(game_map)



class MainMenu:
    def __init__(self, background):
        global menu_active, map_name, current_map_number
        if current_map_number == 0:
            map_name = "Randomed map"
        if music:
            pygame.mixer.music.load(menu_music)
            pygame.mixer.music.play()

        self.button_boxes = ButtonBoxes()
        self.background = background
        if isinstance(self.background, tuple):
            self.bg_type = 'colour'
        else:
            self.bg_type = 'image'
        menu_active = True
        self.button_colour = (150, 150, 150)
        self.button_text_colour = (0, 0, 0)
        self.main_buttons_skin = pygame.transform.scale(pygame.image.load('res\head_button.jpg'),
                                            (round(self.button_boxes.start_game_box[2]), round(self.button_boxes.start_game_box[3]))).convert()
        self.choise_buttons_skin = pygame.transform.scale(pygame.image.load('res\choise_button.jpg'),
                                                        (round(self.button_boxes.start_game_box[2]),
                                                         round(self.button_boxes.start_game_box[3]))).convert()
        self.exit_buttons_skin = pygame.transform.scale(pygame.image.load('res\exit_button.jpg'),
                                                   (round(self.button_boxes.exit_button_box[2]),
                                                    round(self.button_boxes.exit_button_box[3]))).convert()
        self.exit_button = Button(self.button_boxes.exit_button_box, 'Exit', self.exit_buttons_skin, self.button_text_colour)
        self.change_map_button = Button(self.button_boxes.change_map_button, map_name, self.choise_buttons_skin, (200, 200, 200))
        self.start_game_button = Button(self.button_boxes.start_game_box, 'Start game', self.main_buttons_skin, self.button_text_colour)
        self.theme_choose_button = Button(self.button_boxes.theme_choose_box, theme, self.choise_buttons_skin, (200, 200, 200))
        self.map_editor_button = Button(self.button_boxes.map_editor_button, 'Map editor', self.main_buttons_skin, self.button_text_colour)
        self.buttons_list = (self.exit_button, self.start_game_button, self.theme_choose_button, self.map_editor_button)
        self.active_press_animation = None
        self.button_press_time = 50
        self.pressed_box = None


    def draw(self):
        FadeInOut_object.start_fade_in()
        while menu_active and not ProgramExit:
            if self.bg_type == 'colour':
                DisplaySurface.fill(self.background)
            else:
                DisplaySurface.blit(self.background, (0, 0))
            for event in pygame.event.get():
                quit_logic(event)
                self.pressed_box = self.button_boxes.tap_check(event, self.button_boxes.boxes_list)
                if self.pressed_box == self.button_boxes.boxes_list[1]:
                    self.pressed_box = None
            self.theme_choose_button = Button(self.button_boxes.theme_choose_box, theme, self.choise_buttons_skin,
                                              (200, 200, 200))
            self.change_map_button = Button(self.button_boxes.change_map_button, map_name, self.choise_buttons_skin,
                                              (200, 200, 200))
            self.exit_button.draw(DisplaySurface, 255)
            self.start_game_button.draw(DisplaySurface, 255)
            self.change_map_button.draw(DisplaySurface, 255)
            self.theme_choose_button.draw(DisplaySurface, 255)
            self.map_editor_button.draw(DisplaySurface, 255)
            message('Theme:', self.theme_choose_button.x, self.theme_choose_button.y, (255, 255, 255),bg=True, size=19)
            message('Map:', self.change_map_button.x, self.change_map_button.y, (255, 255, 255),bg=True, size=19)
            if self.pressed_box != None:
                self.active_press_animation = self.pressed_box
                self.time_of_unpressed = pygame.time.get_ticks() + self.button_press_time
            if self.active_press_animation != None:
                pressed_illusion(self.active_press_animation, self.time_of_unpressed)
            pygame.display.update()


def bar_logic():
    global button_state
    if button_state in (1,3):
        barconf[4] = -15*game_speed[1]
    elif button_state in (2,4):
        barconf[4] = 15*game_speed[1]
    else:
        barconf[4] = 0
    barconf[0] += barconf[4]
    if barconf[0] < 0:
        barconf[0] = 1
    elif barconf[0] > screen_size[0]-barconf[2]:
        barconf[0] = screen_size[0]-barconf[2]


def det_button_state(event):
    global button_state
    if event.type == pygame.KEYDOWN:
        if button_state == 0:
            if event.key == pygame.K_LEFT:
                button_state = 1
            elif event.key == pygame.K_RIGHT:
                button_state = 2
        elif button_state == 1 and event.key == pygame.K_RIGHT:
            button_state = 4
        elif button_state == 2 and event.key == pygame.K_LEFT:
            button_state = 3

    elif event.type == pygame.KEYUP:
        if button_state in (1,2):
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                button_state = 0
        elif button_state in (3,4):
            if event.key == pygame.K_LEFT:
                button_state = 2
            if event.key == pygame.K_RIGHT:
                button_state = 1

error = 0.1

def check_for_break(health):
    if health == 0:
        return False
    else:
        return True

horiz_vector = (1,0)
deb_vec_len = 1000
FadeInOut_object = fade_in_out.FadeInOut(DisplaySurface)

def block_collision(x,y,w,h,help):
    global angle_ball_block, angle_ball_horiz
    sl = 0
    right = ballconf[0]+ballconf[2]
    bot = ballconf[1]+ballconf[2]
    top = ballconf[1]
    left = ballconf[0]
    center = (ballconf[0]+ballconf[2]/2, ballconf[1]+ballconf[2]/2)
    vector_ball = (ballconf[3], ballconf[4])
    angle_ball_horiz = acos(vector_ball[0]/(sqrt(vector_ball[0]**2+vector_ball[1]**2)))*180/pi
    vector_block_center = (x+w/2-(center[0]), y+h/2-center[1])
    if debug:
        line = pygame.draw.line(DisplaySurface, (255,0,0), (center[0], center[1]), ((center[0]+vector_ball[0]*deb_vec_len), (center[1]+vector_ball[1]*deb_vec_len)))
    angle_ball_block = acos((vector_ball[0]*vector_block_center[0]+vector_ball[1]*vector_block_center[1])/((sqrt(vector_ball[0]**2+vector_ball[1]**2))*(sqrt(vector_block_center[0]**2+vector_block_center[1]**2))))*180/pi
    if game_map[help][0]:
        if x < right and x+w >= left and y+h - abs(ballconf[4]) <= top <= y+h <= bot:
            pygame.mixer.Sound(choice(blandwa_hits)).play()
            game_map[help][6] -= 1
            game_map[help][0] = check_for_break(game_map[help][6])
            sleep(sl)
            return 1
        elif x < right and x+w >= left and top <= y <= bot <= y + abs(ballconf[4]):
            pygame.mixer.Sound(choice(blandwa_hits)).play()
            game_map[help][6] -= 1
            game_map[help][0] = check_for_break(game_map[help][6])
            sleep(sl)
            return 2
        elif x + abs(ballconf[3]) >= right >= x  and bot >= y and top <= y+h:
            pygame.mixer.Sound(choice(blandwa_hits)).play()
            game_map[help][6] -= 1
            game_map[help][0] = check_for_break(game_map[help][6])
            sleep(sl)
            return 3
        elif x+w - abs(ballconf[3]) <= left <= x+w and bot >= y and top <= y+h:
            pygame.mixer.Sound(choice(blandwa_hits)).play()
            game_map[help][6] -= 1
            game_map[help][0] = check_for_break(game_map[help][6])
            sleep(sl)
            return 4
        else:
            return 0
    else:
        return 0

you_win = False



first_block_init = True

def basic_map():
    global game_map
    game_map = []
    block_rows = 15
    block_columns = 20
    w, h = 40, 25
    height_of_box = screen_size[1]/2
    horizontal_space = (screen_size[0]-w*block_columns)/(block_columns+1)
    vertical_space = (height_of_box-h*block_rows)/(block_rows+1)
    for row in range(block_rows):
        for col in range(block_columns):
            block_x = horizontal_space*(col+1)+w*col
            block_y = vertical_space*(row+1)+h*row
            bol = bool(getrandbits(1))
            skin_number = randint(0, len(blocklist)-1)
            game_map.append([bol,block_x,block_y, w, h, skin_number, 1, 1])
    return game_map
def random_color():
    return (randint(0,255),randint(0,255),randint(0,255))


def load_map():
    if current_map_number > 0:
        return convert_map_string_to_list(open(current_theme_map_list[current_map_number-1]).read())
    else:
        return basic_map()


def convert_map_string_to_list(string_map):
    converted_map = []
    string_map = string_map[1:]
    while len(string_map) > 0:
        result = convert_block(string_map)
        converted_map.append(result[0])
        string_map = result[1]
    return converted_map
def convert_block(string_map):
    block = []
    if string_map[1:5] == 'True':
        block.append(True)
    else:
        block.append(False)
    string_map = string_map[7:]
    for i in range(6):
        block.append(int(string_map[:string_map.index(',')]))
        string_map = string_map[string_map.index(',')+2:]
    block.append(int(string_map[:string_map.index(']')]))
    string_map = string_map[string_map.index(']') + 3:]

    return (block, string_map)



def bonus_double_speed():
    pass
first_ir = True
alive_blocks = 0

def establish_skins_for_every_block(game_map):
    for block in game_map:
        block[5] = pygame.transform.scale(blocklist[block[5]], (block[3], block[4]))
    return game_map

def blocks_init_and_drawing():
    global first_ir, alive_blocks, game_speed, blocks_left
    if first_ir:
        alive_blocks = 0
        for block in game_map:
            if block[0] == True:
                alive_blocks += 1
        first_ir = False
    blocks_left = 0
    coll_list = []
    help = 0
    ball_coords = (ballconf[0]+ballconf[2], ballconf[1]+ballconf[2])
    for block in game_map:
            block_x = block[1]
            block_y = block[2]
            w = block[3]
            h = block[4]
            block_coords = (block_x+w/2, block_y+h/2)
            skin = block[5]
            skin.set_alpha(255*(block[6]/block[7]))
            if sqrt((block_coords[0]-ball_coords[0])**2+(block_coords[1]-ball_coords[1])**2) <= max(w,h)*2:
                stat = block_collision(block_x, block_y, w, h, help)
            else:
                stat = 0
            if stat > 0:
                coll_list.append(stat)
                if debug:
                    pygame.draw.rect(DisplaySurface, (255,25,25), pygame.Rect((block_x, block_y), (w, h)))
                    if stat == 1:
                        pygame.draw.line(DisplaySurface, (25,255,25), (block_x, block_y+h), (block_x+w, block_y+h), 5)
                    elif stat == 2:
                        pygame.draw.line(DisplaySurface, (25, 255, 25), (block_x, block_y), (block_x + w, block_y), 5)
                    elif stat == 3:
                        pygame.draw.line(DisplaySurface, (25, 255, 25), (block_x, block_y), (block_x, block_y+h), 5)
                    elif stat == 4:
                        pygame.draw.line(DisplaySurface, (25, 255, 25), (block_x+w, block_y), (block_x + w, block_y+h), 5)
                    pygame.display.update()
            if game_map[help][0]:
                blocks_left += 1
                r = Rect((block_x,block_y),(w,h))
                DisplaySurface.blit(skin, r)
            help += 1
    if blocks_left > 0:
        if game_speed[1] < max_game_speed:
            game_speed[1] = 1/sqrt((blocks_left/alive_blocks))
        else:
            game_speed[1] = max_game_speed
    if len(coll_list) > 1:
        if coll_list[0] == coll_list[1]:
            if coll_list[0] in (1,2):
                ballconf[4] *= -1
            elif coll_list[0] in (3,4):
                ballconf[3] *= -1
        else:
            for collis in coll_list:
                if collis in (1,2):
                    ballconf[4] *= -1
                elif collis in (3,4):
                    ballconf[3] *= -1
    elif len(coll_list) == 1:
        if coll_list[0] in (1,2):
                ballconf[4] *= -1
        elif coll_list[0] in (3,4):
            ballconf[3] *= -1
    return blocks_left

def debug_pause():
    print('Debug pausing')
    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                cont = False

def drawing():
    global bar_image, ball_image
    ball = Rect((ballconf[0],ballconf[1]),(ballconf[2],ballconf[2]))
    bar = Rect((barconf[0],barconf[1]),(barconf[2], barconf[3]))
    bar_line = pygame.Surface((screen_size[0],4))
    bar_line.fill((30,30,30))
    DisplaySurface.blit(ball_light, ball.inflate(ballconf[2],ballconf[2]))
    DisplaySurface.blit(bar_line,(0,barconf[1]+barconf[3]/2-2))
    DisplaySurface.blit(bar_image, bar)
    DisplaySurface.blit(ball_image, ball)


main_first = True
menu_active = True


def main_loop():
    global main_first, bg_alpha, bg_bool, bg_alpha_range, you_win, game_speed, menu_active, you_died, game_map
    if menu_active:
        main_menu = MainMenu(main_menu_background)
        main_menu.draw()
    if main_first:
        if music:
            pygame.mixer.music.load(choice(musiclist))
            pygame.mixer.music.play()
        main_first = False
        game_map = establish_skins_for_every_block(load_map())
        game_speed = [1, 1]
    background.set_alpha(bg_alpha)
    DisplaySurface.fill(black)
    DisplaySurface.blit(background, (0, 0))
    if bg_blinking == 1:
        if bg_bool:
            bg_alpha += 1
        else:
            bg_alpha -= 1
        if bg_alpha == bg_alpha_range[1]:
            bg_bool = False
        if bg_alpha == bg_alpha_range[0]:
            bg_bool = True

    for event in pygame.event.get():
        det_button_state(event)
        if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
            you_died = True
    bar_logic()
    ball_logic()
    drawing()
    blocks_left = blocks_init_and_drawing()
    if debug:
        message('Angles: Horiz: %f Block: %f' % (angle_ball_horiz, angle_ball_block), 20, barconf[1] - 150, message_map_color, size=info_text_size)
        message('Game speed: %d' % (round(game_speed[0]*100)), 20, barconf[1] -120, message_map_color, size=info_text_size)
        message('Theme: %s' % (theme), 20, barconf[1] - 90, message_map_color, size=info_text_size)
    message('game_map: %s' % (map_name), 20, barconf[1] - 60, message_map_color, size=info_text_size)
    message('Blocks left: %d' % (blocks_left), 20, barconf[1] - 30, message_map_color, size=info_text_size)
    if blocks_left == 0:
        you_win = True
    pygame.display.update()
    clock.tick(FPS)

first_iteration = True
setup_def_barnball()


list_of_themes = []
for theme in os.listdir('res'):
    if os.path.isdir('res\\'+ str(theme)):
        list_of_themes.append(theme)


current_theme_map_list = []
current_map_number = 0
theme_number = 0
theme = list_of_themes[theme_number]
data_initialization()

if bg_blinking == 1:
    bg_alpha_range = (80, 255)
    bg_alpha = bg_alpha_range[0]
    bg_bool = True
else:
    bg_alpha = 255

while not ProgramExit:
    if not you_died and not you_win:        # Основной сценарий игры
        main_loop()
        first_iteration = True
    else:
        if you_died:                         # Пользователь проиграл
            if first_iteration:
                pygame.mixer.music.load(you_died_sound)
                pygame.mixer.music.play()
                first_iteration = False
            you_died_image.set_alpha(4)
            DisplaySurface.blit(you_died_image, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:           # Пользователь проиграл и нажал Space
                        you_died = False
                        first_ir = True
                        setup_def_barnball()
                        button_state = 0
                        main_first = True
                        pygame.mixer.music.stop()
                    elif event.key == pygame.K_ESCAPE:           # Пользователь проиграл и нажал Escape
                        you_died = False
                        first_ir = True
                        setup_def_barnball()
                        button_state = 0
                        main_first = True
                        pygame.mixer.music.stop()
                        menu_active = True
                if event.type == pygame.QUIT:
                    ProgramExit = True
            clock.tick(FPS/2)
        else:                                                        # Пользователь проиграл
            if first_iteration:
                pygame.mixer.music.load(you_win_sound)
                pygame.mixer.music.play()
                first_iteration = False
                sleep(0.5)
            if ending_alpha_change == 1:
                you_win_image.set_alpha(4)
            DisplaySurface.blit(you_win_image,(0,0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:                # Пользователь выиграл и нажал Space
                        you_win = False
                        first_ir = True
                        setup_def_barnball()
                        button_state = 0
                        main_first = True
                        pygame.mixer.music.stop()
                    elif event.key == pygame.K_ESCAPE:             # Пользователь выиграл и нажал Escape
                        you_win = False
                        first_ir = True
                        setup_def_barnball()
                        button_state = 0
                        main_first = True
                        pygame.mixer.music.stop()
                        menu_active = True
                if event.type == pygame.QUIT:
                    ProgramExit = True
            clock.tick(FPS/2)