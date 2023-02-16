from math import sqrt

class Camera:
    def __init__(self, file:str, Resx, Resy) -> None:
        self.file = file
        self.Resx = Resx
        self.Resy = Resy
    
    def recarregar(self, pontos):
        self.vetorN = ()
        self.vetorV = ()
        self.pontoC = ()
        self.escalarD = None
        self.escalarHx = None
        self.escalarHy = None
        self.preencher_parametros()
        pontos_vista = self.mudanca_coordenadas_mundiais_to_vista(pontos)
        pontos_vista = self.proj_perspectiva(pontos_vista)
        pontos_tela = self.mudanca_coordenadas_vista_to_tela(pontos_vista)
        return pontos_tela
    
    def _open_file(self, file:str):
        with open(file, 'r') as arquivo:
            return arquivo.readlines()
        
    def preencher_parametros(self):
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

    def _proj_ortogonal_vetores(self, vetorU, vetorV):
        u_v = self._prod_escalar(vetorU, vetorV)
        v_v = self._prod_escalar(vetorV, vetorV)
        k = u_v / v_v
        result = self._mult_Ponto_or_Vetor_to_escalar(vetorV, k)
        return result

    def _mult_Ponto_or_Vetor_to_escalar(self, p_or_v, k):
        return (p_or_v[0] * k, p_or_v[1] * k, p_or_v[2] * k)
    
    def _prod_escalar(self, vetorU, vetorV):
        return vetorU[0] * vetorV[0] + vetorU[1] * vetorV[1] + vetorU[2] * vetorV[2]
    
    def _ortogonalizar_vetorV(self):
        projV_N = self._proj_ortogonal_vetores(self.vetorV, self.vetorN)
        self.vetorV_linha = self._sub_de_Pontos_or_Vetores(self.vetorV, projV_N)
    
    def _encontrar_vetorU(self):
        self._ortogonalizar_vetorV()
        self.vetorU = self._prod_vetorial(self.vetorN, self.vetorV_linha)

    def _normalizacao_vetoresNVU(self):
        normaN = self._norma_vetor(self.vetorN)
        self.vetorN_normalizado = self._mult_Ponto_or_Vetor_to_escalar(self.vetorN, normaN)
        normaV_linha = self._norma_vetor(self.vetorV_linha)
        self.vetorV_linha_normalizado = self._mult_Ponto_or_Vetor_to_escalar(self.vetorV_linha, normaV_linha)
        normaU = self._norma_vetor(self.vetorU)
        self.vetorU_normalizado = self._mult_Ponto_or_Vetor_to_escalar(self.vetorU, normaU)
    def _processo_Gram_Schmidt(self):
        self._encontrar_vetorU()
        self._normalizacao_vetoresNVU()
        self.base_ortonormal = (self.vetorU_normalizado, self.vetorV_linha_normalizado, self.vetorN_normalizado)

    def mudanca_coordenadas_mundiais_to_vista(self, pontos):
        self._ortogonalizar_vetorV()
        self._processo_Gram_Schmidt()
        self.matriz_mundiais_to_vista = [self.base_ortonormal[0], self.base_ortonormal[1], self.base_ortonormal[2]]
        pontos_vista = []
        for pontoP in pontos:
            vetor_c_to_p = self._sub_de_Pontos_or_Vetores(pontoP, self.pontoC)
            p_linha = self._mult_matriz_to_vetor(self.matriz_mundiais_to_vista, vetor_c_to_p)
            pontos_vista.append(p_linha)
        return pontos_vista
    
    def mudanca_coordenadas_vista_to_tela(self, pontos):
        pontos_normal = self._coordenadas_normalizadas(pontos)
        pontos_tela = []
        for ponto in pontos_normal:
            x = (((ponto[0] + 1)/2) * self.Resx) + 0.5
            y = self.Resy - (((ponto[1] + 1)/2) * self.Resy) + 0.5
            pontos_tela.append((x, y))
        return pontos_tela
    
    def _coordenadas_normalizadas(self, pontos):
        pontos_normal = []
        for ponto in pontos:
            x = ponto[0] / self.escalarHx
            y = ponto[1] / self.escalarHy
            pontos_normal.append((x, y))
        return pontos_normal
    def proj_perspectiva(self, pontos):
        pontos_vista = []
        for ponto in pontos:
            x = self.escalarD * (ponto[0] / ponto[2])
            y = self.escalarD * (ponto[1] / ponto[2])
            pontos_vista.append((x, y))
        return pontos_vista
    
    def descartar_coordenadaZ(self, pontos):
        pontos_semZ = [(x, y) for x, y, z in pontos]
        return pontos_semZ
    def _mult_matriz_to_vetor(self, matriz, vetorU):
        x = matriz[0][0] * vetorU[0] + matriz[0][1] * vetorU[1] + matriz[0][2] * vetorU[2]
        y = matriz[1][0] * vetorU[0] + matriz[1][1] * vetorU[1] + matriz[1][2] * vetorU[2]
        z = matriz[2][0] * vetorU[0] + matriz[2][1] * vetorU[1] + matriz[2][2] * vetorU[2]
        p_linha = (x, y, z)
        return p_linha
    
    def _add_de_Vetores(self, vetorU, vetorV):
        return (vetorU[0] + vetorV[0], vetorU[1] + vetorV[1], vetorU[2] + vetorV[2])
    def _sub_de_Pontos_or_Vetores(self, p_v1, p_v2):
        return (p_v1[0] - p_v2[0], p_v1[1] - p_v2[1], p_v1[2] - p_v2[2])
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
        det2 = self._add_de_Vetores(det1, k_aux)

        u_x_v = self._sub_de_Pontos_or_Vetores(det1, det2)
        return u_x_v
    def _norma_vetor(self, vetorU):
        norma = sqrt(self._prod_escalar(vetorU, vetorU))
        return norma
