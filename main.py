import pygame
import sys
from random import randint


size = width, height = [800, 800]
player_image_path = "C:\\Users\\Acher\\Documents\\Python\\Yandex\\2 years\\Projects\\Pygame\\Assets\\player.png"
enemy_image_path = "C:\\Users\\Acher\\Documents\\Python\\Yandex\\2 years\\Projects\\Pygame\\Assets\\enemy.png"
plr = pygame.sprite.Group()
text = None
PAUSE = True
cur_count = 0
max_count = 0
enemy_speed = 5

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        "Инициализация игрока"
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(player_image_path)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.add(plr)
        return
    
    def render(self):
        "Отрисовка игрока"
        self.screen.blit(self.image, self.rect)
        return
    
    def reset(self):
        global cur_count, enemy_speed
        enemy_speed = 5
        cur_count = 0
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        return


class Enemy():
    def __init__(self, screen):
        "Инициализация врага"
        self.screen = screen
        self.image = pygame.image.load(enemy_image_path)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = randint(self.rect.width // 2, width - self.rect.width // 2)
        self.rect.top = self.screen_rect.top
        return
   
    def render(self):
        "Отрисовка врага"
        self.screen.blit(self.image, self.rect)
        return


class Enemys(Enemy):
    def __init__(self, screen):
        self.screen = screen
        self.enemys = []
        return
    
    def add(self):
        self.enemys.append(Enemy(self.screen))
        return
    
    def moves(self):
        global PAUSE, cur_count, max_count, enemy_speed
        i = 0
        while i < len(self.enemys):
            if pygame.sprite.spritecollideany(self.enemys[i], plr):
                PAUSE = True
                max_count = cur_count
                break
            elif self.enemys[i].rect.top + self.enemys[i].rect.height > height:
                self.enemys.pop(i)
                i -= 1
                cur_count += 1
                enemy_speed += 0.5
            else:
                self.enemys[i].rect.top += enemy_speed
            i += 1
        return
    
    def renders(self):
        for enemy in self.enemys:
            enemy.render()
        return
    
    def destroys(self):
        self.enemys.clear()
        return


def start():
    global PAUSE, cur_count
    pygame.init()
    text = pygame.font.SysFont("Consolas", 32).render("Управление стрелками", True, pygame.color.Color("White"))
    screen = pygame.display.set_mode(size)
    bg_color = (0, 0, 0)
    clock = pygame.time.Clock()
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 2000)
    player = Player(screen)
    enemys = Enemys(screen)

    while True:
        if PAUSE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    PAUSE = False
            else:
                player.reset()
                enemys.destroys()
                screen.fill(bg_color)
                screen.blit(text, (width // 2 - text.get_rect().centerx, height // 2 - text.get_rect().center[1]))
                pygame.display.flip()
                clock.tick(30)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == MYEVENTTYPE:
                    enemys.add()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                    run = True
                    while run:
                        if PAUSE:
                            break
                        for i in pygame.event.get():
                            if i.type == MYEVENTTYPE:
                                enemys.add()
                            elif i.type == pygame.KEYUP and i.key == event.key:
                                run = False
                        if event.key == pygame.K_RIGHT:
                            if player.rect.centerx + player.rect.width // 2 < width:
                                player.rect.centerx += width // 10 // 4
                            else:
                                player.rect.centerx -= 0
                        elif event.key == pygame.K_LEFT:
                            if player.rect.centerx - player.rect.width // 2 > 0:
                                player.rect.centerx -= width // 10 // 4
                            else:
                                player.rect.centerx += 0
                        screen.fill(bg_color)
                        player.render()
                        enemys.moves()
                        enemys.renders()
                        screen.blit(pygame.font.SysFont("Consolas", 32).render("current count: " + str(cur_count), True, pygame.color.Color("White")), (10, 10))
                        screen.blit(pygame.font.SysFont("Consolas", 32).render("max count: " + str(max_count), True, pygame.color.Color("White")), (10, 40))
                        pygame.display.flip()
                        clock.tick(30)
            screen.fill(bg_color)
            player.render()
            enemys.moves()
            enemys.renders()
            screen.blit(pygame.font.SysFont("Consolas", 32).render("current count: " + str(cur_count), True, pygame.color.Color("White")), (10, 10))
            screen.blit(pygame.font.SysFont("Consolas", 32).render("max count: " + str(max_count), True, pygame.color.Color("White")), (10, 40))
            pygame.display.flip()
            clock.tick(30)
    return

start()