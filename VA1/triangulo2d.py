class Triangulo2D:
    def __init__(self, vertices:list) -> None:
        self.verticeA = vertices[0]
        self.verticeB = vertices[1]
        self.verticeC = vertices[2]

    def pontos_arestas(self):
        vertices = [tuple(self.verticeA), tuple(self.verticeB), tuple(self.verticeC)]
        vertices_aux = list(vertices)
        pontos = set()
        for vertice in vertices:
            vertices_aux.pop(0)
            for vertice_aux in vertices_aux:
                pontos.update(self._interpolacao_linear(vertice, vertice_aux))
        return list(pontos)

    def _interpolacao_linear(self, ponto1:tuple, ponto2:tuple):
        vetor_ponto2to1 = self._sub_pontos(ponto2, ponto1)
        pontos = set()
        range1 = [x*0.01 for x in range(0, 101)]
        for b in range1:
            ponto = self._add_pontos(ponto1, self._mult_vetor_escalar(vetor_ponto2to1, b))
            pontos.add(ponto)
        return list(pontos)
    
    def _mult_vetor_escalar(self, vetor:tuple, k:float):
        return (int(vetor[0] * k), int(vetor[1] * k), int(vetor[2] * k))
    def _add_pontos(self, ponto1:tuple, ponto2:tuple):
        return (ponto1[0] + ponto2[0], ponto1[1] + ponto2[1], ponto1[2] + ponto2[2])

    def _sub_pontos(self, ponto1:tuple, ponto2:tuple):
        return (ponto1[0] - ponto2[0], ponto1[1] - ponto2[1], ponto1[2] - ponto2[2])
