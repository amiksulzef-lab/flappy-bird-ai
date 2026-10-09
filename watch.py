import sys
import pygame

from game import *
from brain import Brain
from evolve import get_inputs

# watch best bird
brain = Brain.load("best_brain.json")
clock = pygame.time.Clock()

bird = Bird()
pipes = [Pipe(350), Pipe(350 + PIPE_DIST)]
base_x = 0
score = 0
best = 0

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if brain.think(get_inputs(bird, pipes)):
        bird.jump()
    bird.move()
    update_pipes(pipes)
    base_x = (base_x - SPEED) % -48

    for p in pipes:
        if not p.passed and p.x + 52 < bird.x:
            p.passed = True
            score += 1

    if bird_dead(bird, pipes):
        print("died at", score)
        best = max(best, score)
        bird = Bird()
        pipes = [Pipe(350), Pipe(350 + PIPE_DIST)]
        score = 0

    draw_window([bird], pipes, base_x, ["Score " + str(score), "Best " + str(best)])
