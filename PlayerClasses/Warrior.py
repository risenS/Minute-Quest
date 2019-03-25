import pygame
import copy
from Actors.Player import Player
from Weapon import Weapon


class Warrior(Player):
    """ The playable Warrior character class. This
        character will be the melee damage specialist."""

    def __init__(self, start_pos, img="images/Characters/"
                                      "warrior", stats=[3, 1, 1, 30]):
        super().__init__(start_pos, img)
        # CONSTRUCTOR PARAMETERS #
        # stats: a list of initial stats in the order [MELEE, RANGE, MAGIC, MAX_HP]

        self.class_name = "WARRIOR"
        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]
        self.base_stats = copy.deepcopy(self.stats)

        self.weapons["axe"] = Weapon("images/Weapons/w_axe_war_0.png", (40, 40))
        self.cur_weapon = self.weapons["axe"]

        self.num_rages = 3
        self.rage_timer = 0     # counts upward to self.max_rage_timer
        self.max_rage_time = 5
        self.rage_active = False

    def use_ability(self, keys, mouseButtons):
        """ Method for using class-specific ability."""
        if keys[pygame.K_r] or mouseButtons[2]:
            if self.num_rages > 0:
                self.activate_rage()

    def activate_rage(self):
        """ Method for applying the effects of rage."""
        if not self.rage_active:
            self.rage_active = True
            self.num_rages -= 1
            self.stats["MELEE"] *= 2
            self.stats["CUR_HP"] += self.stats["MAX_HP"] // 4

    def deactivate_rage(self):
        """ Method for turning off the effects of rage."""
        self.rage_active = False
        self.rage_timer = 0
        self.stats["MELEE"] = self.base_stats["MELEE"]
        if self.stats["CUR_HP"] > self.stats["MAX_HP"]:
            self.stats["CUR_HP"] = self.stats["MAX_HP"]

    def rage_update(self, dt):
        """ Update the status of the Warrior rage
            ability."""
        self.rage_timer += dt
        if self.rage_timer >= self.max_rage_time:
            self.deactivate_rage()

    def update(self, *args):
        """ Override for base class update method.
            Has all the same functionality, just added rage
            mechanics for Warrior."""
        mouseButtons, keys, dt = args
        super().update(*args)
        self.use_ability(keys, mouseButtons)
        self.basic_attack(mouseButtons, keys, dt)
        if self.rage_active:
            self.rage_update(dt)
        if self.weapon_active:
            self.weapon_update(dt)

    def draw(self, window, cameraPos):
        super().draw(window,cameraPos)
        # testing player weapon image
        if self.cur_weapon is not None:
            if self.facing_right:
                if self.weapon_active:
                        window.blit(self.cur_weapon.image,
                                    (self.rect.x - cameraPos[0] + 15, self.rect.y - cameraPos[1])
                                    )
            if not self.facing_right:
                if self.weapon_active:
                        window.blit(pygame.transform.flip(self.cur_weapon.image, True, False),
                                    (self.rect.x - cameraPos[0] - 15, self.rect.y - cameraPos[1])
                                    )