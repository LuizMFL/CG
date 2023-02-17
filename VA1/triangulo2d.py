class Triangulo2D:
    def __init__(self, vertices:list) -> None:
        self.verticeA = vertices[0]
        self.verticeB = vertices[1]
        self.verticeC = vertices[2]

    def get_vertices(self):
        return (self.verticeA, self.verticeB, self.verticeC)