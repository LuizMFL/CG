from math import sqrt

class Camera:
    def __init__(self, file:str, Resx, Resy) -> None:
        self.file = file
        self.Resx = Resx
        self.Resy = Resy

    #?
    def recarregar(self, faces_vertices):
        self.vetorN = ()
        self.vetorV = ()
        self.pontoC = ()
        self.escalarD = None
        self.escalarHx = None
        self.escalarHy = None
        self.carregar_parametros() #OK
        vertices_vista = self.mudanca_coordenadas_mundiais_to_vista(faces_vertices) # return list((A, B, C)) onde A,B,C = (x, y, z)
        vertices_perspectiva_vista = self.proj_perspectiva(vertices_vista) # return list((A, B, C)) onde A,B,C = (x, y)
        faces_vertices_tela = self.mudanca_coordenadas_vista_to_tela(vertices_perspectiva_vista) # return list((A, B, C)) onde A,B,C = (x, y)
        pontos_tela = self.rasterizacao_triangulos(faces_vertices_tela) # return list(linha,linha, ...) onde linha = (A,B,C,...)
        return pontos_tela

    #OK!
    def carregar_parametros(self):
        self._preencher_parametros()
        self._ortogonalizar_vetorV()
        self._processo_Gram_Schmidt()

    #OK!
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
    
    #OK!
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

    #OK!
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
    
    #OK!
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
                var, _ = self._procura_numero(linha_aux, int)
                if chr == 'D':
                    self.escalarD = var
                elif chr == 'X':
                    self.escalarHx = var
                else:
                    self.escalarHy = var
        # print(f'CAMERA->N={self.vetorN},V={self.vetorV},C={self.pontoC},d={self.escalarD},hx={self.escalarHx},hy={self.escalarHy}')

    #OK!
    def proj_perspectiva(self, vertices_vista):
        vertices_perspectiva_vista = []
        for face in vertices_vista:
            vertice_perspectiva_vista0 = (self.escalarD * (face[0][0] / face[0][2]), self.escalarD * (face[0][1] / face[0][2]))
            vertice_perspectiva_vista1 = (self.escalarD * (face[1][0] / face[1][2]), self.escalarD * (face[1][1] / face[1][2]))
            vertice_perspectiva_vista2 = (self.escalarD * (face[2][0] / face[2][2]), self.escalarD * (face[2][1] / face[2][2]))
            vertices_perspectiva_vista.append((vertice_perspectiva_vista0, vertice_perspectiva_vista1, vertice_perspectiva_vista2))
        return vertices_perspectiva_vista

    #OK!
    def _add_de_Vetores(self, vetorU, vetorV):
        return (vetorU[0] + vetorV[0], vetorU[1] + vetorV[1], vetorU[2] + vetorV[2])

    #OK!
    def _coordenadas_normalizadas(self, vertices_perspectiva_vista):
        vertices_perspectiva_vista_normal = []
        for face in vertices_perspectiva_vista:
            vertice0 = (face[0][0] / self.escalarHx, face[0][1] / self.escalarHy)
            vertice1 = (face[1][0] / self.escalarHx, face[1][1] / self.escalarHy)
            vertice2 = (face[2][0] / self.escalarHx, face[2][1] / self.escalarHy)
            vertices_perspectiva_vista_normal.append((vertice0, vertice1, vertice2))
        return vertices_perspectiva_vista_normal

    #OK!
    def _encontrar_vetorU(self):
        self.vetorU = self._prod_vetorial(self.vetorN, self.vetorV_linha)

    #OK!
    def _mult_Ponto_or_Vetor_to_escalar(self, p_or_v, k):
        return (p_or_v[0] * k, p_or_v[1] * k, p_or_v[2] * k)

    #OK!
    def _mult_matriz_to_vetor(self, vetorU):
        matriz = self.base_ortonormal
        x = (matriz[0][0] * vetorU[0]) + (matriz[0][1] * vetorU[1]) + (matriz[0][2] * vetorU[2])
        y = (matriz[1][0] * vetorU[0]) + (matriz[1][1] * vetorU[1]) + (matriz[1][2] * vetorU[2])
        z = (matriz[2][0] * vetorU[0]) + (matriz[2][1] * vetorU[1]) + (matriz[2][2] * vetorU[2])
        p_linha = (x, y, z)
        return p_linha

    #OK!
    def _normalizacao_vetoresNVU(self):
        normaN = self._norma_vetor(self.vetorN)
        self.vetorN_normalizado = self._mult_Ponto_or_Vetor_to_escalar(self.vetorN, normaN)
        normaV_linha = self._norma_vetor(self.vetorV_linha)
        self.vetorV_linha_normalizado = self._mult_Ponto_or_Vetor_to_escalar(self.vetorV_linha, normaV_linha)
        normaU = self._norma_vetor(self.vetorU)
        self.vetorU_normalizado = self._mult_Ponto_or_Vetor_to_escalar(self.vetorU, normaU)

    #OK!
    def _norma_vetor(self, vetorU):
        norma = sqrt(self._prod_escalar(vetorU, vetorU))
        return norma

    #OK!
    def _ortogonalizar_vetorV(self):
        projV_N = self._proj_ortogonal_vetores(self.vetorV, self.vetorN)
        self.vetorV_linha = self._sub_de_Pontos_or_Vetores(self.vetorV, projV_N)

    #OK!
    def _open_file(self, file:str):
        with open(file, 'r') as arquivo:
            return arquivo.readlines()

    #OK!
    def _prod_vetorial(self, vetorU, vetorV):
        vetorI = (1, 0, 0)
        vetorJ = (0, 1, 0)
        vetorK = (0, 0, 1)
        i_aux = self._mult_Ponto_or_Vetor_to_escalar(vetorI, vetorU[1] * vetorV[2])
        j_aux = self._mult_Ponto_or_Vetor_to_escalar(vetorJ, vetorU[2] * vetorV[0])
        k_aux = self._mult_Ponto_or_Vetor_to_escalar(vetorK, vetorU[0] * vetorV[1])
        
        det1 = self._add_de_Vetores(i_aux, j_aux)
        det1 = self._add_de_Vetores(det1, k_aux)

        i_aux = self._mult_Ponto_or_Vetor_to_escalar(vetorI, vetorU[2] * vetorV[1])
        j_aux = self._mult_Ponto_or_Vetor_to_escalar(vetorJ, vetorU[1] * vetorV[0])
        k_aux = self._mult_Ponto_or_Vetor_to_escalar(vetorK, vetorU[0] * vetorV[2])

        det2 = self._add_de_Vetores(i_aux, j_aux)
        det2 = self._add_de_Vetores(det2, k_aux)

        u_x_v = self._sub_de_Pontos_or_Vetores(det1, det2)
        return u_x_v

    #OK!
    def _processo_Gram_Schmidt(self):
        self._encontrar_vetorU()
        self._normalizacao_vetoresNVU()
        self.base_ortonormal = (self.vetorU_normalizado, self.vetorV_linha_normalizado, self.vetorN_normalizado)

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

    #OK!
    def _proj_ortogonal_vetores(self, vetorU, vetorV):
        u_v = self._prod_escalar(vetorU, vetorV)
        v_v = self._prod_escalar(vetorV, vetorV)
        k = u_v / v_v
        result = self._mult_Ponto_or_Vetor_to_escalar(vetorV, k)
        return result

    #OK!
    def _prod_escalar(self, vetorU, vetorV):
        return (vetorU[0] * vetorV[0]) + (vetorU[1] * vetorV[1]) + (vetorU[2] * vetorV[2])

    #OK!
    def _sub_de_Pontos_or_Vetores(self, p_v1, p_v2):
        return (p_v1[0] - p_v2[0], p_v1[1] - p_v2[1], p_v1[2] - p_v2[2])