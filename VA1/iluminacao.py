class Iluminacao:
    def __init__(self, file:str) -> None:
        self.file = file
    
    def recarregar(self):
        self._preencher_parametros()
        
    def _preencher_parametros(self):
        texto = self._open_file(self.file)
        for linha in texto:
            a = linha.split(' = ')
            variavel = a.pop(0)
            a = a[0].split(' ')
            if variavel == 'Iamb':
                self.Iamb = (int(a[0]), int(a[1]), int(a[2]))
            elif variavel == 'Ka':
                self.Ka = float(a[0])
            elif variavel == 'Ks':
                self.Ks = float(a[0])
            elif variavel == 'Il':
                self.Il = (int(a[0]), int(a[1]), int(a[2]))
            elif variavel == 'Pl':
                self.Pl = (int(a[0]), int(a[1]), int(a[2]))
            elif variavel == 'Kd':
                self.Kd = (float(a[0]), float(a[1]), float(a[2]))
            elif variavel == 'Od':
                self.Od = (float(a[0]), float(a[1]), float(a[2]))
            elif variavel == 'n':
                self.n = int(a[0])

    def _open_file(self, file:str):
        with open(file, 'r') as arquivo:
            return arquivo.readlines()
if __name__ == '__main__':
    i = Iluminacao('VA1\datasets\parametro_iluminacao')
    i.recarregar()
    