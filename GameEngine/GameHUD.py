import pygame


class GameHUD:
    """ This is the HUD class which
        displays party information,
        time remaining, etc."""

    def __init__(self, window):
        self.timer = 60     # seconds
        self.hud_surf = pygame.Surface((100, window.get_height()))
        self.font = pygame.font.Font('./fonts/LuckiestGuy-Regular.ttf',60)
        self.small_font = pygame.font.Font('./fonts/LuckiestGuy-Regular.ttf', 15)
        self.announce_font = pygame.font.Font('./fonts/LuckiestGuy-Regular.ttf', 30)
        self.font_color = pygame.color.THECOLORS['green']
        self.room_objective = None

    def draw(self, window, party_list):
        """ Draw pertinent information
            about each party member, as well
            as the remaining time."""
        x = 10
        y = 20
        bar_width = 75
        bar_height = 15
        self.hud_surf.fill((0, 0, 0))
        for char in party_list.party_members:
            if char == party_list.active_member:
                # determine what color the active party member's HP bar should be
                color = None
                hp_percentage = (char.stats["CUR_HP"] / char.stats["MAX_HP"]) * 100
                if hp_percentage <= 25:
                    color = pygame.color.THECOLORS["red"]
                elif hp_percentage <= 50:
                    color = pygame.color.THECOLORS["yellow"]
                else:
                    color = pygame.color.THECOLORS["blue"]

                # draw actual hp bar first
                pygame.draw.rect(self.hud_surf,
                                 color,
                                 (x,
                                  y,
                                  (char.stats["CUR_HP"] / char.stats["MAX_HP"]) * bar_width,
                                  bar_height)
                                 )
            else:
                # gray out hp bar for inactive members
                pygame.draw.rect(self.hud_surf,
                                 pygame.color.THECOLORS["gray"],
                                 (x,
                                  y,
                                  (char.stats["CUR_HP"] / char.stats["MAX_HP"]) * bar_width,
                                  bar_height)
                                 )
            # draw numerical values for each party member's HP
            self.hud_surf.blit(self.small_font.render(str(char.stats["CUR_HP"]) + ' / ' + str(char.stats["MAX_HP"]),
                                                      False,
                                                      (pygame.color.THECOLORS['white'])
                                                      ),
                               (x, y - 15)
                               )
            # draw outline of hp bar
            pygame.draw.rect(self.hud_surf,
                             pygame.color.THECOLORS["white"],
                             (x, y, bar_width, bar_height),
                             2)
            self.hud_surf.blit(char.rframes[1],
                               (x, y + 20)
                               )
            y += window.get_height() // 4
        # blit hud surface onto main game window
        window.blit(self.hud_surf,
                    (0, 0)
                    )
        # blit timer onto main game window
        if self.timer > 0:
            font_surf = self.font.render(str(round(self.timer, 1)),
                                         False,
                                         self.font_color
                                         )
        else:
            font_surf = self.font.render("TIME UP",
                                         False,
                                         self.font_color
                                         )
        window.blit(font_surf,
                    (window.get_width() // 2, 30)
                    )
        # blit the room objective
        # TODO Make the announcement only last for a few seconds
        # TODO Make the announcement fit better if the rect goes off-screen
        announcement = self.announce_font.render(self.room_objective, False, self.font_color)
        text_offset = announcement.get_width() // 2
        window.blit(announcement,
                    ((window.get_width() // 2) - text_offset, 525)
                    )

    def update(self, *args):
        """ Updates remaining time for given playable
            segment ( dungeon, town, etc. )"""
        mouseButtons, keys, dt = args
        self.timer -= dt

        if self.timer < 10:
            self.font_color = pygame.color.THECOLORS['red']
        elif self.timer < 30:
            self.font_color = pygame.color.THECOLORS['yellow']
        else:
            self.font_color = pygame.color.THECOLORS['green']

    def getTime(self):
        return self.timer

    def getRoomObj(self, str):
        self.room_objective = str

    def toggleDebug(self):
        pass