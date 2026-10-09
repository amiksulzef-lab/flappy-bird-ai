import random
import pygame

WIDTH = 288
HEIGHT = 512
FLOOR_Y = 400
PIPE_GAP = 120
PIPE_DIST = 180  # space between pipes
SPEED = 4

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird AI")
font = pygame.font.SysFont("arial", 18, bold=True)

BG = pygame.image.load("assets/background-day.png").convert()
BASE = pygame.image.load("assets/base.png").convert_alpha()
PIPE_BOTTOM = pygame.image.load("assets/pipe-green.png").convert_alpha()
PIPE_TOP = pygame.transform.flip(PIPE_BOTTOM, False, True)
BIRD_IMGS = [
    pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(),
    pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(),
    pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(),
]


class Bird:
    def __init__(self):
        self.x = 60
        self.y = 200
        self.vel = 0
        self.frame = 0

    def jump(self):
        self.vel = -9

    def move(self):
        self.vel += 1
        if self.vel > 10:
            self.vel = 10
        self.y += self.vel
        self.frame += 1

    def draw(self, win):
        img = BIRD_IMGS[self.frame // 5 % 3]
        angle = max(-90, min(25, -self.vel * 4))
        img = pygame.transform.rotate(img, angle)
        rect = img.get_rect(center=(self.x + 17, self.y + 12))
        win.blit(img, rect)

    def get_rect(self):
        # a bit smaller than the bird
        return pygame.Rect(self.x + 3, self.y + 3, 28, 18)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(80, 240)  # top of the gap
        self.passed = False

    def move(self):
        self.x -= SPEED

    def draw(self, win):
        win.blit(PIPE_TOP, (self.x, self.gap_y - 320))
        win.blit(PIPE_BOTTOM, (self.x, self.gap_y + PIPE_GAP))

    def collide(self, bird):
        r = bird.get_rect()
        top = pygame.Rect(self.x, 0, 52, self.gap_y)
        bottom = pygame.Rect(self.x, self.gap_y + PIPE_GAP, 52, HEIGHT)
        return r.colliderect(top) or r.colliderect(bottom)


def bird_dead(bird, pipes):
    if bird.y + 24 >= FLOOR_Y or bird.y < 0:
        return True
    for p in pipes:
        if p.collide(bird):
            return True
    return False


def update_pipes(pipes):
    for p in pipes:
        p.move()
    if pipes[0].x < -52:
        pipes.pop(0)
        pipes.append(Pipe(pipes[-1].x + PIPE_DIST))


def draw_window(birds, pipes, base_x, texts):
    screen.blit(BG, (0, 0))
    for p in pipes:
        p.draw(screen)
    screen.blit(BASE, (base_x, FLOOR_Y))
    for b in birds:
        b.draw(screen)
    for i, t in enumerate(texts):
        screen.blit(font.render(t, True, (255, 255, 255)), (10, 10 + i * 22))
    pygame.display.update()


# play yourself
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(350), Pipe(350 + PIPE_DIST)]
    base_x = 0
    score = 0
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.move()
        update_pipes(pipes)
        base_x = (base_x - SPEED) % -48

        for p in pipes:
            if not p.passed and p.x + 52 < bird.x:
                p.passed = True
                score += 1

        if bird_dead(bird, pipes):
            print("score:", score)
            bird = Bird()
            pipes = [Pipe(350), Pipe(350 + PIPE_DIST)]
            score = 0

        draw_window([bird], pipes, base_x, ["Score: " + str(score)])

    pygame.quit()


if __name__ == "__main__":
    main()
