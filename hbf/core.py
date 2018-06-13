import pygame
import sys
from os import path
from random import choice,random
from hbf import sprites, player, enemy, mob, npc, environment
#from hbf import environment
#from hbf import input
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
        self.window_width = 1200 #display_info.current_w
        self.window_height = 800 #display_info.current_h
        self.screen = pygame.display.set_mode((self.window_width, self.window_height)) #FULLSCREEN|HWSURFACE|DOUBLEBUF)
        
        self.clock = pygame.time.Clock()
        self.draw_debug = DEBUG 
        self.level = 0
        self.exit = False
        self.temp = 0

        # define events
        self.FT_SWORDSTRIKE_1 = -1
        self.FT_SWORDSTRIKE_2 = -1

        # loading files
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

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
        self.draw_text("Adventure Time", self.font, 90, RED, self.window_width / 2, 200, align="n")
        self.draw_text("Rescue FP!", self.font, 70, RED, self.window_width / 2, self.window_height / 2, align="center")
        pygame.display.update()

        # load sprite sheet images
        self.spritesheets = {}
        
        self.images = {}
        self.images['finn_and_jake_sword_combo'] = pygame.image.load(os.path.join(self.img_dir, "finn_and_jake_sword_combo.png"))
        self.images['finn_and_jake_idle'] = pygame.image.load(os.path.join(self.img_dir, "finn_and_jake_idle.png"))
        self.images['finn_and_jake_run'] = pygame.image.load(os.path.join(self.img_dir, "finn_and_jake_run.png"))
        self.images['flame_princess_npc'] = pygame.image.load(os.path.join(self.img_dir, "flame_princess_npc.png"))
        self.images['finn_and_jake_found_sword_1'] = pygame.image.load(os.path.join(self.img_dir, "finn_and_jake_found_sword_1.png"))
        self.images['finn_and_jake_found_sword_2'] = pygame.image.load(os.path.join(self.img_dir, "finn_and_jake_found_sword_2.png"))
        self.images['finn_and_jake_found_sword_3'] = pygame.image.load(os.path.join(self.img_dir, "finn_and_jake_found_sword_3.png"))

        #for k in self.images.keys():
        #    self.images[k] = pygame.transform.scale(self.images[k], (self.images[k].get_width()*2, self.images[k].get_height()*2))
        
        self.player_ss_img = pygame.image.load(os.path.join(self.img_dir, PLAYER_SPRITESHEET))
        self.player_ss_img = pygame.transform.scale(self.player_ss_img, (self.player_ss_img.get_width()*2, self.player_ss_img.get_height()*2))

        self.spritesheets['rumo'] = pygame.image.load(os.path.join(self.img_dir, "rumo.png"))
        self.spritesheets['homun'] = pygame.image.load(os.path.join(self.img_dir, "homun.png"))
        self.spritesheets['homunculus'] = pygame.image.load(os.path.join(self.img_dir, "homunculus.png"))

        # lighting effects
        self.fog = pygame.Surface((self.window_width, self.window_height))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pygame.image.load(os.path.join(self.img_dir, LIGHT_MASK)).convert_alpha()
        self.light_mask = pygame.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()



        
        



        
        self.splat_image = pygame.image.load(os.path.join(self.img_dir, 'splat red.png'))
        self.splat_image = pygame.transform.scale(self.splat_image, (64, 64))


        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        

        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pygame.image.load(os.path.join(self.img_dir, ITEM_IMAGES[item]))

        # load music
        pygame.mixer.music.load(os.path.join(self.snd_dir, BG_MUSIC))

        # load game sounds
        self.effects_sounds = {}
        for type in GAME_SOUNDS:
            self.effects_sounds[type] = pygame.mixer.Sound(os.path.join(self.snd_dir, GAME_SOUNDS[type]))

        # load weapon sounds
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pygame.mixer.Sound(os.path.join(self.snd_dir, snd))
                s.set_volume(0.2)
                self.weapon_sounds[weapon].append(s)

        #self.weapon_sounds['gun'] = []
        #for snd in GUN_SOUND:
        #    
        #    s.set_volume(0.5)
        #    self.weapon_sounds['gun'].append(s)

        # load play hit sounds - should this be in the playerclass?
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUND:
            self.player_hit_sounds.append(pygame.mixer.Sound(os.path.join(self.snd_dir, snd)))

        # load ???
        self.mob_hit_sounds = []
        for snd in MOB_HIT_SOUND:
            self.mob_hit_sounds.append(pygame.mixer.Sound(os.path.join(self.snd_dir, snd)))
   
    def new(self):
        
        self.paused = False
        self.night = False
        self.dungeon = False

        if self.level == 2:
            self.dungeon = True
            self.night = True
            self.text_ttl = 300 #frames, not seconds

        self.map = environment.IsoTileMap(os.path.join(self.map_dir, MAPS[self.level]))
        self.map.make_map(['background','midground'])
        self.map_foreground = environment.IsoTileMap(os.path.join(self.map_dir, MAPS[self.level]))
        self.map_foreground.make_map(['foreground'], True)
        self.camera = environment.Camera(self.map, self.window_width, self.window_height)

        # Define sprites
        self.all_sprites            = pygame.sprite.LayeredUpdates()
        self.wall_sprites           = pygame.sprite.Group()
        self.nearby_wall_sprites    = pygame.sprite.Group()
        self.mob_sprites            = pygame.sprite.Group()
        self.bullet_sprites         = pygame.sprite.Group()
        self.sword_sprites          = pygame.sprite.Group()
        self.item_sprites           = pygame.sprite.Group()
        self.hidden_sprites         = pygame.sprite.Group()
        self.damage_sprites         = pygame.sprite.Group()
        self.exit_sprites           = pygame.sprite.Group()

        # create sprites based on the object layer from map
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = player.Player(self, vec(tile_object.x , tile_object.y))
            if tile_object.name == 'fp':
                npc.FlamePrincess(self, vec(tile_object.x , tile_object.y))
            if tile_object.name == 'wall':
                sprites.ObstaclePoly(self, vec(tile_object.x, tile_object.y), tile_object.points)
            if tile_object.name == 'rumo':
                enemy.Rumo(self, vec(tile_object.x, tile_object.y))
            if tile_object.name == 'homunculus':
                enemy.Homunculus(self, vec(tile_object.x, tile_object.y))
            if tile_object.name == 'homun':
                enemy.Homun(self, vec(tile_object.x, tile_object.y))
            if tile_object.name in ['health', 'shotgun','pistol','chainsaw','sword']:
                sprites.Item(self, vec(tile_object.x, tile_object.y), tile_object.name)
            if tile_object.name == 'exit':
                sprites.LevelExit(self, vec(tile_object.x, tile_object.y))

        self.spawn_points = [obj for obj in self.map.tmxdata.objects if obj.name == 'spawn']
        
        self.hud = environment.Hud(self.player, 10, 10)
            
        self.effects_sounds['level_start'].play()

        self.current_mob = mob.Mob(self, 3)



    def run(self):
        # Game loop
        self.running = True
        pygame.mixer.music.play(loops = 1)

        #self.input_manager = input.InputManager()
        
        while self.running:
            # clock.tick delays loop enough to stay at the correct FPS
            # dt is how long the previous frame took in seconds, this is used to produce smooth movement independant of frame rate
            self.dt = self.clock.tick(FPS) / 1000
            #print(self.clock.tick(FPS)/1000)
            self.events()
            if not self.paused:
                self.update()
            self.draw()
        
        if not self.exit:
            # give the user a chance to start a new game
            self.show_gameover_screen()

    def events(self):
        """
        game loop events
        """

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
            sprites.SwordStrike(self, self.player.strike_pos, self.player.damage)
        if self.FT_SWORDSTRIKE_2 > 0:
            self.FT_SWORDSTRIKE_2 -= 1
        elif self.FT_SWORDSTRIKE_2 == 0:
            self.FT_SWORDSTRIKE_2 = -1
            sprites.SwordStrike(self, self.player.strike_pos, self.player.damage)
            

    def update(self):
        # call the update method on all sprites
        self.polytests = 0
        self.all_sprites.update()

        # ???
        self.camera.update(self.player)
        self.hud.update()

        # player hits level exit
        hit = pygame.sprite.spritecollide(self.player, self.exit_sprites, False, sprites.Sprite.collide_hitrect)
        if hit:
            self.draw_text("Loading", self.font, 60, RED, self.window_width / 2, self.window_height / 2, align="center")
            pygame.display.update()
            self.level += 1
            self.new()

        # player hits items
        hits = pygame.sprite.spritecollide(self.player,self.item_sprites, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.health = PLAYER_HEALTH
            if hit.type == 'sword':
                hit.kill()
                #self.effects_sounds['gun_pickup'].play()
                self.player.pick_up_sword()
            #if hit.type == 'pistol':
            #    hit.kill()
            #    self.effects_sounds['gun_pickup'].play()
            #    self.player.weapon = 'pistol'
            #if hit.type == 'chainsaw':
            #    hit.kill()
            #    self.effects_sounds['gun_pickup'].play()
            #    self.player.weapon = 'chainsaw'

        # mobs hit player
        hits = pygame.sprite.spritecollide(self.player, self.mob_sprites, False, sprites.Sprite.collide_hitrect)
        for hit in hits:
            # randomly play hit sound
            if random() < 0.7: 
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.running = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # sword hits enemy
        hits = pygame.sprite.groupcollide(self.mob_sprites, self.sword_sprites, False, True, collided=sprites.Sprite.collide_hitrect)
        for h in hits:
            h.hit(hits[h][0].damage) # we just use the first hit even if there are multiple

  
    def draw(self):
        """The draw phase draw every visible object to the screen. 
        Note that order is important, You must build up the image layer at a time"""

        # draw map basckground
        self.screen.blit(self.map.image, self.camera.apply(self.map.rect))

        # draw sprites
        for sprite in self.all_sprites:
            if isinstance(sprite, sprites.Enemy):
                sprite.draw_health()
            if sprite.image:
                self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

        # draw map foreground
        self.screen.blit(self.map_foreground.image, self.camera.apply(self.map_foreground.rect))

        for sprite in self.damage_sprites:
            sprite.draw()

        #dot = pygame.C
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

            #pygame.draw.rect(self.screen, WHITE, self.camera.apply(self.player.rect), 2) #screen, color, rect, thickness
            #pygame.draw.rect(self.screen, RED, self.camera.apply(self.camera.rect), 4) #screen, color, rect, thickness
            ##pygame.draw.rect(self.screen, RED, self.camera.apply(self.player.hit_rect), 2)
            #pygame.draw.polygon(self.screen, CYAN, (self.camera.apply_poly(self.player.hit_poly)).points, 2)
            #
            #if self.player.atk_rect:
            #    pygame.draw.rect(self.screen, RED, self.player.atk_rect, 3)
            ##olist = self.player.mask.outline()
            ##tmpsurf = pygame.Surface((self.player.rect.width, self.player.rect.height))
            ##pygame.draw.polygon(tmpsurf, RED, olist, 0)
            ##self.screen.blit(tmpsurf, self.camera.apply(self.player.rect))
#
            #for sprite in self.all_sprites:
            #    pygame.draw.rect(self.screen, WHITE, self.camera.apply(sprite.rect), 1)
            #    pygame.draw.rect(self.screen, RED, self.camera.apply(sprite.hit_rect), 1)
            #for sprite in self.hidden_sprites:
            #    pygame.draw.rect(self.screen, BLACK, self.camera.apply(sprite.rect), 1)
            #for sprite in self.mob_sprites:
            #    #pygame.draw.rect(self.screen, WHITE, self.camera.apply(sprite.rect), 2)
            #    #pygame.draw.rect(self.screen, WHITE, self.camera.apply(sprite.image.get_rect()), 2)
            #    pygame.draw.rect(self.screen, RED, self.camera.apply(sprite.hit_rect), 2)
            #    #pygame.draw.line(self.screen, RED, sprite.pos, (sprite.pos + sprite.vel * 20)) # target line
            #for sprite in self.wall_sprites:
            #    pygame.draw.polygon(self.screen, CYAN, (self.camera.apply_poly(sprite.hit_poly)).points, 2)
            #    #pygame.draw.rect(self.screen, CYAN, self.camera.apply(sprite.rect), 2)
            #    #pygame.draw.rect(self.screen, RED, self.camera.apply(sprite.rect), 2)
            #for sprite in self.bullet_sprites:
            #    pygame.draw.rect(self.screen, RED, self.camera.apply(sprite.rect), 2)
        
        if self.night:
            self.render_fog()
        
        
        # draw the HUD
        pygame.draw.rect(self.screen, self.hud.hbar_fill_col, self.hud.hbar_fill)
        pygame.draw.rect(self.screen, self.hud.hbar_outline_col, self.hud.hbar_outline, 2)  

        if self.dungeon:
            if self.text_ttl > 0:
                self.text_ttl -= 1
                self.draw_text("Survive", self.font, 60, RED, self.window_width / 2, self.window_height / 2, align="center")

        if self.paused:
            self.screen.blit(self.dim_screen, (0,0))
            self.draw_text("Paused", self.font, 105, RED, self.window_width / 2, self.window_height / 2, align="center")

        # update the screen
        pygame.display.update()

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player.rect).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0,0), special_flags=pygame.BLEND_MULT)



    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.font, 100, RED, self.window_width/2, self.window_height/2, align="center")
        self.draw_text("press a key to restart", self.font, 50, WHITE, self.window_width/2, self.window_height * 3/4, align="center")
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
        
