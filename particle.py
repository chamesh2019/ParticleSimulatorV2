from turtle import position
import numpy as np
from scipy.spatial.distance import cdist

class Particles:
    def __init__(self, size: tuple[int, int])  -> None:
        self.particles: list[Particle] = []
        self.ACC_CONST = 25000
        self.smoothing = 5
        self.width = size[0]
        self.height = size[1]
        self.margin = 50


        self.generate_wall()
        
    def generate_wall(self) -> None:
        step = 50
        for pos in range(0, self.height * 2, step):
            self.add_particle(-self.margin, pos - self.height / 2)
        
        for pos in range(0, self.height * 2, step):
            self.add_particle(self.width + self.margin, pos - self.height / 2)

        for pos in range(0, self.width * 2, step):
            self.add_particle(pos - self.width / 2, -self.margin)
        
        for pos in range(0, self.width * 2, step):
            self.add_particle(pos - self.width / 2, self.height + self.margin)


    def add_particle(self, pos_x, pos_y) -> None:
        self.particles.append(Particle(pos_x, pos_y))


    def calculate_acceleration(self)  -> None:
        positions = [paricle for paricle in self.particles]

        for position in positions:
            position.acceleration = np.array([0, 0], dtype=np.float64)

        positions = np.array([position.pos for position in positions])

        distances = cdist(positions, positions)
        distances[distances == 0] = np.inf

        
        deltas = positions[:,None,:] - positions[None,:,:] # (N,N,2)
        angles = np.arctan2(deltas[:,:,1], deltas[:,:,0]) # (N,N)

        forces = self.ACC_CONST / (distances ** 2)

        accelerationX = forces * np.cos(angles)
        accelerationY = forces * np.sin(angles)

        for index, (par_accX, par_accY) in enumerate(zip(accelerationX, accelerationY)):
            self.particles[index].acceleration = np.array([float(np.sum(par_accX)), float(np.sum(par_accY))])

    def calculate_velocity(self) -> None:
        for particle in self.particles:
            if not particle.is_out(self.width, self.height, self.margin):
                particle.velocity += particle.acceleration 
                particle.velocity = particle.velocity * ((100 - self.smoothing) / 100)
                particle.pos += particle.velocity


    def update(self) -> None:
        self.calculate_acceleration()
        self.calculate_velocity()


class Particle:
    def __init__(self, pos_x: int, pos_y: int) -> None:
        self.pos = np.array([pos_x, pos_y], dtype=np.float64)
        self.velocity = np.array([0, 0], dtype=np.float64)
        self.acceleration = np.array([0, 0], dtype=np.float64)
    
    def is_out(self, width: int, height: int, margin: int) -> bool:
        if self.pos[0] <= -margin:
            return True

        if self.pos[0] >= width + margin:
            return True
        
        if self.pos[1] <= - margin:
            return True
        
        if self.pos[1] >= height + margin:
            return True
        return False

