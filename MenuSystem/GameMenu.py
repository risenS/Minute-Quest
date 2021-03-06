import pygame
from config import *
from MenuSystem.Button import Button
import pickle


class GameMenu(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize Control Menu"""
        super().__init__()
        self.screen = pygame.Surface(SCREEN_RES)

        self.rect = self.screen.get_rect()
        self.font = pygame.font.Font('./fonts/AmaticSC-Regular.ttf',20)
        self.headerFont = pygame.font.Font('./fonts/AmaticSC-Regular.ttf',75)
        self.headertextColor = pygame.color.THECOLORS['white']
        self.bg_color = pygame.color.THECOLORS['black']
        self.buttonColor = pygame.color.THECOLORS['blue']
        self.buttonTextColor = pygame.color.THECOLORS['white']
        self.buttonSelectColor = pygame.color.THECOLORS['yellow']
        self.margin = 10

        self.screen.fill(self.bg_color)
        self.header = self.headerFont.render("Minute Quest", False, self.headertextColor)
        self.headerRect = self.header.get_rect()
        self.headerRect.topleft = (self.margin, self.margin)
        self.buttonOptions = [
            "Enter Dungeon",
            "Fight The Boss",
            "Save Game",
            "Main Menu"
        ]
        self.buttons = []
        for option in self.buttonOptions:
            text = self.font.render(option,False,self.buttonTextColor)
            self.buttons.append(Button(text, 0, 0, 300, 50, self.buttonColor,self.buttonSelectColor) )

        self.placeButtons()
        self.current_index = 0
        default = self.buttons[self.current_index]
        default.select()
        self.selectedOption = None
        self.keyboardControls = pygame.Surface(SCREEN_RES)
        self.gamepadControls = pygame.Surface(SCREEN_RES)
        self.bg_image = pygame.image.load('images/DungeonBg.png')
        self.ambient_sound = pygame.mixer.Sound('Sounds/water_ambience.wav')

    def Reset(self):
        self.current_index = 0
        self.selectedOption = None
        for button in self.buttons:
            button.deselect()
        self.buttons[self.current_index].select()

    def placeButtons(self):
        """Place buttons on screen"""
        gap_y = self.margin
        totalHeightButton = 0
        for button in self.buttons:
            totalHeightButton += gap_y + button.rect.h

        current_y = SCREEN_RES[1] - totalHeightButton - self.margin
        for button in self.buttons:
            x = self.margin + button.rect.w//2
            y = current_y
            button.updateLocation(x, y)
            current_y += button.rect.h + 5

    def play_music(self):
        # pygame.mixer.music.load('Sounds/Music/Loop_NatureGoddess_00.ogg')
        # pygame.mixer.music.queue('Sounds/Music/Loop_NatureGoddess_01.ogg')
        # pygame.mixer.music.queue('Sounds/Music/Loop_NatureGoddess_02.ogg')
        # pygame.mixer.music.queue('Sounds/Music/Loop_NatureGoddess_03.ogg')
        # pygame.mixer.music.queue('Sounds/Music/Loop_NatureGoddess_04.ogg')
        # pygame.mixer.music.set_volume(0.1)
        # pygame.mixer.music.play()
        pass

    def play_sounds(self):
        self.ambient_sound.set_volume(.1)
        self.ambient_sound.play()

    def stop_sounds(self):
        self.ambient_sound.stop()

    def update(self,key):
        """Evaluate action based on user keypress"""
        if key == pygame.K_w or key == pygame.K_a:
            if self.current_index > 0:
                self.buttons[self.current_index].deselect()
                self.current_index -= 1
                self.buttons[self.current_index].select()

        if key == pygame.K_s or key == pygame.K_d:
            if self.current_index < len(self.buttons)-1:
                self.buttons[self.current_index].deselect()
                self.current_index += 1
                self.buttons[self.current_index].select()

        if self.buttonOptions[self.current_index] == "Enter the Dungeon":
            pass
        elif self.buttonOptions[self.current_index] == "Shop":
            pass
        elif self.buttonOptions[self.current_index] == "Fight The Boss":
            pass
        elif self.buttonOptions[self.current_index] == "Save Game":
            pass

        if key == pygame.K_RETURN:
            if self.buttonOptions[self.current_index] == "Main Menu" or \
                    self.buttonOptions[self.current_index] == "Enter Dungeon" or \
                        self.buttonOptions[self.current_index] == "Fight The Boss" or \
                    self.buttonOptions[self.current_index] == "Save Game":
                self.setMenuSelection()

    def getMenuSelection(self):
        self.stop_sounds()
        return self.selectedOption

    def setMenuSelection(self):
        self.selectedOption = self.buttonOptions[self.current_index]

    def draw(self, window):
        self.screen.blit(self.bg_image, (0, 0))
        self.screen.blit(self.header, self.headerRect)
        for button in self.buttons:
            button.draw(self.screen)

        window.blit(self.screen, self.rect)


if __name__ == "__main__":
    import os
    from EventManager import *

    running = True
    clock = pygame.time.Clock()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Menu Test")
    screen = pygame.display.set_mode(SCREEN_RES)
    eventManager = EventManager()
    menu = LandingMenu()
    eventManager.addGameMenu(menu)

    while running:

        # UPDATES
        running = eventManager.process_menu_input()

        if not running:
            break

        screen.fill(pygame.color.THECOLORS['black'])
        menu.draw(screen)
        pygame.display.update()


