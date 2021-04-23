import random
import math
import csv
import copy

cidades_nome = ["Santa Paula",
"Campos",
"Riacho de Fevereiro",
"Algas","Além-do-Mar",
"Guardião",
"Foz da Água Quente",
"Leão",
"Granada",
"Lagos",
"Ponte-do-Sol",
"Porto",
"Limões"]

with open('cidades.csv', newline='') as f:
  reader = csv.reader(f)
  cidades = list(reader)

with open('itens.csv', newline='') as f:
  reader = csv.reader(f)
  itens = list(reader)

# ---------------------------- FUNÇÕES ----------------------------
# -----------------------------------------------------------------
def calcular(cidAnterior, cidAtual):
  tempo_roubos = 0
  valor_roubo = 0
  peso_roubos = 0 

  tempo_viagens = 0
  custo_viagens = 0

  for i in range(0, len(itens) - 1):
    if itens[i][4] == cidAtual:
      peso_roubos += int(itens[i][1])
      tempo_roubos += int(itens[i][2])
      valor_roubo += int(itens[i][3])

  for i in range(0, len(cidades) - 1):
    if (cidades[i][0] == cidAnterior and cidades[i][1] == cidAtual) or (cidades[i][1] == cidAnterior and cidades[i][0] == cidAtual):
      tempo_viagens += int(cidades[i][2])
      custo_viagens += int(cidades[i][3])

  return peso_roubos, (tempo_roubos + tempo_viagens), (valor_roubo - custo_viagens)

# -----------------------------------------------------------------

def inicializacao():
  individuo = ['Escondidos']
  limite_tempo = 72
  limite_peso = 20
  valor = 0

  while True:
    possibilidades_validas = []
    
    possibilidades_validas = [item for item in cidades_nome if item not in individuo]
    if possibilidades_validas:
      cidade_atual = individuo[-1]
      prox_cidade = random.choice(possibilidades_validas)

      peso, tempo, valor = calcular(cidade_atual, prox_cidade)
      limite_peso -= peso
      limite_tempo -= tempo
      individuo.append(prox_cidade)

    if limite_tempo <= 9 or not possibilidades_validas:
      for i in range(0, len(cidades) - 1):
        if cidades[i][0] == "Escondidos" and cidades[i][1] == prox_cidade:
          limite_tempo -= int(cidades[i][2])  
          valor -= int(cidades[i][3])

      individuo.append('Escondidos')
      break

  return individuo

# -----------------------------------------------------------------

def fitnessa(individuo):
  fit = 0
  peso_limite = 20
  tempo_limite = 72

  peso_atual = 0
  tempo_atual = 0
  valor_atual = 0

  for i in range(0,len(individuo)-1):
    peso, tempo, valor = calcular(individuo[i], individuo[i+1])
    peso_atual += peso
    tempo_atual += tempo
    valor_atual += valor

  peso_limite -= peso_atual
  tempo_limite -= tempo_atual

  ## --- FITNESS ---

  ## BOLSA
  if (peso_limite <= -5):
    fit -= 10000
  elif (peso_limite < 0 and peso_limite > -5):
      #peso ultrapassou limite
      fit -= 3000
  elif (peso_limite >= 0 and peso_limite <= 4):
      #sobrou entre 0kg e 4kg de peso
      fit += 1750
  elif (peso_limite >= 5 and peso_limite <= 13): 
      #sobrou entre 5kg e 13
      fit += 1000

    ## TEMPO
  if (tempo_limite <= -4):
      fit -= 20000
  elif (tempo_limite < 0):
      fit -= 3000
  elif (tempo_limite >= 0 and tempo_limite <= 10):
      fit += 1500
  elif (tempo_limite >= 11 and tempo_limite <= 19):
      fit += 1100
  elif (tempo_limite > 20):
      fit += 500

  ## VALOR ARRECADADO
  fit += valor_atual

  return fit

# -----------------------------------------------------------------

