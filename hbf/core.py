import pygame
import sys
from os import path
from random import choice,random
from hbf import sprites
from hbf import environment
from pygame.locals import * 
from settings import *

# alias
vec = pygame.math.Vector2

class Game:
    def __init__(self):
        # initiate game
        pygame.mixer.pre_init(44100, -16, 4, 2048)
        pygame.init()
        pygame.key.set_repeat(1, 1) # (delay, repeat)
        self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.clock = pygame.time.Clock()
        self.draw_debug = DEBUG
        self.exit = False

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
        else:
            print('running from source')
            self.dir = os.path.dirname(__file__)
        
        self.img_dir = os.path.join(self.dir, '../img')
        self.snd_dir = os.path.join(self.dir, '../snd')
        self.map_dir = os.path.join(self.dir, '../map')

        # lighting effects
        self.fog = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pygame.image.load(os.path.join(self.img_dir, LIGHT_MASK)).convert_alpha()
        self.light_mask = pygame.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()


        # font
        self.font = os.path.join(self.img_dir, 'ZOMBIE.TTF')
        print(os.path.join(self.img_dir, PLAYER_IMAGE))
        self.player_image = pygame.image.load(os.path.join(self.img_dir, PLAYER_IMAGE)).convert_alpha()
        self.bullet_image = pygame.image.load(os.path.join(self.img_dir, BULLET_IMG))
        
        self.splat_image = pygame.image.load(os.path.join(self.img_dir, 'splat red.png'))
        self.splat_image = pygame.transform.scale(self.splat_image, (64, 64))

        self.bullet_images = {}
        self.bullet_images['lg'] = pygame.image.load(os.path.join(self.img_dir, BULLET_IMG))
        self.bullet_images['sm'] = pygame.transform.scale(self.bullet_images['lg'], (10, 10))
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.mob_image = pygame.image.load(os.path.join(self.img_dir, MOB_IMAGE))
        


        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pygame.image.load(os.path.join(self.img_dir, img))) #convert alpha??

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
        
        self.map = environment.TileMap(os.path.join(self.map_dir, MAP))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        
        self.camera = environment.Camera(self.map, WINDOWWIDTH, WINDOWHEIGHT)

        

        # Define sprites
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.wall_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            # could calculate center here to be cleaner
            if tile_object.name == 'player':
                self.player = sprites.Player(self, tile_object.x , tile_object.y)
            if tile_object.name == 'wall':
                sprites.Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                sprites.Mob(self, tile_object.x, tile_object.y)
            if tile_object.name in ['health', 'shotgun']:
                sprites.Item(self, vec(tile_object.x, tile_object.y), tile_object.name)

        self.hud = environment.Hud(self.player, 10, 10)
            
        self.effects_sounds['level_start'].play()


    def run(self):
        # Game loop
        self.running = True
        pygame.mixer.music.play(loops = 1)
        
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
        #Game loop - events
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

    def update(self):
        # call the update method on all sprites
        self.all_sprites.update()

        # ???
        self.camera.update(self.player)
        self.hud.update()

        # player hits items
        hits = pygame.sprite.spritecollide(self.player,self.item_sprites, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.health = PLAYER_HEALTH
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'

        # should this move to the mob class????
        # mobs hit player
        hits = pygame.sprite.spritecollide(self.player, self.mob_sprites, False, sprites.collide_hit_rect)
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

        # bullets hit mobs
        hits = pygame.sprite.groupcollide(self.mob_sprites, self.bullet_sprites, False, True)
        for mob in hits:
            # decrement health by damange * # of bullets that hit
            #hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.dmg
            # stall sprite to simulate stopping power of bullet
            mob.vel = vec(0, 0)
  

    def draw(self):

        # draw map5
        self.screen.blit(self.map_img, self.camera.apply(self.map_rect))



        # draw sprites
        for sprite in self.all_sprites:
            if isinstance(sprite, sprites.Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

        
        # debug 
        if self.draw_debug == True:
            pygame.display.set_caption("FPS: {:.2f}".format(self.clock.get_fps()))
            pygame.draw.rect(self.screen, WHITE, self.camera.apply(self.player.rect), 2) #screen, color, rect, thickness
            pygame.draw.rect(self.screen, RED, self.camera.apply(self.player.hit_rect), 2)
            for sprite in self.mob_sprites:
                pygame.draw.rect(self.screen, WHITE, self.camera.apply(sprite.rect), 2)
                pygame.draw.rect(self.screen, RED, self.camera.apply(sprite.hit_rect), 2)
                #pygame.draw.line(self.screen, RED, sprite.pos, (sprite.pos + sprite.vel * 20)) # target line
            for sprite in self.wall_sprites:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply(sprite.rect), 2)
            for sprite in self.bullet_sprites:
                pygame.draw.rect(self.screen, RED, self.camera.apply(sprite.rect), 2)
        
        if self.night:
            self.render_fog()
        
        
        # draw the HUD
        pygame.draw.rect(self.screen, self.hud.hbar_fill_col, self.hud.hbar_fill)
        pygame.draw.rect(self.screen, self.hud.hbar_outline_col, self.hud.hbar_outline, 2)  


        if self.paused:
            self.screen.blit(self.dim_screen, (0,0))
            self.draw_text("Paused", self.font, 105, RED, WINDOWWIDTH / 2, WINDOWHEIGHT / 2, align="center")

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
        self.draw_text("GAME OVER", self.font, 100, RED, WINDOWWIDTH/2, WINDOWHEIGHT/2, align="center")
        self.draw_text("press a key to restart", self.font, 50, WHITE, WINDOWWIDTH/2, WINDOWHEIGHT * 3/4, align="center")
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
        
