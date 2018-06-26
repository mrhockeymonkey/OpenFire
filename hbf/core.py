import pygame
import sys
from os import path
from random import choice,random
from hbf import sprites, player, enemy, mob, environment, animation
from pygame.locals import * 
from settings import *

# alias
vec = pygame.math.Vector2

class Game: 
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 4, 2048) #custom mixer settings (freq, size, channels, buffersize)
        pygame.init()
        pygame.key.set_repeat(1, 1) # setup repeat keys (delay, repeat)
        
        display_info = pygame.display.Info() # initialize display
        self.window_width = 1200
        self.window_height = 800
        self.screen = pygame.display.set_mode((self.window_width, self.window_height)) #FULLSCREEN|HWSURFACE|DOUBLEBUF)
        
        self.clock = pygame.time.Clock()
        self.draw_debug = DEBUG 
        self.current_level = START_LEVEL
        self.exit = False
        self.temp = 0

        # define events
        self.FT_SWORDSTRIKE_1 = -1
        self.FT_SWORDSTRIKE_2 = -1

        # loading files
        self.load_data()

    def load_data(self):

        # check to see if running from source or bundle
        if getattr(sys, 'frozen', False):
            print('running from bundle')
            self.dir = sys._MEIPASS
            self.img_dir = os.path.join(self.dir, 'img')
            self.snd_dir = os.path.join(self.dir, 'snd')
            self.map_dir = os.path.join(self.dir, 'map')
        else:
            print('running from source')
            self.dir = os.path.dirname(__file__)
            self.img_dir = os.path.join(self.dir, '../img')
            self.snd_dir = os.path.join(self.dir, '../snd')
            self.map_dir = os.path.join(self.dir, '../map')

        # font
        self.font = os.path.join(self.img_dir, FONT)
        animation.draw_text(self.screen, "Adventure Time", self.font, 100, RED, self.window_width / 2, 200, align="n")
        animation.draw_text(self.screen, "Rescue Flame Princess", self.font, 60, RED, self.window_width / 2, self.window_height / 2, align="center")
        pygame.display.update()

        # images
        self.images = {}
        for k,v in IMAGES_TO_LOAD.items():
            self.images[k] = pygame.image.load(os.path.join(self.img_dir, v))

        # lighting effects
        self.fog = pygame.Surface((self.window_width, self.window_height))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pygame.image.load(os.path.join(self.img_dir, LIGHT_MASK)).convert_alpha()
        self.light_mask = pygame.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # load music & sounds
        pygame.mixer.music.load(os.path.join(self.snd_dir, BG_MUSIC))
        self.sounds = {}
        for k,v in SOUNDS.items():
            self.sounds[k] = pygame.mixer.Sound(os.path.join(self.snd_dir, v))
        #self.effects_sounds = {}
        #for type in GAME_SOUNDS:
        #    self.effects_sounds[type] = pygame.mixer.Sound(os.path.join(self.snd_dir, GAME_SOUNDS[type]))
#
        #self.player_hit_sounds = []
        #for snd in PLAYER_HIT_SOUND:
        #    self.player_hit_sounds.append(pygame.mixer.Sound(os.path.join(self.snd_dir, snd)))
