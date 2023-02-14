from PIL import Image, ImageDraw
import keyboard

class Triangulo3D:
    def __init__(self, file:str) -> None:
        self.file = file
        self.recarregar()
        
    def recarregar(self):
        self.vertices = []
        self.indice_vert_triangulos = []
        self.triangulos = []
        self._preencher_malha()
        self._criar_triangulos()

    def _open_file(self, file:str):
        with open(file, 'r') as arquivo:
            return arquivo.readlines()
        
    def _preencher_malha(self):
        texto = self._open_file(self.file)
        linha1 = texto.pop(0)
        n_vertices, linha1 = self._procura_numero(linha1)
        n_triangulos, _ = self._procura_numero(linha1)
        for _ in range(n_vertices):
            linha = texto.pop(0)
            x, linha = self._procura_numero(linha)
            y, linha = self._procura_numero(linha)
            z, _ = self._procura_numero(linha)
            self.vertices.append((x, y, z))

        for _ in range(n_triangulos):
            linha = texto.pop(0)
            x, linha = self._procura_numero(linha)
            y, linha = self._procura_numero(linha)
            z, _ = self._procura_numero(linha)
            self.indice_vert_triangulos.append((x, y, z))

    def _procura_numero(self, linha:str):
        num = ''
        continua = 0
        for chr in linha:
            continua += 1
            if chr == ' ' or chr == '\n':
                break
            num += chr
        num = int(num)
        linha = linha[continua:]
        return num, linha

    def _criar_triangulos(self):
        for indices in self.indice_vert_triangulos:
            vertices = []
            vertices.append(tuple(self.vertices[indices[0] - 1]))
            vertices.append(tuple(self.vertices[indices[1] - 1]))
            vertices.append(tuple(self.vertices[indices[2] - 1]))
            self.triangulos.append(Triangulo2D(vertices))
class Triangulo2D:
    def __init__(self, vertices:list) -> None:
        self.verticeA = vertices[0]
        self.verticeB = vertices[1]
        self.verticeC = vertices[2]

class Camera:
    def __init__(self, file:str) -> None:
        self.file = file
        self.recarregar()
    
    def recarregar(self):
        self.vetorN = ()
        self.vetorV = ()
        self.pontoC = ()
        self.escalarD = None
        self.escalarHx = None
        self.escalarHy = None
        self._preencher_parametros()

    def _open_file(self, file:str):
        with open(file, 'r') as arquivo:
            return arquivo.readlines()
        
    def _preencher_parametros(self):
        texto = self._open_file(self.file)
        for linha in texto:
            chr = linha[0].upper()
            linha_aux = str(linha[4:])
            if chr == 'C' or chr == 'N' or chr == 'V':
                x, linha_aux = self._procura_numero(linha_aux)
                y, linha_aux = self._procura_numero(linha_aux)
                z, _ = self._procura_numero(linha_aux)
                tupla = (x,y,z)
                if chr == 'C':
                    self.pontoC = tupla
                elif chr == 'N':
                    self.vetorN = tupla
                else:
                    self.vetorV = tupla
            else:
                var, _ = self._procura_numero(linha_aux)
                if chr == 'D':
                    self.escalarD = var
                elif chr == 'X':
                    self.escalarHx = var
                else:
                    self.escalarHy = var
    
    def _procura_numero(self, linha:str):
        num = ''
        continua = 0
        for chr in linha:
            continua += 1
            if chr == ' ' or chr == '\n':
                break
            num += chr
        num = int(num)
        linha = linha[continua:]
        return num, linha

class Main:
    def __init__(self) -> None:
        file_triangulo = input('Qual o dir do arquivo dos Triângulos: ')
        file_camera = input('Qual o dir do arquivo dos Parâmetros da Câmera: ')
        self.triangulo3D = Triangulo3D(file_triangulo)
        self.camera = Camera(file_camera)
        while True:
            print('CTRL+L -> RECARREGAR')
            keyboard.wait('ctrl+l')
            self.triangulo3D.recarregar()
if __name__ == '__main__':
    Main()