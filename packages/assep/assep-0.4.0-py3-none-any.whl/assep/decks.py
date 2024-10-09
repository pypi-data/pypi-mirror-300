import pandas as pd

class DECKS():
    r"""Classe destinada a automatizar a extração de dados diretamente dos arquivos PWF/ANA/ATP/etc.

    É condensado nessa classe métodos para obter dados diretamente dos arquivos em formatos
    textuais. Os dados são extraídos visando facilitar a manipulação dos dados.

    Parameters
    ----------
    Classe inicializada com o Path do ANAREDE e a lista de SAVs a serem trabalhados.

    Examples
    --------
    Para inicializar a classe, basta chamar ela para o objeto de interesse.

    >>> import CEPEL_Tools as cp
    >>> Path_Anarede = str(r"C:\Cepel\Anarede\V110602\ANAREDE.exe")
    >>> lista_casos = easygui.fileopenbox(default="D:\\_APAGAR\\LIXO\\*.SAV", title="Selecionar os Decks SAV - ANAREDE", multiple=True)
    >>> oAnarede = cp.ANAREDE(Path_Anarede, lista_casos)
    """
    ###================================================================================================================
    ###
    ### CÓDIGOS DE INICIALIZAÇÃO
    ###
    ###================================================================================================================
    def __init__(self):
        pass

    ###================================================================================================================
    ###
    ### CÓDIGOS EXTRAÇÃO DADOS DECK CEPEL
    ###
    ###================================================================================================================
    def __get_content_codeANA(self, nome_arquivo, str_inic, str_final):
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

        # Encontrando a primeira ocorrência de 'DBAR'
        indice_codePWF = None
        for i, linha in enumerate(linhas):
            if linha.strip() == str_inic:
                indice_codePWF = i
                break

        # Encontrando a primeira ocorrência de '99999' após 'DBAR'
        indice_99999 = None
        for i, linha in enumerate(linhas[indice_codePWF:], start=indice_codePWF):
            if linha.strip() == str_final:
                indice_99999 = i
                break

        # Identificando corretamente os valores, posso dar sequência
        miolo = []
        if not indice_codePWF is None and not indice_99999 is None:
            for linha in linhas[indice_codePWF + 1:indice_99999]:
                if not linha.startswith('('):
                    miolo.append(linha)

        return miolo

    def __get_transposed_list(self, miolo, col_size):
        # Gerando a lista aninhada
        lista_dados = []
        for i in range(len(col_size)):
            col_dado = [linha[col_size[i][0]:col_size[i][1]].strip() for linha in miolo]
            lista_dados.append(col_dado)

        # Obtendo dataframe
        transposed_lista_dados = list(map(list, zip(*lista_dados)))

        return transposed_lista_dados

    ###================================================================================================================
    ###
    ### CÓDIGOS ANAFAS
    ###
    ###================================================================================================================
    def __get_codeANA_DBAR(self, miolo):
        # Lista de especificações
        cabecalhos = ["Numero",       "Codigo_Atualizacao", "Estado",       "Tipo_Barra", "A",          "Nome",       "Tensao_pre_falta", "Ang_pre_falta", "Tensao_base",
                     "Capac_DJ_kA",   "Data_Entrada",       "Data_Saida",   "Area",       "SubArea",    "Fronteira",]
        col_size =   [[0,5],          [5,6],                [6,7],          [7,8],        [8,9],        [9,21],       [22,26],             [26,30],        [31,35],
                    [36,42],        [52,60],              [60,68],        [69,72],      [72,75],      [76,77],]

        # Gerando a lista aninhada
        lista_dados = self.__get_transposed_list(miolo, col_size)
        # Obtendo dataframe
        df = pd.DataFrame(lista_dados, columns=cabecalhos)

        # Definindo alguns tipos de colunas
        df = df.astype({'Numero': int})

        return df

    def __get_codeANA_DCIR(self, miolo):
        # Lista de especificações
        cabecalhos = ["Barra_De",         "Codigo_Atualizacao",  "Estado",            "Barra_Para",          "Num_Circuito",   "Tipo_Circuito",     "R_pos",
                    "X_pos",              "R_zer",               "X_zer",             "Nome_Circuito",       "Suscep_pos_/_Pg",   "Suscep_zer_/_Qg",   "Tap",
                    "Barra_Delta_DY(TB)", "NC_ramo_serie(TC)",   "Area",              "Defasagem",           "Comprimento",       "Conexao_De",        "Rn_aterr_De",
                    "Xn_aterr_De",        "Conexao_Para",        "Rn_aterr_Para",     "Xn_aterr_Para",       "SubArea",           "N_Unidades_Total",  "N_Unidades_Operando",
                    "Capac_Interrup_De",  "Capac_Interrup_Para", "Data_Entrada",      "Data_Saida",          "MVA",               "Nome_Grupo",]
        col_size =   [[0,5],                [5,6],                 [6,7],               [7,12],                [14,16],             [16,17],              [17,23],
                    [23,29],              [29,35],               [35,41],             [41,47],               [47,52],             [52,57],              [57,62],
                    [62,67],              [67,69],               [69,72],             [72,75],               [76,80],             [80,82],              [82,88],
                    [88,94],              [94,96],               [96,102],            [102,108],             [108,111],           [115,118],            [118,121],
                    [122,128],            [131,137],             [160,168],           [168,176],             [177,184],           [199,219],]

        # Gerando a lista aninhada
        lista_dados = self.__get_transposed_list(miolo, col_size)
        # Obtendo dataframe
        df = pd.DataFrame(lista_dados, columns=cabecalhos)

        # Definindo alguns tipos de colunas
        df = df.astype({'Barra_De': int, 'Barra_Para': int, 'Num_Circuito': int,})

        return df

    def __get_codeANA_DMUT(self, miolo):
        # Lista de especificações
        cabecalhos = ["Barra_De_1",        "Codigo_Atualizacao", "Estado",       "Barra_Para_1", "Num_Circuito_1",  "Barra_De_2", "Barra_Para_2", "Num_Circuito_2",
                    "Resistencia_Mutua", "Reatancia_Mutua",    "Inicio_1",     "Final_1",      "Inicio_2",        "Final_2",    "Area",         "SubArea",]
        col_size =   [[0,5],               [5,6],                [6,7],          [7,12],         [14,16],            [16,21],     [23,28],        [30,32],
                    [32,38],             [38,44],              [45,51],        [51,57],        [57,63],            [63,69],     [69,72],        [72,75],]

        # Gerando a lista aninhada
        lista_dados = self.__get_transposed_list(miolo, col_size)
        # Obtendo dataframe
        df = pd.DataFrame(lista_dados, columns=cabecalhos)

        # Definindo alguns tipos de colunas
        df = df.astype({'Barra_De_1': int, 'Barra_Para_1': int, 'Num_Circuito_1': int, 'Barra_De_2': int, 'Barra_Para_2': int, 'Num_Circuito_2': int,})

        return df

    def __get_codeANA_DMOV(self, miolo):
        # Lista de especificações
        cabecalhos = ["Barra_De",          "Codigo_Atualizacao",   "Estado",             "Barra_Para",             "Num_Circuito",    "Tensao_Base",
                    "Corrente_Protecao", "Corrente_Disparo_Gap", "Energia_Maxima_MOV", "Potencia_Dissipada_MOV", "Tensao_Conducao", "Tipo_Disparo",]
        col_size =   [[0,5],               [5,6],                  [6,7],                [7,12],                   [14,16],           [17,21],
                    [22,30],             [31,39],                [40,48],              [49,57],                  [58,66],           [73,74],]

        # Gerando a lista aninhada
        lista_dados = self.__get_transposed_list(miolo, col_size)
        # Obtendo dataframe
        df = pd.DataFrame(lista_dados, columns=cabecalhos)

        # Definindo alguns tipos de colunas
        df = df.astype({'Barra_De': int, 'Barra_Para': int, 'Num_Circuito': int,})

        return df

    def __get_codeANA_DSHL(self, miolo):
        # Lista de especificações
        cabecalhos = ["Barra_De",  "Codigo_Atualizacao",   "Estado",            "Barra_Para",              "Num_Circuito",          "Terminal",
                    "Grupo",     "Pot_Reativa",          "Conexao",           "Resistencia_Aterramento", "Reatancia_Aterramento", "Estado_Aterramento",
                    "Nome",      "Total_Unidades",       "Unidades_Operando", "Area",                    "SubArea", ]
        col_size =   [[0,5],       [5,6],                  [6,7],                [7,12],                   [14,16],                 [16,17],
                    [17,19],     [20,26],                [27,28],              [28,34],                  [34,40],                 [40,41],
                    [41,47],     [48,51],                [51,54],              [69,72],                  [73,75],]

        # Gerando a lista aninhada
        lista_dados = self.__get_transposed_list(miolo, col_size)
        # Obtendo dataframe
        df = pd.DataFrame(lista_dados, columns=cabecalhos)

        # Definindo alguns tipos de colunas
        df = df.astype({'Barra_De': int, 'Barra_Para': int, 'Num_Circuito': int,})

        return df

    def __get_codeANA_DEOL(self, miolo):
        # Lista de especificações
        cabecalhos = ["Numero_Barra",   "Codigo_Atualizacao",    "Estado",            "K",       "Grupo",          "Pot_Ativa_pre_falta",
                    "Max_Corrente_RMS", "Tensao_Minima_Conexao", "FP_curto_circuito", "Nome",    "Total_Unidades", "Unidades_Operando",
                    "FP_pre_falta",     "Tensao_Maxima_Conexao", "Area",              "SubArea", "Nome_Extenso",   "V1",
                    "V2"]
        col_size =   [[0,5],              [5,6],                   [6,7],               [7,10],    [14,16],          [17,23],
                    [23,29],            [29,35],                 [35,41],             [41,47],   [48,51],          [51,54],
                    [55,61],            [62,68],                 [69,72],             [73,75],   [112,132],        [133,137],
                    [138,142],]

        # Gerando a lista aninhada
        lista_dados = self.__get_transposed_list(miolo, col_size)
        # Obtendo dataframe
        df = pd.DataFrame(lista_dados, columns=cabecalhos)

        # Definindo alguns tipos de colunas
        df = df.astype({'Numero_Barra': int,})

        return df

    def __get_codeANA_DARE(self, miolo):
        # Lista de especificações
        cabecalhos = ["Area", "Codigo_Atualizacao", "Nome_Area",]
        col_size =   [[0,3],         [5,6],                [18,54],]

        # Gerando a lista aninhada
        lista_dados = self.__get_transposed_list(miolo, col_size)
        # Obtendo dataframe
        df = pd.DataFrame(lista_dados, columns=cabecalhos)

        return df

    def get_df_ANA(self, nome_arquivo):
        # Inicio dicionário contendo todos os dataframes
        dic_ANA = {}

        # Coleto dados do DBAR
        miolo = self.__get_content_codeANA(nome_arquivo, "DBAR", "99999")
        dic_ANA["DBAR"] = self.__get_codeANA_DBAR(miolo)

        # Coleto dados do DCIR
        miolo = self.__get_content_codeANA(nome_arquivo, "DCIR", "99999")
        dic_ANA["DCIR"] = self.__get_codeANA_DCIR(miolo)

        # Coleto dados do DMUT
        miolo = self.__get_content_codeANA(nome_arquivo, "DMUT", "99999")
        dic_ANA["DMUT"] = self.__get_codeANA_DMUT(miolo)

        # Coleto dados do DMOV
        miolo = self.__get_content_codeANA(nome_arquivo, "DMOV", "99999")
        dic_ANA["DMOV"] = self.__get_codeANA_DMOV(miolo)

        # Coleto dados do DSHL
        miolo = self.__get_content_codeANA(nome_arquivo, "DSHL", "99999")
        dic_ANA["DSHL"] = self.__get_codeANA_DSHL(miolo)

        # Coleto dados do DEOL
        miolo = self.__get_content_codeANA(nome_arquivo, "DEOL", "99999")
        dic_ANA["DEOL"] = self.__get_codeANA_DEOL(miolo)

        # Coleto dados do DARE
        miolo = self.__get_content_codeANA(nome_arquivo, "DARE", "99999")
        dic_ANA["DARE"] = self.__get_codeANA_DARE(miolo)

        return dic_ANA

    ###================================================================================================================
    ###
    ### CÓDIGOS ANAREDE
    ###
    ###================================================================================================================
    def __get_codePWF_DBAR(self, miolo):
        # Lista de especificações
        cabecalhos = ["Numero",                 "Operacao",          "Estado",       "Tipo",           "Grupo_Base_Tensao", "Nome",
                      "Grupo_Limite_Tensao",    "Tensao",            "Angulo",       "Geracao_Ativa",  "Geracao_Reativa",   "Geracao_Reativa_Minima",
                      "Geracao_Reativa_Maxima", "Barra_Controlada",  "Carga_Ativa",  "Carga_Reativa",  "Shunt",             "Area",
                      "Tensao_Def_Carga",        "Modo_Visualizacao",]
        col_size =   [[0,5],                    [5,6],               [6,7],           [7,8],           [8,10],              [10,22],
                      [22,24],                  [24,28],             [28,32],         [32,37],         [37,42],             [42,47],
                      [47,52],                  [52,58],             [58,63],         [63,68],         [68,73],             [73,76],
                      [76,80],                  [80,81],]

        # Gerando a lista aninhada
        lista_dados = self.__get_transposed_list(miolo, col_size)
        # Obtendo dataframe
        df = pd.DataFrame(lista_dados, columns=cabecalhos)

        # Definindo alguns tipos de colunas
        df = df.astype({'Numero': int})

        return df

    def __get_codePWF_DLIN(self, miolo):
        # Lista de especificações
        cabecalhos = ["Barra_De",              "Estado_De",    "Operacao",               "Estado_Para",      "Barra_Para",       "Num_Circuito",
                      "Estado",                "Proprietario", "Manobravel",             "Resistencia",      "Reatancia",        "Susceptancia",
                      "Tap",                   "Tap_Minimo",   "Tap_Maximo",             "Defasagem",        "Barra_Controlada", "Capacidade_Normal",
                      "Capacidade_Emergencia", "Numero_Taps",  "Capacidade_Equipamento",]
        col_size =   [[0,5],                   [5,6],          [7,8],                    [9,10],             [10,15],            [15,17],
                      [17,18],                 [18,19],        [19,20],                  [20,26],            [26,32],            [32,38],
                      [38,43],                 [43,48],        [48,53],                  [53,58],            [58,64],            [64,68],
                      [68,72],                 [72,74],        [74,78]]
        # Gerando a lista aninhada
        lista_dados = self.__get_transposed_list(miolo, col_size)
        # Obtendo dataframe
        df = pd.DataFrame(lista_dados, columns=cabecalhos)

        # Definindo alguns tipos de colunas
        df = df.astype({'Barra_De': int, 'Barra_Para': int, 'Num_Circuito': int})

        return df

    def get_df_PWF(self, nome_arquivo):
        # Inicio dicionário contendo todos os dataframes
        dic_PWF = {}

        # Coleto dados do DBAR
        miolo = self.__get_content_codeANA(nome_arquivo, "DBAR", "99999")
        dic_PWF["DBAR"] = self.__get_codePWF_DBAR(miolo)

        # Coleto dados do DCIR
        miolo = self.__get_content_codeANA(nome_arquivo, "DLIN", "99999")
        dic_PWF["DLIN"] = self.__get_codePWF_DLIN(miolo)

        # # Coleto dados do DMUT
        # miolo = self.__get_content_codeANA(nome_arquivo, "DMUT", "99999")
        # dic_PWF["DMUT"] = self.__get_codeANA_DMUT(miolo)

        # # Coleto dados do DMOV
        # miolo = self.__get_content_codeANA(nome_arquivo, "DMOV", "99999")
        # dic_PWF["DMOV"] = self.__get_codeANA_DMOV(miolo)

        # # Coleto dados do DSHL
        # miolo = self.__get_content_codeANA(nome_arquivo, "DSHL", "99999")
        # dic_PWF["DSHL"] = self.__get_codeANA_DSHL(miolo)

        # # Coleto dados do DEOL
        # miolo = self.__get_content_codeANA(nome_arquivo, "DEOL", "99999")
        # dic_PWF["DEOL"] = self.__get_codeANA_DEOL(miolo)

        # # Coleto dados do DARE
        # miolo = self.__get_content_codeANA(nome_arquivo, "DARE", "99999")
        # dic_PWF["DARE"] = self.__get_codeANA_DARE(miolo)

        return dic_PWF
