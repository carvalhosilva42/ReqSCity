import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

def tratamentoOntologiaCidadesInteligentes():
    dicionario_cidadesInteligentes = ""
    dicionario_arquivo_cidadesInteligentes = open("m3.owl", "r")
    for linha_dicionario in dicionario_arquivo_cidadesInteligentes:
        dicionario_cidadesInteligentes += linha_dicionario
    dicionario_arquivo_cidadesInteligentes.close()

    dicionario_cidadesInteligentes = nltk.word_tokenize(dicionario_cidadesInteligentes)

    list_palavras_cidadesInteligentes = []
    for i in range(len(dicionario_cidadesInteligentes)):
        if (dicionario_cidadesInteligentes[i] == 'Class'):
            aux = dicionario_cidadesInteligentes[i + 3]
            palavra = ''
            for i in range(len(aux)):
                if i == 0:
                    palavra += aux[i]
                else:
                    if aux[i].isupper():
                        palavra += ' '
                        palavra += aux[i]
                    else:
                        palavra += aux[i]
            list_palavras_cidadesInteligentes.append(palavra.lower())
    return (list_palavras_cidadesInteligentes)
class AmbiguidadeLexica:
    def __init__(self, tokens, dicionario, POS):
        self.tokens = tokens
        self.ambiguos_lexicos = {"PA": [], "AFL": []}
        self.dicionario=dicionario
        self.POS=POS
    def palavras_ambiguas(self):
        for i in range(len(self.tokens)):
            for j in self.dicionario:
                if j.lower() in self.tokens[i]:
                    self.ambiguos_lexicos["PA"].append(i)
    def limpeza(self):
        limpo = []
        sw = stopwords.words('english')
        especiais = ['.', '?', '!', ':', '-', '...', ',', ';', '""', '()', '#']
        for req in self.POS:
            words = []
            for word in req:
                if (word[0] in sw) or (word[0] in especiais):
                    continue
                else:
                    words.append(word)
            limpo.append(words)
        return limpo
    def objetoWN(self,pos):
        #Possibilidade de usar uma hashmap
        if pos == 'V':
            return wn.VERB
        elif pos == 'N':
            return wn.NOUN
        elif pos == 'R':
            return wn.ADV
        elif pos == 'J':
            return wn.ADJ
        else:
            return wn.NOUN
    def algoritmo_flex_amb(self):
        LIMIAR_MIN = 3 / 4
        QTDE_SIM = 2
        limpo = self.limpeza()
        for i in range(len(limpo)):
            qtde = len(limpo[i])
            possiveis = []
            for req in limpo[i]:
                if len(wn.synsets(req[0], pos=self.objetoWN(req[1][0]))) > QTDE_SIM:
                    possiveis.append(req[0])
            if len(possiveis) >= (LIMIAR_MIN * qtde):
                self.ambiguos_lexicos["AFL"].append(i)

    def requisitos_ambiguos(self):
        self.palavras_ambiguas()
        self.algoritmo_flex_amb()
        return self.ambiguos_lexicos
    def requisitos_ambiguos(self):
        self.palavras_ambiguas()
        self.algoritmo_flex_amb()
        return self.ambiguos_lexicos

class AmbiguidadeSintatica:
    def __init__(self, tokens, POS):
        self.tokens = tokens
        self.POS=POS
        self.ambiguos_sintaticos={"CA": [], "PV": []}

    def coordination_ambiguity(self):
        param1='JJNNSCC'
        param2='CCNNSCC'
        ambiguos=[]
        for i in range(len(self.POS)):
            aux = ''
            for j in self.POS[i]:
                aux+=j[1]
            if (param1 in aux) or (param2 in aux):
                ambiguos.append(i)
        self.ambiguos_sintaticos["CA"]=ambiguos
    def passive_voice(self):
        params=['VBZVBN','VBPVBN','VBZVBGVBN','VBPVBGVBN','VBDVBN','VBZVBN','VBDVBGVBN','VBZVBNVBN','VBPVBNVBN','VBDVBNVBN','MDVBVBN','MDVBVBNVBN']
        ambiguos=[]
        for i in range(len(self.POS)):
            aux = ''
            for j in self.POS[i][3:6]:
                aux+=j[1]
            for param in params:
                if param in aux:
                    ambiguos.append(i)

        self.ambiguos_sintaticos["PV"]=set(ambiguos)

    def requisitos_ambiguos(self):
        self.coordination_ambiguity()
        self.passive_voice()
        return self.ambiguos_sintaticos

