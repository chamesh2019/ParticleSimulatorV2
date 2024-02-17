import pygame as pg
from particle import Particles

def main():
    pg.init()
    SIZE = (1300, 680)
    window = pg.display.set_mode(SIZE)
    clock = pg.time.Clock()


    running = True
    particles = Particles(SIZE)

    while running:
        window.fill((0, 0, 0))
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                particles.add_particle(event.pos[0], event.pos[1])

        for particle in (particles.particles):
            pg.draw.circle(pg.display.get_surface(), (255, 255, 255), tuple(particle.pos), 5)

        particles.update()
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()