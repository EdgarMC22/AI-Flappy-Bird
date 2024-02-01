import pygame
import brain as brain
import configure

class Bird_player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.bird_images = [pygame.image.load("assets/bird_down.png"),
                            pygame.image.load("assets/bird_mid.png"),
                            pygame.image.load("assets/bird_up.png")]    
        self.image = self.bird_images[0]
        self.rect = self.image.get_rect()
        self.pos = (100, 250)
        self.rect.center = self.pos
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True
        self.pos = (100, 250)
        self.lifespan = 0
        self.sprite = self
        
        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    def update(self, ai, user_input=None):
        # Animate Bird
        if self.alive:
            self.image_index += 1
            self.lifespan += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = self.bird_images[self.image_index // 10]

        # Gravity and Flap
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # Rotate Bird
        self.image = pygame.transform.rotate(self.image, self.vel * -7)

        # User Input (for manual play)
        if user_input is not None and isinstance(user_input, (list, tuple)):
            if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
                self.flap = True
                self.vel = -7

        # AI Control
        if ai == True:
            if self.alive:
                self.look()
                self.think()

    def bird_flap(self):
        if not self.flap and not (self.rect.y < 30):
            self.flap = True
            self.vel = -5
        if self.vel >= 3:
            self.flap = False

    # AI related functions
    def look(self):
        if configure.pipes.sprites():
            self.vision[0] = max(0, self.rect.center[1] - configure.pipes.sprites()[0].rect.bottom) / 500
        else:
            self.vision[0] = 0
        if configure.pipes.sprites() and len(configure.pipes.sprites()) > 1:
            self.vision[1] = max(0, configure.pipes.sprites()[0].rect.x - self.rect.center[0]) / 500
            self.vision[2] = max(0, configure.pipes.sprites()[1].rect.top - self.rect.center[1]) / 500
        else:
            self.vision[1] = 0
            self.vision[2] = 0

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        print("Decision:", self.decision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Bird_player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone
