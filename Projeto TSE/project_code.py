from email.headerregistry import ContentDispositionHeader
import os
from datetime import datetime, date
import voto

NOME = 0
MAE = 1
PAI = 2
NASCIMENTO = 3
TITULO = 4
VOTOU = 5
CIDADE = 6
ZONA = 7
SECAO =8
UF = 9
DATA_DOMICILIO = 10
ANO_ATUAL = 2022


substituicoes = ['$NOME$', 
    '$MAE$', 
    '$PAI$',   
    '$NASC$', 
    '$TITULO$',
    '$CIDADE$',
    '$ZONA$',
    '$SEC$',
    '$UF$',
    '$DATA_DOMICILIO$']

def solicitar_dados():
    nome= input('Nome: ')
    mae= input('Nome da Mãe: ')
    pai= input('Nome do Pai: ')
    nascimento= input('Data de Nascimento: ')
    titulo= input('Título de eleitor: ')
    cidade= input('Cidade: ')
    zona= input('Zona Eleitoral:: ')
    secao= input('Seção Eleitoral: ')
    uf= input('UF: ')
    data_domicilio= input('Data Domicilio: ')
    votou= input('Votou na última eleição? (S/N): ')
    votou = votou.upper()
    dados = (nome, mae, pai, nascimento, titulo, cidade, zona, secao, uf, data_domicilio, votou) #Colocamos tudo em uma tupla
    return dados

def criar_base_dados(caminho):
    # nome mae pai	data_nasc titulo votou
    colunas = ['nome', 'mae', 'pai', 'data_nasc', 'titulo', 'cidade', 'zona', 'secao', 'uf', 'data_domicilio', 'votou'] 

    arquivo = open(caminho, 'w')
    linha = ','.join(colunas) #Juntando as colunas e separando por virgula de acordo com o formato CSV
    arquivo.write(linha + '\n') #escrevendo a linha toda e pula uma linha
    arquivo.close()

def cadastrar_eleitor(dados, caminho): #Dados é a tupla que o usuario inseriu e o caminho é o caminho do arquivo
    arquivo = open(caminho, 'a') #a é para adicionar, append, se colocassemos w ele sobreescreveria
    arquivo.write(','.join(dados) + '\n') #adicionando os dados e pulando uma linha
    arquivo.close()
    print('Eleitor Cadastrado com sucesso!\n')

def solicitar_dados_busca(caminho):
    nome= input('Nome: ')
    titulo= input('Título de eleitor: ')
    dados = (nome, titulo) #Colocamos tudo em uma tupla
    return dados

def localizar_eleitor(dados, caminho):
    arquivo = open(caminho)
    linhas = arquivo.readlines()
    arquivo.close
    for linha in linhas:
        dados_eleitor = linha.strip().split(',')
        if (dados[0] == dados_eleitor[NOME] 
            and dados[1] == dados_eleitor[TITULO]): #Aqui estamos verificando se o nome e título são iguais, dentro da iteração FOR que vai em todas as linhas
            #encontramos o usuarios na base de dados
            return dados_eleitor
    #nao encontramos o usuario            
    return []

#procurando o arquivo que vamos usar e caso nao exista vamos criar
caminho = 'eleitores.csv'
if not os.path.exists(caminho):
    criar_base_dados('eleitores.csv')

# dados_eleitor = solicitar_dados()
# cadastrar_eleitor(dados_eleitor, 'eleitores.csv')

#Solicitar dados pra buscar na base
dados = solicitar_dados_busca(caminho)
dados_eleitor = localizar_eleitor(dados, caminho)
if dados_eleitor:
    print(dados_eleitor)
    data_nascimento = dados_eleitor[NASCIMENTO]
    #Formatando a data para ['dd', 'mm', 'aaaa']
    partes = data_nascimento.split('/')
    partes = [int(d) for d in partes]
    data = date(day=partes[0], month=partes[1], year=partes[2])
    idade = int((date.today() - data).days/365)



    if voto.situacao_voto(idade) == voto.PROIBIDO:
        print (f'Com {idade} anos, seu voto é proibido')
    elif (voto.situacao_voto(idade) == voto.OBRIGATORIO 
        and dados_eleitor[VOTOU] == 0):
        print ('VOOCÊ NÃO ESTA QUITE COM A JUSTIÇA ELEITORAL')
    else:
        arquivo = open('certidao.html', 'r')
        conteudo = arquivo.read()
        arquivo.close()

        for i in range (len(substituicoes)): #Substituindo o conteudo
            conteudo = conteudo.replace(substituicoes[i], 
                                        dados_eleitor[i])

        #Substituindo DATA e HORA(
        agora = datetime.now()
        data_ok = str(agora.date().strftime('%d/%m/%Y'))
        hora_ok = str(agora.time().strftime('%H:%M:%S'))
        conteudo = conteudo.replace('$DATA$', data_ok)
        conteudo = conteudo.replace('$HORA$', hora_ok)
        arquivo = open('certidao_emitida.html', 'w')
        arquivo.write(conteudo)
        arquivo.close()
else: 
    print('Eleitor não cadastrado(a)')

