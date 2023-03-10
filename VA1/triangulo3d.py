class Triangulo3D:
    def __init__(self, file:str) -> None:
        self.file = file
    
    #OK!
    def get_triangulos(self):
        return self.triangulos

    #OK!
    def recarregar(self):
        self.vertices = []
        self.indice_vert_triangulos = []
        self.triangulos = []
        self._preencher_malha()
        self._criar_triangulos()

    #OK!
    def _criar_triangulos(self):
        for indices in self.indice_vert_triangulos:
            vertices = []
            vertices.append(tuple(self.vertices[indices[0] - 1]))
            vertices.append(tuple(self.vertices[indices[1] - 1]))
            vertices.append(tuple(self.vertices[indices[2] - 1]))
            self.triangulos.append((vertices[0], vertices[1], vertices[2]))

    #OK!
    def _open_file(self, file:str):
        with open(file, 'r') as arquivo:
            return arquivo.readlines()
    
    #OK!
    def _preencher_malha(self):
        texto = self._open_file(self.file)
        linha1 = texto.pop(0)
        n_vertices, linha1 = self._procura_numero(linha1, int)
        n_triangulos, _ = self._procura_numero(linha1, int)
        for _ in range(n_vertices):
            linha = texto.pop(0)
            x, linha = self._procura_numero(linha)
            y, linha = self._procura_numero(linha)
            z, _ = self._procura_numero(linha)
            self.vertices.append((x, y, z))

        for _ in range(n_triangulos):
            linha = texto.pop(0)
            x, linha = self._procura_numero(linha, int)
            y, linha = self._procura_numero(linha, int)
            z, _ = self._procura_numero(linha, int)
            self.indice_vert_triangulos.append((x, y, z))

    #OK!
    def _procura_numero(self, linha:str, tipo=float):
        num = ''
        continua = 0
        for chr in linha:
            continua += 1
            if chr == ' ' or chr == '\n':
                break
            num += chr
        num = tipo(num)
        linha = linha[continua:]
        return num, linha