class Incompletude:
    def __init__(self, POS):
        self.POS=[]
        for req in POS:
            self.POS.append(req)
        self.incompletudes={'SF': [],'MS':[],'MVM': [],'DS':[]}
    def verificar_incompletudes(self):
        regras_SF=['VB','VBN','VBD','VBG','SF','VBP','VBZ']
        regras_MS_MSM=['VB','VBN','VBD','VBG','VBP','VBZ','MD', 'JJ']
        for i,classes in enumerate(self.POS):
            #Sentence Fragment
            if (classes[-2][1] in regras_SF):
                self.incompletudes['SF'].append(i)
            #Missing Subject
            if (classes[0][1] in regras_MS_MSM):
                self.incompletudes['MS'].append(i)
            #Missing Verb Mistake
            countVerbo = 0
            for j in range(len(classes)):
                if (classes[j][1] in regras_MS_MSM):
                    countVerbo += 1
            if countVerbo == 0:
                self.incompletudes['MVM'].append(i)
            #Dummy Subject
            if (classes[0][0] == 'it' or classes[0][0] == 'there'):
                self.incompletudes['DS'].append(i)
    def requisitos_incompletos(self):
        self.verificar_incompletudes()
        return self.incompletudes

#Nome da Classe e definição de regras mais satisfatórias
class Completude:
    def __init__(self, tokens, palavras_smart_cities,sensores):
        self.tokens=tokens
        self.palavras_sc=palavras_smart_cities
        self.sensores=sensores
        self.contextualizados={"Contextualizados":[], "Completos":[]}
    def contextualiza(self):
        for i in range(len(self.tokens)):
            for k in range(len(self.tokens[i])):
                for j in range(len(self.palavras_sc)):
                    if (self.palavras_sc[j] in self.tokens[i][k]):
                        if i not in self.contextualizados["Contextualizados"]:
                            self.contextualizados["Contextualizados"].append(i)
    def completude(self):
    # casos para analise:
        # 1 - Sensor sem definição do sensor
        for i in self.contextualizados["Contextualizados"]:
            palavras = self.tokens[i]
            for j in range(len(palavras)):
                if (palavras[j] == "sensor" or palavras[j] == "sensors"):
                    if not ((palavras[j + 1] in self.sensores) or (palavras[j - 1] in self.sensores)):
                        if i not in self.contextualizados["Completos"]:
                            self.contextualizados["Completos"].append(i)
    def retorna_completos(self):
        self.contextualiza()
        self.completude()
        return self.contextualizados
class Texto:
    def __init__(self, texto):
        self.texto=texto
        self.tokens = []
        self.POS=[]
        for i in self.texto:
            i=i.lower()
            tokens=nltk.word_tokenize(i)
            self.tokens.append(tokens)
            self.POS.append(nltk.pos_tag(tokens))
        dicionario = ""
        dicionario_arquivo = open("dicionario_base.txt", "r")
        for linha_dicionario in dicionario_arquivo:
            dicionario += linha_dicionario
        dicionario_arquivo.close()
        dicionario = nltk.word_tokenize(dicionario)
        self.dicionario = dicionario
        sensores = ""
        sensores_arquivo = open("sensores.txt", "r")
        for linha_sensores in sensores_arquivo:
            sensores+=linha_sensores
        self.sensores = sensores.split('\n')

    def requisitos(self):
        return self.texto
    def tokeniza(self):
        return self.tokens
    def etiqueta(self):
        return self.POS
    def ambiguidades(self):
        if 'ambiguos_lexicos' not in self.__dict__:
            self.ambiguos_lexicos=AmbiguidadeLexica(self.tokens,self.dicionario, self.POS)
        if 'ambiguos_sintaticos' not in self.__dict__:
            self.ambiguos_sintaticos=AmbiguidadeSintatica(self.tokens,self.POS)
        return self.ambiguos_lexicos.requisitos_ambiguos(),self.ambiguos_sintaticos.requisitos_ambiguos()
    def incompletude(self):
        if 'incompletos' not in self.__dict__:
            self.incompletos=Incompletude(self.POS)
        return self.incompletos.requisitos_incompletos()
    def contextualizados(self):
        if 'contextualizados' not in self.__dict__:
            palavras=tratamentoOntologiaCidadesInteligentes()
            self.contextualizados=Completude(self.tokens,palavras,self.sensores)
        return self.contextualizados.retorna_completos()