#
        #self.ENEMY_HIT_SOUNDs = []
        #for snd in ENEMY_HIT_SOUND:
        #    self.ENEMY_HIT_SOUNDs.append(pygame.mixer.Sound(os.path.join(self.snd_dir, snd)))
   
    def new(self):
        """ Starts a new level """
        # level properties
        level_info = LEVELS[self.current_level]
        self.night = level_info['night']
        self.dungeon = level_info['dungeon']
        if self.dungeon:
            self.text_ttl = 300 #frames, not seconds

        # map, camera & hud
        self.map = environment.IsoTileMap(os.path.join(self.map_dir, level_info['map_file']))
        self.map.make()
        self.camera = environment.Camera(self.map, self.window_width, self.window_height)

        # define sprites groups
        self.all_sprites            = pygame.sprite.LayeredUpdates()
        self.wall_sprites           = pygame.sprite.Group()
        self.nearby_wall_sprites    = pygame.sprite.Group()
        self.mob_sprites            = pygame.sprite.Group()
        self.sword_sprites          = pygame.sprite.Group()
        self.item_sprites           = pygame.sprite.Group()
        self.damage_sprites         = pygame.sprite.Group()
        self.exit_sprites           = pygame.sprite.Group()
        self.npc_sprites            = pygame.sprite.Group()

        # create sprites based on the object layer from map
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = player.Player(self, vec(tile_object.x , tile_object.y))
            if tile_object.name == 'fp':
                sprites.FlamePrincess(self, vec(tile_object.x , tile_object.y))
            if tile_object.name == 'wall':
                sprites.ObstaclePoly(self, vec(tile_object.x, tile_object.y), tile_object.points)
            if tile_object.name in ['health','sword']:
                sprites.Item(self, vec(tile_object.x, tile_object.y), tile_object.name)
            if tile_object.name == 'exit':
                sprites.LevelExit(self, vec(tile_object.x, tile_object.y))

        # spawn enemy mobs
        self.spawn_points = [obj for obj in self.map.tmxdata.objects if obj.name == 'spawn']
        self.mob = mob.Mob(self, level_info['enemy_total'], level_info['enemy_onscreen'])

        # hud and level start sound
        self.hud = environment.Hud(self.player, 10, 10)


    def run(self):
        """ Main game loop consisting of events, update & draw """
        self.running = True
        self.paused = False
        pygame.mixer.music.play(loops = 0)
        
        while self.running:
            # clock.tick delays loop enough to stay at the correct FPS
            # dt is how long the previous frame took in seconds, this is used to produce smooth movement independant of frame rate
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()
        
        if not self.exit:
            # give the user a chance to start a new game
            self.show_gameover_screen()

    def events(self):
        """ Handles all in game events"""

        # first check to see what keys are pressed down to track movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.player.move('L')
        if keys[K_RIGHT] or keys[K_d]:
            self.player.move('R')
        if keys[K_UP] or keys[K_w]:
            self.player.move('U')
        if keys[K_DOWN] or keys[K_s]:
            self.player.move('D')

        # second look for other events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                self.exit = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_n:
                    self.night = not self.night
                    print('night ' +  str(self.night))
                if event.key == pygame.K_q:
                    self.draw_debug = not self.draw_debug
                    print('debug ' +  str(self.draw_debug))
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
                    self.player.stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.attack()

        # finally trigger events based on the clock. (frame bound events)
        # finns sword strike hitboxes are based on frames
        if self.FT_SWORDSTRIKE_1 > 0:
            self.FT_SWORDSTRIKE_1 -= 1
        elif self.FT_SWORDSTRIKE_1 == 0:
            self.FT_SWORDSTRIKE_1 = -1
            sprites.SwordStrike(self, self.player.strike_pos, self.player.damage, self.player.force)
        if self.FT_SWORDSTRIKE_2 > 0:
            self.FT_SWORDSTRIKE_2 -= 1
        elif self.FT_SWORDSTRIKE_2 == 0:
            self.FT_SWORDSTRIKE_2 = -1
            sprites.SwordStrike(self, self.player.strike_pos, self.player.damage, self.player.force)
            

    def update(self):
        """Handles updating all elements of the game accordingly"""
        # call the update method on all sprites
        self.polytests = 0
        self.all_sprites.update()

        # ???
        self.camera.update(self.player)
        self.hud.update()

        # player hits level exit
        hit = pygame.sprite.spritecollide(self.player, self.exit_sprites, False, sprites.Sprite.collide_hitrect)
        if hit:
            if self.dungeon and len(self.mob.enemies) != 0:
                pass # player has to clear dungeon to proceed
            else:
                animation.draw_text(self.screen, "Loading", self.font, 60, RED, self.window_width / 2, self.window_height / 2, align="center")
                pygame.display.update()
                self.current_level += 1
                self.new()

        # player hits fp
        hit = pygame.sprite.spritecollide(self.player, self.npc_sprites, False, sprites.Sprite.collide_hitrect)
        if hit:
            self.current_level = 0
            animation.draw_text(self.screen, "mathematical", self.font, 60, RED, self.window_width / 2, self.window_height / 2, align="center")
            pygame.display.update()
            pygame.time.wait(8000)
            self.running = False

        # player hits items
        hits = pygame.sprite.spritecollide(self.player,self.item_sprites, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.sounds['health_up'].play()
                self.player.health = PLAYER_HEALTH
            if hit.type == 'sword':
                hit.kill()
                self.player.pick_up_sword()


        # enemy hit player
        hits = pygame.sprite.spritecollide(self.player, self.mob_sprites, False, sprites.Sprite.collide_hitrect)
        if hits:
            self.player.hit(hits[0].atk, hits[0].rot)
            if self.player.health <= 0:
                self.running = False

        # sword hits enemy
        hits = pygame.sprite.groupcollide(self.mob_sprites, self.sword_sprites, False, True, collided=sprites.Sprite.collide_hitrect)
        for h in hits:
            h.hit(hits[h][0].damage, hits[h][0].force) # we just use the first hit even if there are multiple

        # update the state of the mob
        self.mob.update()

  
    def draw(self):
        """The draw phase draw every visible object to the screen. 
        Note that order is important, You must build up the image layer at a time"""

        # draw map basckground
        self.screen.blit(self.map.background, self.camera.apply(self.map.rect))

        # draw sprites
        for sprite in self.all_sprites:
            if sprite.image:
                self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
            if isinstance(sprite, enemy.Enemy):
                width = int(sprite.rect.width  * (sprite.health / sprite.max_health))
                health_bar = pygame.Rect(sprite.rect.x, sprite.rect.y, width, 7)
                pygame.draw.rect(self.screen, RED, self.camera.apply(health_bar))

        # draw map foreground
        self.screen.blit(self.map.foreground, self.camera.apply(self.map.rect))

        for sprite in self.damage_sprites:
            self.screen.blit(sprite.image, sprite.rect)

        # update window title with fps
        pygame.display.set_caption("Happy Battle Factor | {0:.2f}fps".format(self.clock.get_fps()))
        
        # debug 
        if self.draw_debug == True:
            print("polytests: {0}".format(self.polytests))
            pygame.display.set_caption("Happy Battle Factor | {0:.2f}fps {1}".format(
                self.clock.get_fps(), 
                len(self.nearby_wall_sprites.sprites())
            ))
            for sprite in self.all_sprites:
                sprite.draw_debug()
        
        if self.night:
            self.render_fog()
        
        # draw the HUD
        pygame.draw.rect(self.screen, self.hud.hbar_fill_col, self.hud.hbar_fill)
        pygame.draw.rect(self.screen, self.hud.hbar_outline_col, self.hud.hbar_outline, 2)  

        if self.dungeon:
            if self.text_ttl > 0:
                self.text_ttl -= 1
                animation.draw_text(self.screen, "Survive", self.font, 60, RED, self.window_width / 2, self.window_height / 2, align="center")

        if self.paused:
            self.screen.blit(self.dim_screen, (0,0))
            animation.draw_text(self.screen, "Paused", self.font, 105, RED, self.window_width / 2, self.window_height / 2, align="center")

        # update the screen
        pygame.display.update()

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player.rect).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0,0), special_flags=pygame.BLEND_MULT)

    def show_gameover_screen(self):
        self.screen.fill(BLACK)
        animation.draw_text(self.screen, "GAME OVER", self.font, 100, RED, self.window_width/2, self.window_height/2, align="center")
        animation.draw_text(self.screen, "press a key to restart", self.font, 50, WHITE, self.window_width/2, self.window_height * 3/4, align="center")
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pygame.event.wait() #clear event queue
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False
        
