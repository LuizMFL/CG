from math import sqrt

class Camera:
    def __init__(self, file:str) -> None:
        self.file = file
    
    def recarregar(self, faces_vertices):
        self.vetorN = ()
        self.vetorV = ()
        self.pontoC = ()
        self.escalarD = None
        self.escalarHx = None
        self.escalarHy = None
        self.carregar_parametros() #OK
        
        self.Resx = self.escalarHx * 250
        self.Resy = self.escalarHy * 250
        
        vertices_vista = self.mudanca_coordenadas_mundiais_to_vista(faces_vertices) # return list((A, B, C)) onde A,B,C = (x, y, z)
        vertices_perspectiva_vista = self.proj_perspectiva(vertices_vista) # return list((A, B, C)) onde A,B,C = (x, y)
        #! Calcular Normal de cada Triângulo
        #! Calcular Normal de cada Vértice
        y = [9999999999999 for _ in range(0,self.Resy)]
        self.matriz_z_buffer = [y for _ in range(0, self.Resx)] # Primeiro coordenada X depois Y
        
        faces_vertices_tela = self.mudanca_coordenadas_vista_to_tela(vertices_perspectiva_vista) # return list((A, B, C)) onde A,B,C = (x, y)
        #! Dentro do scanline, para cada PONTO encontrar o P original; E então Consultar/Atualizar o z-buffer, se a coordenada z de P < z atual do z-buffer, então ele precisa ser desenhado e para isso tem os seguintes:
        #? atual do z-buffer vai ser igual à coordenada atual
        #? Encontra N normal de P e normaliza N
        #? Encontrar V (coordenada do ponto 3D atual negativada) e normalizar ele
        #? Encontrar L = Pl - P e normalizar L
        #? Encontrar R
        #? Verificar casos especiais
        #? Calcular a Cor
        
        pontos_tela = self.rasterizacao_triangulos(faces_vertices_tela) # return list(linha,linha, ...) onde linha = (A,B,C,...)
        return pontos_tela
    
    def _consultar_atualizar_z_buffer(self, ponto:tuple):
        if ponto[2] < self.matriz_z_buffer[ponto[0]][ponto[1]]:
            self.matriz_z_buffer[ponto[0]][ponto[1]] = int(ponto[2])
            return True
        return False
    
    
    def carregar_parametros(self):
        self._preencher_parametros()
        self._ortogonalizar_vetorV()
        self._processo_Gram_Schmidt()
        
    def mudanca_coordenadas_mundiais_to_vista(self, faces_vertices):
        vertices_vista = []
        for face in faces_vertices:
            vetor_c_to_face0 = self._sub_de_Pontos_or_Vetores(face[0], self.pontoC)
            vetor_c_to_face1 = self._sub_de_Pontos_or_Vetores(face[1], self.pontoC)
            vetor_c_to_face2 = self._sub_de_Pontos_or_Vetores(face[2], self.pontoC)
            vertice_linha0 = self._mult_matriz_to_vetor(vetor_c_to_face0)
            vertice_linha1 = self._mult_matriz_to_vetor(vetor_c_to_face1)
            vertice_linha2 = self._mult_matriz_to_vetor(vetor_c_to_face2)
            vertices_vista.append((vertice_linha0, vertice_linha1, vertice_linha2))
        return vertices_vista

    #? ROUND???
    def mudanca_coordenadas_vista_to_tela(self, vertices_perspectiva_vista):
        vertices_perspectiva_vista_normal = self._coordenadas_normalizadas(vertices_perspectiva_vista) # return list((A, B, C)) onde A,B,C = (x, y)
        vertices_tela = []
        for face in vertices_perspectiva_vista_normal:
            vertice0 = (round((((face[0][0] + 1)/2) * self.Resx) + 0.5), round(self.Resy - (((face[0][1] + 1)/2) * self.Resy) + 0.5))
            vertice1 = (round((((face[1][0] + 1)/2) * self.Resx) + 0.5), round(self.Resy - (((face[1][1] + 1)/2) * self.Resy) + 0.5))
            vertice2 = (round((((face[2][0] + 1)/2) * self.Resx) + 0.5), round(self.Resy - (((face[2][1] + 1)/2) * self.Resy) + 0.5))
            vertices_tela.append((vertice0, vertice1, vertice2))
        return vertices_tela
    
    def proj_perspectiva(self, vertices_vista):
        vertices_perspectiva_vista = []
        for face in vertices_vista:
            vertice_perspectiva_vista0 = (self.escalarD * (face[0][0] / face[0][2]), self.escalarD * (face[0][1] / face[0][2]))
            vertice_perspectiva_vista1 = (self.escalarD * (face[1][0] / face[1][2]), self.escalarD * (face[1][1] / face[1][2]))
            vertice_perspectiva_vista2 = (self.escalarD * (face[2][0] / face[2][2]), self.escalarD * (face[2][1] / face[2][2]))
            vertices_perspectiva_vista.append((vertice_perspectiva_vista0, vertice_perspectiva_vista1, vertice_perspectiva_vista2))
        return vertices_perspectiva_vista
    
    def rasterizacao_triangulos(self, faces_vertices_tela):
        pontos = []
        for face in faces_vertices_tela:
            x0_y0, x1_y1, x2_y2 = self._vertice_y_menor(face) 
            deltax1_0 = x1_y1[0] - x0_y0[0]
            deltay1_0 = x1_y1[1] - x0_y0[1]
            deltax2_0 = x2_y2[0] - x0_y0[0]
            deltay2_0 = x2_y2[1] - x0_y0[1]
            try:
                declive2_0 = deltax2_0/deltay2_0
                x3 = x0_y0[0]
                for y2 in range(x0_y0[1], x1_y1[1]):
                    x3 += declive2_0
                # Criando quarto vertice
                x3_y3 = (x3, x1_y1[1])

                deltax3_0 = x3_y3[0] - x0_y0[0]
                deltay3_0 = x3_y3[1] - x0_y0[1]
                deltax1_2 = x1_y1[0] - x2_y2[0]
                deltay1_2 = x1_y1[1] - x2_y2[1]
                deltax3_2 = x3_y3[0] - x2_y2[0]
                deltay3_2 = x3_y3[1] - x2_y2[1]

                if not deltay1_0 == 0:
                    x_min = x0_y0[0]
                    x_max = x0_y0[0]
                    declive1_0 = deltax1_0/deltay1_0
                    declive3_0 = deltax3_0/deltay3_0
                    for y in range(x0_y0[1], x1_y1[1] + 1):
                        for x in range(round(x_min), round(x_max) + 1):
                                
                                pontos.append((x,y))
                        if deltax1_0 < deltax3_0:
                            x_min += declive1_0
                            x_max += declive3_0
                        else:
                            x_min += declive3_0
                            x_max += declive1_0

                    if not deltay1_2 == 0:
                        x_min = x2_y2[0]
                        x_max = x2_y2[0]
                        declive3_2 = deltax3_2/deltay3_2
                        declive1_2 = deltax1_2/deltay1_2
                        for y in range(x2_y2[1], x1_y1[1] - 1, -1):
                            for x in range(round(x_min), round(x_max) + 1):
                                    pontos.append((x,y))
                            if deltax1_2 > deltax3_2:
                                x_min -= declive3_2
                                x_max -= declive1_2
                            else:
                                x_min -= declive1_2
                                x_max -= declive3_2
                else:
                    x_min = x2_y2[0]
                    x_max = x2_y2[0]
                    declive3_2 = deltax3_2/deltay3_2
                    declive1_2 = deltax1_2/deltay1_2
                    for y in range(x2_y2[1], x1_y1[1] - 1, -1):
                        for x in range(round(x_min), round(x_max) + 1):
                                pontos.append((x,y))
                        if deltax1_2 > deltax3_2:
                            x_min -= declive3_2
                            x_max -= declive1_2
                        else:
                            x_min -= declive1_2
                            x_max -= declive3_2
            except ZeroDivisionError:
                print(f'Todos os vertices estão contidos em uma linha que passa por Y={x2_y2[1]}: {x0_y0} - {x1_y1} - {x2_y2}')
                for x in range(x0_y0[0], x2_y2[0]):
                    pontos.append((x, x0_y0[1]))
        return pontos
    
    def _coordenadas_normalizadas(self, vertices_perspectiva_vista):
        vertices_perspectiva_vista_normal = []
        for face in vertices_perspectiva_vista:
            vertice0 = (face[0][0] / self.escalarHx, face[0][1] / self.escalarHy)
            vertice1 = (face[1][0] / self.escalarHx, face[1][1] / self.escalarHy)
            vertice2 = (face[2][0] / self.escalarHx, face[2][1] / self.escalarHy)
            vertices_perspectiva_vista_normal.append((vertice0, vertice1, vertice2))
        return vertices_perspectiva_vista_normal
    
    def _encontrar_vetorU(self):
        x = (self.vetorN[1] * self.vetorV[2]) - (self.vetorN[2] * self.vetorV[1])
        y = (self.vetorN[2] * self.vetorV[0]) - (self.vetorN[0] * self.vetorV[2])
        z = (self.vetorN[0] * self.vetorV[1]) - (self.vetorN[1] * self.vetorV[0])
        self.vetorU = (x, y, z)
        #self.vetorU = self._prod_vetorial(self.vetorN, self.vetorV_linha)

    def _mult_matriz_to_vetor(self, vetorU):
        matriz = self.base_ortonormal
        x = (matriz[0][0] * vetorU[0]) + (matriz[0][1] * vetorU[1]) + (matriz[0][2] * vetorU[2])
        y = (matriz[1][0] * vetorU[0]) + (matriz[1][1] * vetorU[1]) + (matriz[1][2] * vetorU[2])
        z = (matriz[2][0] * vetorU[0]) + (matriz[2][1] * vetorU[1]) + (matriz[2][2] * vetorU[2])
        p_linha = (x, y, z)
        return p_linha
    
    def _norma_vetor(self, vetorU):
        norma = sqrt(self._prod_escalar(vetorU, vetorU))
        return norma
    
    def _ortogonalizar_vetorV(self):
        projV_N = self._proj_ortogonal_vetores(self.vetorV, self.vetorN)
        self.vetorV = self._sub_de_Pontos_or_Vetores(self.vetorV, projV_N)
    
    def _processo_Gram_Schmidt(self):
        # Primeiro Normalizar vetores e após isso encontrar o valor de vetor U
        normaV = self._norma_vetor(self.vetorV)
        self.vetorV = self._mult_Ponto_or_Vetor_to_escalar(self.vetorV, 1/normaV)
        normaN = self._norma_vetor(self.vetorN)
        self.vetorN = self._mult_Ponto_or_Vetor_to_escalar(self.vetorN, 1/normaN)
        self._encontrar_vetorU()
        normaU = self._norma_vetor(self.vetorU)
        self.vetorU = self._mult_Ponto_or_Vetor_to_escalar(self.vetorU, 1/normaU)

        self.base_ortonormal = (self.vetorU, self.vetorV, self.vetorN)

    def _proj_ortogonal_vetores(self, vetorU, vetorV):
        u_v = self._prod_escalar(vetorU, vetorV)
        v_v = self._prod_escalar(vetorV, vetorV)
        k = u_v / v_v
        result = self._mult_Ponto_or_Vetor_to_escalar(vetorV, k)
        return result
    
    def _mult_Ponto_or_Vetor_to_escalar(self, p_or_v, k):
        return (p_or_v[0] * k, p_or_v[1] * k, p_or_v[2] * k)

    def _prod_escalar(self, vetorU, vetorV):
        return (vetorU[0] * vetorV[0]) + (vetorU[1] * vetorV[1]) + (vetorU[2] * vetorV[2])

    def _sub_de_Pontos_or_Vetores(self, p_v1, p_v2):
        return (p_v1[0] - p_v2[0], p_v1[1] - p_v2[1], p_v1[2] - p_v2[2])
    
    def _vertice_y_menor(self, vertices):
        face_aux = list(vertices)
        x0_y0 = face_aux[0] if face_aux[0][1] <= face_aux[1][1] else face_aux[1]
        x0_y0 = x0_y0 if x0_y0[1] <= face_aux[2][1] else face_aux[2]
        face_aux.pop(face_aux.index(x0_y0))
        x1_y1 = face_aux[0] if face_aux[0][1] <= face_aux[1][1] else face_aux[1]
        face_aux.pop(face_aux.index(x1_y1))
        x2_y2 = face_aux[0]
        if x0_y0[1] == x1_y1[1]:
            if x0_y0[0] > x1_y1[0]:
                x0_y0, x1_y1 = x1_y1, x0_y0
        if x1_y1[1] == x2_y2[1]:
            if x1_y1[0] > x2_y2[0]:
                x1_y1, x2_y2 = x2_y2, x1_y1
        return x0_y0, x1_y1, x2_y2
    
    def _preencher_parametros(self):
        texto = self._open_file(self.file)
        for linha in texto:
            a = linha.split(' = ')
            variavel = a.pop(0)
            a = a[0].split(' ')
            if variavel == 'N':
                self.vetorN = (int(a[0]), int(a[1]), int(a[2]))
            elif variavel == 'V':
                self.vetorV = (int(a[0]), int(a[1]), int(a[2]))
            elif variavel == 'd':
                self.escalarD = int(a[0])
            elif variavel == 'x':
                self.escalarHx = int(a[0])
            elif variavel == 'y':
                self.escalarHy = int(a[0])
            elif variavel == 'C':
                self.pontoC = (int(a[0]), int(a[1]), int(a[2]))
            elif variavel == 'Iamb':
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
    
    