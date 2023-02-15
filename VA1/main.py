from PIL import Image, ImageDraw, ImageTk
import tkinter
from threading import Thread


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
        print(self.pontos_arestas())

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
    def pontos_arestas(self):
        pontos = set()
        for triangulo in self.triangulos:
            pontos.update(triangulo.pontos_arestas())
        return list(pontos)
    
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
        img = Image.new('RGB', (100, 100), 'black')
        while True:
            self.showPIL(img)
            print('CTRL+L -> RECARREGAR')
            self.triangulo3D.recarregar()

    def showPIL(self, pilImage):
        root = tkinter.Tk()
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        root.focus_set()    
        root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        canvas = tkinter.Canvas(root,width=w,height=h)
        canvas.pack()
        canvas.configure(background='black')
        imgWidth, imgHeight = pilImage.size
        if imgWidth > w or imgHeight > h:
            ratio = min(w/imgWidth, h/imgHeight)
            imgWidth = int(imgWidth*ratio)
            imgHeight = int(imgHeight*ratio)
            pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(pilImage)
        imagesprite = canvas.create_image(w/2,h/2,image=image)
        root.bind('ctrl', root.quit)
        tkinter.Button(root, text="Quit", command=root.destroy).pack()
        root.mainloop()
        print('deuu')

if __name__ == '__main__':
    Main()