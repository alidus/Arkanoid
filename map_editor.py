import pygame, ctypes, os, time
user32 = ctypes.windll.user32
from pygame.locals import *
from random import *
import eztext
class MapEditor:
    def __init__(self, window_sizes, surface, debug):
        global EditorExit, exit_button, colour_pack, button_states, button_boxes, list_of_themes, theme, current_theme, window_size, DisplaySurface
        window_size = window_sizes
        DisplaySurface = surface
        self.clock = pygame.time.Clock()
        current_theme, theme = 'default', 'default'
        self.vari = self.Vars()
        colour_pack = self.ColourPack()
        button_boxes = self.ButtonBoxes()
        EditorExit = False
        button_states = self.ButtonStates()
        self.start_x_pos = None
        self.start_y_pos = None
        self.end_x_pos = None
        self.end_y_pos = None
        self.map = []
        list_of_material_buttons = []
        default_background = pygame.Surface((round(window_size[0]), round(window_size[1])))
        default_background.fill(colour_pack.dark_grey)
        self.background = default_background
        self.button_alpha = 200
        self.drawing_block_active = False
        self.start_position = None
        self.end_position = None
        self.current_material = None
        material_list = self.ButtonsList([], 0, 0)
        exit_button = self.Button(button_boxes.exit_button[0], button_boxes.exit_button[1],
                                   button_boxes.exit_button[2],
                                   button_boxes.exit_button[3], "Exit", colour_pack.dark_white,
                                   colour_pack.black, "exit", button_states.exit_button)
        save_button = self.Button(button_boxes.save_map[0],button_boxes.save_map[1], button_boxes.save_map[2],
                                  button_boxes.save_map[3], "Save map", colour_pack.dark_white, colour_pack.black,
                                  'save_map', button_states.save_map_button)
        self.list_of_themes = self.init_list_of_themes(exit_button, colour_pack, button_states)
        number_of_themes = len(self.list_of_themes.list_of_buttons)
        self.button_press_time = 50
        self.debug_console = self.DebugConsole(colour_pack.white)
        self.active_press_animation = None
        self.pressed_box = None
        self.input_map_name_box = eztext.Input(x=window_size[0]*0.4, y=window_size[1]*0.95, color=colour_pack.white,
                                               prompt= 'Map name: ')
        while not EditorExit:
            DisplaySurface.blit(self.background, (0, 0))
            self.draw_map(self.map)
            self.events = pygame.event.get()
            pressed = self.event_check(button_boxes, self.events)
            if pressed == -1:
                self.pressed_box = None
                self.x_pos = None
            elif pressed == -2 and self.current_material is not None:
                self.drawing_block_active = True
            else:
                print(button_boxes.button_list)
                self.x_pos = None
                self.y_pos = None
                self.debug_console.print_message('Pressed state: ' + str(pressed))
                self.pressed_box = button_boxes.button_list[pressed]
                self.y_pos = None
            if self.drawing_block_active:
                block = self.check_if_drawing_finished(self.init_block_drawing())
                if block is not None:
                    self.map.append([True, block[0], block[1], block[2], block[3], self.current_material-1, 1, 1])
            if self.pressed_box:
                self.active_press_animation = self.pressed_box
                self.time_of_unpressed = pygame.time.get_ticks() + self.button_press_time
            if self.active_press_animation:
                self.pressed_illusion(self.active_press_animation, self.time_of_unpressed)
            if theme != current_theme:
                self.data = self.DataInit(theme)
                self.map.clear()
                list_of_material_buttons.clear()
                self.current_material = None
                for i in range(number_of_themes + 2, len(button_boxes.button_list)):
                    button_boxes.button_list.pop()
                itera = 0
                for material in self.data.blocklist:
                    button = self.Button(self.vari.material_list_x,
                                         self.vari.material_list_y + (window_size[1] / 20 + 2) * itera,
                                              window_size[0] / 10, window_size[1] / 20, "", material,
                                              colour_pack.black, 'null', False)
                    list_of_material_buttons.append(button)
                    button_boxes.button_list.append((button.x, button.y,
                                                     button.width, button.height))
                    itera += 1
                print("After adding")
                print('Number of themes: %d Number of boxes: %d' % (number_of_themes, len(button_boxes.button_list)))
                print('len of box_list: ' + str(len(button_boxes.button_list)))
                material_list = self.ButtonsList(list_of_material_buttons, self.vari.material_list_x,
                                                      self.vari.material_list_y)
                self.draw_list_of_buttons( material_list, self.button_alpha)
                current_theme = theme
                self.background = self.data.background
            if len(material_list.list_of_buttons) != 0:
                self.draw_list_of_buttons(material_list, self.button_alpha)
            self.clock.tick(self.vari.FPS)
            if not pygame.key.get_mods() & KMOD_CTRL:
                self.input_map_name_box.update(self.events)
            self.input_map_name_box.draw(DisplaySurface)
            self.draw_button(exit_button, self.button_alpha)
            self.draw_button(save_button, self.button_alpha)
            self.draw_list_of_themes(self.button_alpha, self.list_of_themes)
            self.text_message('Themes', self.list_of_themes.x + self.list_of_themes.list_of_buttons[0].width / 2,
                                   window_size[1] * 0.05, colour_pack.dark_green, 40)
            if pressed != -1:
                if pressed == 0:
                    EditorExit = True
                elif pressed == 1:
                    if current_theme == 'default':
                        self.warning('Choose theme to save map', True)
                    elif self.input_map_name_box.value == '':
                        self.warning('Enter map name', True)
                    else:
                        self.save_map_to_disk()
                elif pressed == 2:
                    theme = 'dark_souls'
                elif pressed == 3:
                    theme = "portal"
                elif pressed > 3:
                    self.current_material = pressed - 3
                    print(self.current_material)
                    self.debug_console.print_message("Current material: " + str(self.current_material))
            if self.current_material:
                self.button_glow(button_boxes.button_list[self.current_material+3])
            if debug:
                self.debug_console.draw_console()
            pygame.display.update()


    class ColourPack:
        def __init__(self):
            self.white = (255, 255, 255)
            self.black = (0, 0, 0)
            self.red = (255, 0, 0)
            self.green = (0, 255, 0)
            self.blue = (0, 0, 255)
            self.grey = (122, 122, 122)
            self.dark_grey = (50, 50, 50)
            self.dark_green = (0, 200, 0)
            self.dark_white = (200, 200, 200)


    class Vars:
        def __init__(self):
            self.FPS = 60
            self.material_list_x = window_size[0]/20
            self.material_list_y = window_size[1]/20


    class ButtonBoxes:
        def __init__(self):
            self.exit_button = (window_size[0] - window_size[0] / 15, window_size[1] - window_size[1] / 10,
                                window_size[0] / 20, window_size[0] / 25)
            self.save_map = (window_size[0] / 15, window_size[1] - window_size[1] / 10,
                                window_size[0] / 9, window_size[0] / 25)
            self.button_list = [self.exit_button, self.save_map]



    class ButtonStates:
        def __init__(self):
            self.exit_button = False
            self.save_map_button = False
            self.list_of_themes_buttons = []
            for theme in os.listdir('res'):
                if os.path.isdir('res\\'+str(theme)):
                    self.list_of_themes_buttons.append(False)

    class Button:
        def __init__(self, x, y, width, height, text, colour, text_colour, event, button_state):
            global EditorExit
            self.darker = 150
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.colour = colour
            self.event = event
            self.pressed = button_state
            self.text_colour = text_colour
        def button_click_animation(self):
            self.colour = list(self.colour)
            for i in range(3):
                self.colour[i] -= self.darker
                if self.colour[i] < 0:
                    self.colour[i] = 0
            self.colour = tuple(self.colour)


    class ButtonsList:
        def __init__(self, list_of_buttons, x, y):
            self.list_of_buttons = list_of_buttons
            self.x = x
            self.y = y

    def pressed_illusion(self, button_box, end_time):
        if pygame.time.get_ticks() <= end_time:
            pygame.draw.rect(DisplaySurface, (255, 255, 255, 0),
                             Rect((button_box[0], button_box[1]), (button_box[2], button_box[3])))

    def save_map_to_disk(self):
        map_file = open(str(self.data.maps_directory)+self.input_map_name_box.value+'.' + str(theme)+'.txt', 'w')
        map_file.write(str(self.map))
        map_file.close()
        self.input_map_name_box.value = ''
        self.debug_console.print_message('Map saved')
        self.warning('Map saved')

    def init_block_drawing(self):
        if self.start_x_pos is None:
            self.start_x_pos = pygame.mouse.get_pos()[0]
            self.start_y_pos = pygame.mouse.get_pos()[1]
        mouse_position = pygame.mouse.get_pos()
        self.end_x_pos = mouse_position[0]
        self.end_y_pos = mouse_position[1]

        model_block = Rect((self.start_x_pos, self.start_y_pos), (self.end_x_pos-self.start_x_pos, self.end_y_pos - self.start_y_pos))
        if model_block.width < 0:
            model_block.x = model_block.x + model_block.width
            model_block.width *= -1
        if model_block.height < 0:
            model_block.y = model_block.y + model_block.height
            model_block.height *= -1
        block_skin = pygame.Surface((model_block.width, model_block.height))
        block_skin.fill((0, 255, 0))
        block_skin.set_alpha(80)
        DisplaySurface.blit(block_skin, model_block)
        return model_block

    def check_if_drawing_finished(self, rectangle):
        if pygame.mouse.get_pressed()[0] == False:
            self.drawing_block_active = False
            self.start_x_pos = None
            self.start_y_pos = None
            if rectangle[2] < 0:
                rectangle[0] += rectangle[2]
                rectangle[2] *= -1
            if rectangle[3] < 0:
                rectangle[1] += rectangle[3]
                rectangle[3] *= -1
            return rectangle

    def warning(self, msg='warning_text', shaded=True):
        warning_active = True
        if shaded:
            surf = pygame.Surface((window_size[0], window_size[1]))
            surf.fill((0, 0, 0))
            surf.set_alpha(230)
            DisplaySurface.blit(surf, (0,0))
        warning_rectangle = Rect(window_size[0]*0.35, window_size[1] * 0.35,
                                 window_size[0]*0.3, window_size[1]*0.3)
        pygame.draw.rect(DisplaySurface, (200, 200, 200), warning_rectangle)
        textbox_x = window_size[0]/2
        self.text_message(msg, textbox_x, warning_rectangle.y + warning_rectangle.height/4, (20, 20, 20), 40)
        accept_button = self.Button(warning_rectangle.x+warning_rectangle.width*0.3,
                                    warning_rectangle.y + warning_rectangle.height*0.6, warning_rectangle.width*0.4,
                                    warning_rectangle.height*0.3, 'Ok', (40, 40, 40), (255, 255, 255),
                                    'warning_ok', 'Whatever')
        self.draw_button(accept_button, 255)
        pygame.display.update()
        while warning_active:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if accept_button.x <= mouse_pos[0] <= accept_button.x + accept_button.width and accept_button.y <= mouse_pos[1] <= accept_button.y + accept_button.height:
                        warning_active = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    warning_active = False


    def init_list_of_themes(self, exit_button, colour_pack, button_states):
        x = exit_button.x + exit_button.width / 2 - window_size[0] / 6
        y = window_size[1] * 0.1
        button_width = 300
        free_space = 10
        list_of_themes = self.ButtonsList([], x, y)
        iteration = 0
        for theme in os.listdir('res'):
            if os.path.isdir('res\\'+str(theme)):
                if 0 <= iteration < len(list_of_themes.list_of_buttons):
                    list_of_themes.list_of_buttons[iteration] = self.Button(x, y + (exit_button.height + free_space) * iteration,
                                                                       button_width,
                                                                       exit_button.height, theme, colour_pack.dark_green,
                                                                       colour_pack.dark_grey, 'null',
                                                                       button_states.list_of_themes_buttons[iteration])
                else:
                    list_of_themes.list_of_buttons.append(self.Button(x, y + (exit_button.height + free_space) * iteration,
                                                                 button_width,
                                                                 exit_button.height, theme, colour_pack.dark_green,
                                                                 colour_pack.dark_grey, 'null',
                                                                 button_states.list_of_themes_buttons[iteration]))

                button_boxes.button_list.append((x, y + (exit_button.height + free_space) * iteration,
                                                 button_width, exit_button.height))
                iteration += 1
        return list_of_themes

    def draw_list_of_themes(self, button_alpha, list_of_themes):
        global button_boxes
        iteration = 0
        for theme in os.listdir('res'):
            if os.path.isdir('res\\'+ str(theme)):
                self.draw_button(list_of_themes.list_of_buttons[iteration], button_alpha)
                iteration += 1

    def draw_list_of_buttons(self, button_list, button_alpha):
        global button_boxes
        iteration = 0
        for element in button_list.list_of_buttons:
            self.draw_button(element, button_alpha)
            iteration += 1

    def draw_button(self, button, alpha):
        button_box = pygame.Surface((button.width, button.height))
        button_box.set_alpha(alpha)
        if isinstance(button.colour, tuple):
            button_box.fill(button.colour)
        else:
            button_box.blit(pygame.transform.scale(button.colour, (round(button.width), round(button.height))), (0, 0))

        DisplaySurface.blit(button_box, (button.x, button.y))
        self.text_message(button.text, button.x+button.width/2, button.y+button.height/2, button.text_colour, round(button.height*0.8))

    def check_button_box_tap(self, box, x_pos, y_pos):
        if button_boxes.button_list[box][0] <= x_pos <= button_boxes.button_list[box][0] + button_boxes.button_list[box][2]\
                and button_boxes.button_list[box][1] <= y_pos <= button_boxes.button_list[box][1] + button_boxes.button_list[box][3]:
            return box
        else:
            return -1

    def draw_map(self, map):
        help = 0
        for i in range(len(map)):
            block_x = map[help][1]
            block_y = map[help][2]
            w = map[help][3]
            h = map[help][4]
            skin_number = map[help][5]
            r = Rect((block_x, block_y), (w, h))
            DisplaySurface.blit(pygame.transform.scale(self.data.blocklist[skin_number-1], (w,h)), r)
            help += 1

    def event_check(self, button_boxes, events):
        global EditorExit
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z and pygame.key.get_mods() & KMOD_CTRL:
                self.map.pop()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                EditorExit = True
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.x_pos = event.pos[0]
                self.y_pos = event.pos[1]
                pressed = -2
                for box in range(len(button_boxes.button_list)):
                    result = self.check_button_box_tap(box, self.x_pos, self.y_pos)
                    if result != -1:
                        self.debug_console.print_message('Tap on box in ' + str(self.x_pos) + ', ' + str(self.y_pos))
                        pressed = result
                return pressed
            else:
                return -1
        if len(self.events) == 0:
            return -1

    class DebugConsole:
        def __init__(self, colour):
            self.string_number = 10
            self.x = window_size[0]*0.1
            self.y = window_size[1]*0.75
            self.colour = colour
            self.text_size = 20
            self.array_of_string = []
            for i in range(self.string_number):
                self.array_of_string.append('')

        def print_message(self, message):
            for index in range(len(self.array_of_string)-1):
                self.array_of_string[index] = self.array_of_string[index+1]
            self.array_of_string[len(self.array_of_string)-1] = str(message)

        def draw_console(self):
            global colour_pack
            for string in range(len(self.array_of_string)):
                MapEditor.text_message(MapEditor, self.array_of_string[string], self.x, self.y + string * self.text_size*1.1, self.colour, self.text_size)

    def button_glow(self, button_box):
        rect = Rect((button_box[0], button_box[1]),(button_box[2], button_box[3]))
        surface = pygame.Surface((rect.width, rect.height))
        surface.fill((0,255,0,150))
        surface.set_alpha(100)
        DisplaySurface.blit(surface, (rect.x, rect.y))

    def debug_pause(self):
        cont = True
        pygame.display.update()
        while cont:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    cont = False

    def text_message(self, msg, x, y, colour, size):
        font = pygame.font.SysFont(None, size)
        text = font.render(str(msg), True, colour)
        textpos = text.get_rect()
        textpos.centerx = x
        textpos.centery = y
        DisplaySurface.blit(text, textpos)

    class DataInit:
        def __init__(self, theme):
            self.musiclist, self.blocklist, self.barskins, self.ballskins, self.backgroundlist, \
            self.balllightlist, self.blandwa_hits, self.bar_hits = [], [], [], [], [], [], [], []
            for file in os.listdir('res\\'+theme+'\\pics\\balls\\'):
                self.ballskins.append('res\\'+theme+'\\pics\\balls\\'+str(file))
            for file in os.listdir('res\\'+theme+'\\pics\\bars\\'):
                self.barskins.append('res\\'+theme+'\\pics\\bars\\'+str(file))
            for file in os.listdir('res\\'+theme+'\\pics\\balls_lightning\\'):
                self.balllightlist.append('res\\'+theme+'\\pics\\balls_lightning\\'+str(file))
            for file in os.listdir('res\\'+theme+'\pics\\blocks\\'):
                self.blocklist.append(pygame.image.load('res\\'+theme+'\pics\\blocks\\'+str(file)).convert())
            for file in os.listdir('res\\'+theme+'\\sounds\music\\'):
                self.musiclist.append('res\\'+theme+'\\sounds\music\\'+str(file))
            for file in os.listdir('res\\'+theme+'\\pics\\backgrounds\\'):
                self.backgroundlist.append('res\\'+theme+'\\pics\\backgrounds\\'+str(file))
            for file in os.listdir('res\\' + theme + '\\sounds\\blandwa_hit\\'):
                self.blandwa_hits.append('res\\' + theme + '\\sounds\\blandwa_hit\\' + str(file))
            for file in os.listdir('res\\' + theme + '\\sounds\\bar_hit\\'):
                self.bar_hits.append('res\\' + theme + '\\sounds\\bar_hit\\' + str(file))
                self.background = pygame.image.load(choice(self.backgroundlist)).convert()
            self.background = pygame.transform.scale(self.background, (window_size[0], window_size[1])).convert()
            self.maps_directory = 'maps\\'








