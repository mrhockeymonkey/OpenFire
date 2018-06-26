import pygame
from hbf import enemy
from random import choice, randint

vec = pygame.math.Vector2

class Mob():
    """
    Groups of enemy sprites that can be spawned in waves continuously
    """
    def __init__(self, game, count, onscreen):
        self.game = game
        self.count = count
        self.onscreen = onscreen
        self.spawned = 0
        self.enemies = []
        self.spawn_radius = 30

    def remove(self, sprite):
        self.enemies.remove(sprite)
        self.count -= 1
        print("{} enemies left in mob".format(self.count))

    def update(self):
        if self.spawned < self.count:
            # spawn more enemies if possible
            if len(self.enemies) < self.onscreen:
                self.spawn()

    def spawn(self):
        """
        spawn a random enemy within the radius of a randomly selected spawn point
        """
        spawn_point = choice(self.game.spawn_points)
        x, y = spawn_point.x, spawn_point.y
        enemy_name = choice(['Homun','Homunculus','Rumo'])
        placed = False

        # place an enemy within the spawn radius so that it does not have the same pos as any other enemy
        # the reason for this is to keep the avoid_mobs method happy
        while not placed:
            rand_x, rand_y = randint(0, self.spawn_radius), randint(0, self.spawn_radius)
            new_enemy = getattr(enemy, enemy_name)(self.game, vec(x + rand_x, y + rand_y))
            overlaps = [e for e in self.enemies if e.pos == new_enemy.pos]
            if len(overlaps) == 0:
                print("enemy spawned: " + enemy_name)
                self.enemies.append(new_enemy)
                self.spawned += 1
                placed = True




