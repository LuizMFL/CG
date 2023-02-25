from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from triangulo3d import Triangulo3D
from camera import Camera
from pathlib import Path

PATH = Path(__file__).parent

class Main:
    def __init__(self) -> None:
        path_camera = Path(PATH, 'datasets/parametros_camera.txt')
        print(f'Parametros_Camera dir -> {path_camera}')
        self.file_camera = path_camera
        self.file_triangulo = input('Qual dir do arquivo OBJETO para abrir: ')
        self.Resx = 1000
        self.Resy = 1000
        print(f'Resolução de tela -> ({self.Resx},{self.Resy})')
        self.triangulo3D = Triangulo3D(self.file_triangulo)
        self.camera = Camera(self.file_camera, self.Resx, self.Resy)
        self.stop = False
        while True:
            self.triangulo3D.recarregar()
            self.faces_triangulos = self.triangulo3D.get_triangulos() # face_triangulo = (A, B, C) onde A,B,C = (x,y,z)
            self.pontos_vista = self.camera.recarregar(self.faces_triangulos)
            self.showPIL()
            if self.stop:
                break
            
            

    def showPIL(self):
        root = tk.Tk()
        x = self.Resx
        y = self.Resy
        canvas = tk.Canvas(root, width=x, height=y)
        canvas.pack()
        img = Image.new('RGB', (x, y), 'black')
        img_draw = ImageDraw.Draw(img)
        for ponto in self.pontos_vista:
            img_draw.point(ponto, fill='white')
        img = ImageTk.PhotoImage(img)
        
        canvas.create_image(0, 0, anchor="nw", image=img)

        button = tk.Button(root, text="Recarregar", command=lambda: root.destroy())
        canvas.create_window(x-100, y-50, anchor="nw", window=button)
        button = tk.Button(root, text="Break", command=lambda: self._breaker(root))
        canvas.create_window(x-100, y-100, anchor="nw", window=button)
        
        root.mainloop()
    def _breaker(self, root):
        root.destroy()
        self.stop = True

if __name__ == '__main__':
    Main()