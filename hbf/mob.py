import pygame
from hbf import enemy
from random import choice, randint

vec = pygame.math.Vector2

class Mob():
    def __init__(self, game, count):
        self.game = game
        self.count = count
        self.alive = True
        self.enemies = []
        self.spawn_radius = 30

        for c in range(0, count):
            self.spawn()

    def update(self):
        pass

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
                placed = True
            



