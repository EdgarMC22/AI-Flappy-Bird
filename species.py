import operator
import random
import pygame

class Species(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.players = pygame.sprite.Group()
        self.average_fitness = 0
        self.threshold = 1.2
        self.players.add(player)
        self.benchmark_fitness = player.fitness
        self.benchmark_brain = player.brain.clone()
        self.champion = player.clone()
        self.staleness = 0

    def similarity(self, brain):
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return self.threshold > similarity

    @staticmethod
    def weight_difference(brain_1, brain_2):
        total_weight_difference = 0
        for i in range(0, len(brain_1.connections)):
            for j in range(0, len(brain_2.connections)):
                if i == j:
                    total_weight_difference += abs(brain_1.connections[i].weight -
                                                   brain_2.connections[j].weight)
        return total_weight_difference

    def add_to_species(self, player):
        self.players.add(player)

    def sort_players_by_fitness(self):
        sorted_sprites = sorted(self.players.sprites(), key=operator.attrgetter('fitness'), reverse=True)
        self.players.empty()
        for sprite in sorted_sprites:
            self.players.add(sprite)
        if self.players.sprites()[0].fitness > self.benchmark_fitness:
            self.staleness = 0
            self.benchmark_fitness = self.players.sprites()[0].fitness
            self.champion = self.players.sprites()[0].clone()
        else:
            self.staleness += 1

    def calculate_average_fitness(self):
        total_fitness = 0
        for p in self.players.sprites():
            total_fitness += p.fitness
        if self.players:
            self.average_fitness = int(total_fitness / len(self.players))
        else:
            self.average_fitness = 0

    def offspring(self):
        baby = self.players.sprites()[random.randint(1, len(self.players)) - 1].clone()
        baby.brain.mutate()
        return baby