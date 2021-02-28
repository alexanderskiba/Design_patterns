class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def _get_lights_and_obstacles(self, grid):
        lights = []
        obstacles = []
        for i, row in enumerate(grid):
            for j, elem in enumerate(row):
                if elem == 1:
                    lights += [(j, i)]
                elif elem == -1:
                    obstacles += [(j, i)]
        return lights, obstacles

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)
        lights, obstacles = self._get_lights_and_obstacles(grid)
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        return self.adaptee.generate_lights()