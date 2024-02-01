import math
import species
import operator
import pygame
import bird_player

class Population:
    def __init__(self, size):
        self.players = pygame.sprite.Group()
        self.generation = 1
        self.species = pygame.sprite.Group()
        self.size = size

    def generate_birds(self):
        for _ in range(self.size):
            new_bird = bird_player.Bird_player()
            self.players.add(new_bird)
        return self.players

    def update(self):
        for b in self.players.sprites():
            b.update(True)

    def natural_selection(self):
        self.speciate()
        self.calculate_fitness()
        self.kill_extinct_species()
        self.kill_stale_species()
        self.sort_species_by_fitness()
        self.next_gen()

    def speciate(self):
        for s in self.species.sprites():
            s.players = pygame.sprite.Group()

        for p in self.players.sprites():
            add_to_species = False
            for s in self.species.sprites():
                if s.similarity(p.brain):
                    s.add_to_species(p)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.add(species.Species(p))

    def calculate_fitness(self):
        for p in self.players.sprites():
            p.calculate_fitness()
        for s in self.species.sprites():
            s.calculate_average_fitness()

    def kill_extinct_species(self):
        species_bin = pygame.sprite.Group()
        for s in self.species.sprites():
            if len(s.players) == 0:
                species_bin.add(s)
        for s in species_bin.sprites():
            self.species.remove(s)

    def kill_stale_species(self):
        player_bin = pygame.sprite.Group()
        species_bin = pygame.sprite.Group()
        for s in self.species.sprites():
            if s.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.add(s)
                    for p in s.players.sprites():
                        player_bin.add(p)
                else:
                    s.staleness = 0
        for p in player_bin.sprites():
            self.players.remove(p)
        for s in species_bin.sprites():
            self.species.remove(s)

    def sort_species_by_fitness(self):
        for s in self.species.sprites():
            s.sort_players_by_fitness()

        sorted_sprites = sorted(self.species.sprites(), key=operator.attrgetter('benchmark_fitness'), reverse=True)
        self.species.empty()
        for sprite in sorted_sprites:
            self.species.add(sprite)

    def next_gen(self):
        children = pygame.sprite.Group()

        # Clone of champion is added to each species
        for s in self.species.sprites():
            children.add(s.champion.clone())
        # Fill open player slots with children
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species.sprites():
            for i in range(0, children_per_species):
                children.add(s.offspring())
        while len(children) < self.size:
            children.add(self.species.sprites()[0].offspring())
        self.players = pygame.sprite.Group()
        for child in children.sprites():
            self.players.add(child)
        self.generation += 1