def mutacao(individuo, taxa):
  qtd_genes =  math.ceil(len(individuo) * taxa)
  individuo_mutado = list(individuo)
  for _ in range(qtd_genes):
    possibilidades = [item for item in cidades_nome if item not in individuo_mutado]
    gene = random.choice(range(1,len(individuo)-2))
    i = random.choice(range(0,len(possibilidades)-1))
    individuo_mutado[gene] = possibilidades[i]

  return individuo_mutado

# -----------------------------------------------------------------

def crossover(populacao):
  pop = copy.deepcopy(populacao)
  parte1 = []
  parte2 = []
  crossovers = []
  for individuo in pop:
    parte1.append(individuo[1:4])
    parte2.append(individuo[4:-1])
  bestParts = selecionarIndividuos(parte1 + parte2)

  for i in range(1, len(bestParts) - 1):
    cities = [item for item in bestParts[i] if item not in bestParts[i - 1]]
    if cities:
      lista = bestParts[i - 1] + cities
      lista.insert(0, "Escondidos")
      lista.append("Escondidos")
      if lista not in populacao and lista not in crossovers:
        crossovers.append(lista)
    cities = [item for item in bestParts[i - 1] if item not in bestParts[i]]
    if cities:
      lista = bestParts[i] + cities
      lista.insert(0, "Escondidos")
      lista.append("Escondidos")
      if lista not in populacao and lista not in crossovers:
        crossovers.append(lista)

  crossovers = selecionarIndividuos(crossovers)

  return crossovers

# -----------------------------------------------------------------

def getDados(individuo):
  peso_limite = 20 #peso da bolsa com os itens X
  tempo_limite = 72 #tempo restante da viagem
  valor_total = 0

  peso_atual = 0
  tempo_atual = 0
  valor_atual = 0

  #verifica o peso da mochila e atualiza seu limite
  #soma o tempo dos roubos
  #soma o valor arrecadado nos roubos
  for i in range(0,len(individuo)-1):
    peso, tempo, valor = calcular(individuo[i], individuo[i+1])
    peso_atual += peso
    tempo_atual += tempo
    valor_atual += valor

  peso_limite -= peso_atual
  tempo_limite -= tempo_atual
  valor_total = valor_atual

  print("Tamanho da rota -> ", len(individuo))
  print("Tempo restante ->", tempo_limite, "horas")
  print("Peso na bolsa restante ->", peso_limite, "kg")
  print("Valor arrecadado -> $", valor_total)

# -----------------------------------------------------------------

def selecionarIndividuos(listaIndividuos):
  selecionados = sorted(listaIndividuos, key=fitnessa, reverse=True)
  return selecionados[0:50]

# -----------------------------------------------------------------

populacao = [inicializacao() for _ in range(0,50)]
geracoes=0
popIgual=0
verGer = False

print("~~~~~~~~ Bem vindo ao Maximizador-de-Roubos-AIC ~~~~~~~~")

print("Você gostaria de assistir a evolução das gerações?")
escolha = input("(Digite \"S\" para sim, ou qualquer outra entrada para não): ")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
if escolha == "s" or escolha == "S":
  verGer = True
  print("")
else:
  print("\nAguarde!")

while True: 
  if(popIgual == 100): break

  if geracoes % 10 == 0 and verGer:
    print(f'{"Geração ":^8}{str(geracoes):^4}{", Melhor Fitness: ":^11}{str(fitnessa(populacao[0])):^5}')
  elif geracoes % 20 == 0 and not verGer:
    print('.', end='', flush=True)

  populacao_antiga = copy.deepcopy(populacao)
  populacao_mutada = [mutacao(individuo, 0.3) for individuo in populacao]
  populacao_crossover = crossover(populacao_mutada + populacao)
  populacao = selecionarIndividuos(populacao_antiga + populacao_mutada + populacao_crossover)
  
  if populacao_antiga == populacao: popIgual += 1
  else: popIgual=0

  geracoes+=1


populacao = selecionarIndividuos(populacao)
print("\n\n~~~~~~~~ Resultados ~~~~~~~\n")
print("Melhor rota encontrada:")
print(populacao[0])
print("\nGerações ->", str(geracoes), "\nFitness ->", str(fitnessa(populacao[0])))
getDados(populacao[0])