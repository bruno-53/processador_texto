import unicodedata,requests,string
from validate_docbr import CPF,CNPJ

def abrir_texto(arquivo):
    arquivo_texto = open(arquivo,'r',encoding="utf8")
    arquivo_texto = arquivo_texto.read()
    arquivo_texto = unicodedata.normalize("NFD",arquivo_texto).encode("ascii", "ignore").decode("utf-8").translate(str.maketrans('','',string.punctuation)).upper()
    palavras = arquivo_texto.split()
    return palavras

def processar_texto(texto):
    #DECLARAÇÃO DE VÁRIAVEIS E ABERTURA DO ARQUIVO DE RESULTADOS
    arquivo_resultado = open('resultado.txt','w',encoding="utf8")
    resultado = []
    resultado.append('TOTAL DE PALAVRAS DO TEXTO: {}\n'.format(len(texto)))

    contador = {}
    numeros = []
    cpf = []
    cnpj = []
    cep = []
    telefone_celular_ddd = []
    telefone_celular =[]
    telefone_fixo_ddd = []
    telefone_fixo = []

    #INÍCIO VARREDURA E SEAPARAÇÃO DO TEXTO
    palavras_ignoradas = [
        'UM', 'SER', 'IR', 'ESTAR', 'TER', 'HAVER', 'FAZER', 'DAR', 'FICAR', 'PODER', 'VER', 'NAO', 'MAIS', 'MUITO',
        'JA','QUANDO', 'MESMO', 'DEPOIS', 'AINDA', 'DOIS', 'PRIMEIRO', 'CEM', 'MIL', 'A', 'O', 'UMA', 'DE', 'EM','PARA',
        'POR', 'COM', 'ATE', 'E', 'MAS', 'OU', 'TAMBEM', 'SE', 'ASSIM', 'COMO', 'PORQUE', 'QUE', 'EU', 'VOCE', 'ELE',
        'ESTE','ESSE', 'ISSO', 'SUA', 'AI', 'AH', 'AU', 'UI', 'HUM', ';', '.', ',','DO','AS','AO','DA','DAS','OS',
        'NO','ELA','NA']
    top = 0
    for palavra in texto:
        if (palavra not in contador) and (palavra not in palavras_ignoradas):
            contador[palavra] = 1
            if palavra.isdigit():
                numeros.append(palavra)
        elif palavra not in palavras_ignoradas:
            contador[palavra] +=1
    resultado.append('TOTAL DE SEQUÊNCIAS NUMÉRICAS ENCONTRADOS NO TEXTO: {}\n'.format(len(numeros)))
    resultado.append('---------------------------------\n')
    resultado.append('- 10 PALAVRAS QUE MAIS APARECEM -\n')
    resultado.append('---------------------------------\n')

    for palavra in sorted(contador,key=contador.get,reverse=True):
        top += 1
        if top <= 10:
            resultado.append('TOP {} -- {} : {} \n'.format(top,palavra,contador[palavra]))

    #INÍCIO PROCESSAMENTO DE NÚMEROS DO TEXTO
    resultado.append('---------------------------------------------------------\n')
    resultado.append('- INFORMAÇÕES SOBRE AS SEQUÊNCIAS NUMÉRICAS ENCONTRADAS -\n'.format(len(numeros)))
    resultado.append('---------------------------------------------------------\n')

    for numero in numeros:
        if len(numero) == 11:
            if CPF().validate(numero):
                cpf.append(numero)
                resultado.append('Esse é um CPF válido encontrado no texto: {}\n'.format((CPF().mask(numero))))
            else: #celular + ddd
                telefone_celular_ddd.append(numero)
                resultado.append('Esse talvez seja um celular com DDD {}\n'.format(numero))

        elif len(numero) == 14:
            if CNPJ().validate(numero):
                cnpj.append(numero)
                resultado.append('Esse é um CNPJ válido encontrado no texto: {}\n'.format((CNPJ().mask(numero))))
        elif len(numero) == 8:
            url = requests.get('https://viacep.com.br/ws/{}/json/'.format(numero))
            dados = url.json()
            try:
                if dados['erro'] == True:
                    telefone_fixo.append(numero)
                    resultado.append('Esse talvez seja um telefone fixo sem DDD: {}\n'.format(numero))
            except:
                cep.append(numero)
                cep_f = "{}-{}".format(numero[:5], numero[5:])
                resultado.append('Esse é um CEP válido encontrado no texto: {}, da cidade de {} - {}\n'.format(cep_f,dados['localidade'],dados['uf']))

        elif len(numero) == 9:
            telefone_celular.append(numero)
            resultado.append('Esse talvez seja um celular sem DDD: {}\n'.format(numero))

        elif len(numero) == 10:
            telefone_fixo_ddd.append(numero)
            resultado.append('Esse talvez seja um tel fixo com DDD: {}\n'.format(numero))

    arquivo_resultado.writelines(resultado)
    arquivo_resultado.close()

