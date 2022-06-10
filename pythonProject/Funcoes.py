
def caminho(escolha, texto):
    ambiguos = texto.ambiguidades()
    incompletude = texto.incompletude()
    contextualizados = texto.contextualizados()
    requisito = texto.requisitos()
    headings = ()
    Data = []
    if escolha == 1:
        headings = ("Nº Requisito", "Palavras Ambiguas", "Muitos Sinonimos", "Coordination Ambiguity", "Passive Voice")
        PA = ambiguos[0]['PA']
        AFL = ambiguos[0]['AFL']
        CA = ambiguos[1]['CA']
        PV = ambiguos[1]['PV']
        Data = []
        for i in range(len(requisito)):
            aux = []
            aux.append(i in PA)
            aux.append(i in AFL)
            aux.append(i in CA)
            aux.append(i in PV)
            if True in aux:
                Data.append((i + 1, aux))
            else:
                continue
    elif escolha == 2:
        headings = ("Nº Requisito", "Sentence Fragment", "Missing Subject", "Missing Verb Mistake", "Dummy Subject")
        SF = incompletude['SF']
        MS = incompletude['MS']
        MVM = incompletude['MVM']
        DS = incompletude['DS']
        for i in range(len(requisito)):
            aux = []
            aux.append(i in SF)
            aux.append(i in MS)
            aux.append(i in MVM)
            aux.append(i in DS)
            if True in aux:
                Data.append((i + 1, aux))
            else:
                continue
    elif escolha == 3:
        headings = ("Nº Requisito", "Contextualizados", "Completos")
        Contex = contextualizados['Contextualizados']
        Comple = contextualizados['Completos']
        Data = []
        for i in range(len(requisito)):
            aux = []
            aux.append(i in Contex)
            aux.append(i in Comple)
            if True in aux:
                Data.append((i + 1, aux))
            else:
                continue
        print(Data)
    return [Data, headings]
def tratar_requisitos(f):
    mensagem = ""
    for linha_arq in f:
        frase = ""
        for i in range(len(linha_arq)):
            frase += chr(linha_arq[i])
        mensagem += frase
    f.close()
    mensagem = mensagem.split('\n')
    return mensagem
