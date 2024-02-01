import pygame

class General:
    def __init__(self):
        self.score = 0
        self.scroll_speed = 1
        self.win_height = 720
        self.win_width = 551
        self.ground_image = pygame.image.load("assets/ground.png")
        self.pos = (100, 250)
g = General()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type
        self.score = g.score

    def update(self):
        # Move Pipe
        self.rect.x -= g.scroll_speed
        if self.rect.x <= -(g.win_width):
            self.kill()

        # Score
        if self.pipe_type == 'bottom':
            if g.pos[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if g.pos[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                g.score += 1      

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = g.ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        # Move Ground
        self.rect.x -= g.scroll_speed
        if self.rect.x <= -(g.win_width):
            self.kill()