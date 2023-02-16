from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from threading import Thread
from triangulo3d import Triangulo3D
from camera import Camera
from pathlib import Path

PATH = Path(__file__).parent

class Main:
    def __init__(self) -> None:
        self.file_camera = Path(PATH, 'datasets/parametros_camera.txt')
        self.file_triangulo = input('Qual arquivo para abrir: ')
        self.Resx = 1000
        self.Resy = 1000
        self.triangulo3D = Triangulo3D(self.file_triangulo)
        self.camera = Camera(self.file_camera, self.Resx, self.Resy)
        self.stop = False
        while True:
            self.triangulo3D.recarregar()
            self.pontos_arestas = self.triangulo3D.pontos_arestas()
            self.pontos_vista = self.camera.recarregar(self.pontos_arestas)
            print(self.pontos_vista)
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
        """for ponto in self.pontos_vista:
            img_draw.point(ponto, fill='white')"""
        for ponto in self.triangulo3D.pontos_arestas():
            img_draw.point((ponto[0], ponto[1]), fill='white')
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