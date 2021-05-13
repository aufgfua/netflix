import json
import csv
import pickle
import math
import eel
from trie import *
from abp import *


## OBRIGATORIO PRA EXECUTAR
eel.init('web')


file_ator_abp = 'abp_ator'
file_diretor_abp = 'abp_diretor'
file_filme_abp = 'abp_filme'

file_ator = 'lista_ator'
file_diretor = 'lista_diretor'
file_filme = 'lista_filme'

file_matriz_filme_ator = 'matriz_filme_ator'
file_matriz_filme_diretor = 'matriz_filme_diretor'

file_trie_filme = 'trie_filme'
file_trie_ator = 'trie_ator'
file_trie_diretor = 'trie_diretor'

try:
    infile = open(file_ator, 'rb')
    actors_list = pickle.load(infile)
    infile.close()

    infile = open(file_diretor, 'rb')
    directors_list = pickle.load(infile)
    infile.close()

    infile = open(file_filme, 'rb')
    films_list = pickle.load(infile)
    infile.close()

    infile = open(file_matriz_filme_ator, 'rb')
    matriz_filme_ator = pickle.load(infile)
    infile.close()

    infile = open(file_matriz_filme_diretor, 'rb')
    matriz_filme_diretor = pickle.load(infile)
    infile.close()

    

    infile = open(file_trie_ator, 'rb')
    actor_trie = pickle.load(infile)
    infile.close()


    infile = open(file_trie_diretor, 'rb')
    director_trie = pickle.load(infile)
    infile.close()


    infile = open(file_trie_filme, 'rb')
    film_trie = pickle.load(infile)
    infile.close()



    infile = open(file_ator_abp, 'rb')
    actors_abp = pickle.load(infile)
    infile.close()

    infile = open(file_diretor_abp, 'rb')
    directors_abp = pickle.load(infile)
    infile.close()

    infile = open(file_filme_abp, 'rb')
    films_abp = pickle.load(infile)
    infile.close()

# Se tiver erro ao abrir os arquivos, eles nao foram criados ainda.
except FileNotFoundError:
    csv_original = "info_netflix.csv"
    f = open(csv_original, 'r')
    csv_f = csv.reader(f)
    next(csv_f, None)  # pula o header

    # Lists
    actors_list = []
    directors_list = []
    films_list = []

    # Matrices
    matriz_filme_ator = {}
    matriz_filme_diretor = {}

    # Tries
    film_trie = Trie()
    actor_trie = Trie()
    director_trie = Trie()

    for row in csv_f:
        netflix_id = int(row[0])
        title = row[1]

        directors_string = row[2]
        directors_in_row = directors_string.split(',')

        actors_string = row[3]
        actors_in_row = actors_string.split(',')

        release_year = row[4]
        duration = row[5]


        data_filme = {}
        data_filme['nome'] = title
        data_filme['ano'] = release_year
        data_filme['dur'] = duration
        data_filme['id'] = netflix_id

        films_list.append(data_filme)

        for actor in actors_in_row:
            if actor.strip() not in actors_list:
                actors_list.append(actor.strip())
                actor_trie.insert(actor.strip(), len(actors_list) - 1)

        for director in directors_in_row:
            if director.strip() not in directors_list:
                directors_list.append(director.strip())
                director_trie.insert(director.strip(), len(directors_list) - 1)

        list_id_actors_in_this_movie = []
        list_id_directors_in_this_movie = []

        for actor in actors_in_row:
            list_id_actors_in_this_movie.append(actors_list.index(actor.strip()))

        for director in directors_in_row:
            list_id_directors_in_this_movie.append(directors_list.index(director.strip()))

        film_trie.insert(title, netflix_id)

        matriz_filme_ator[netflix_id] = list_id_actors_in_this_movie
        matriz_filme_diretor[netflix_id] = list_id_directors_in_this_movie

        

    f.close()

    
    actors_abp = createAbp(actors_list)
    directors_abp = createAbp(directors_list)
    films_abp = createAbp_FILME(films_list)

    salvaTudo()



def salvaTudo():

    # Salvando as listas
    outfile = open(file_ator, 'wb')
    pickle.dump(actors_list, outfile)
    outfile.close()

    outfile = open(file_diretor, 'wb')
    pickle.dump(directors_list, outfile)
    outfile.close()

    outfile = open(file_filme, 'wb')
    pickle.dump(films_list, outfile)
    outfile.close()

    # Salvando as matrizes
    outfile = open(file_matriz_filme_ator, 'wb')
    pickle.dump(matriz_filme_ator, outfile)
    outfile.close()

    outfile = open(file_matriz_filme_diretor, 'wb')
    pickle.dump(matriz_filme_diretor, outfile)
    outfile.close()

    # Salvando as TRIEs
    outfile = open(file_trie_ator, 'wb')
    pickle.dump(actor_trie, outfile)
    outfile.close() 

    outfile = open(file_trie_diretor, 'wb')
    pickle.dump(director_trie, outfile)
    outfile.close()

    outfile = open(file_trie_filme, 'wb')
    pickle.dump(film_trie, outfile)
    outfile.close()


    outfile = open(file_ator_abp, 'wb')
    pickle.dump(actors_abp, outfile)
    outfile.close()

    outfile = open(file_diretor_abp, 'wb')
    pickle.dump(directors_abp, outfile)
    outfile.close()
    
    outfile = open(file_filme_abp, 'wb')
    pickle.dump(films_abp, outfile)
    outfile.close()













@eel.expose
def pesquisaFilmePy (nome) :
    dados = film_trie.query(nome)

    filmes_pesquisados = []

    if len(dados) <= 0:
        eel.populaTabelaJs("FALSE")
    else:
        for filme_tupla in dados:
            filmes = films_abp.Find_Node(filme_tupla[2])

            if isinstance(filmes, str) and upper(filmes) == "FALSE":
                continue
            filmes = filmes['data']
            obj = {}
            obj['nome'] = filmes['nome']
            obj['ano'] = filmes['ano']
            obj['dur'] = filmes['dur']
            obj['id'] = filmes['id']
            
            diretores_filme = []
            lista_ids_diretores = matriz_filme_diretor[obj['id']]

            
            for diretor in lista_ids_diretores:
                diretor_nome = directors_abp.Find_Node(diretor)['data']
                diretores_filme.append(diretor_nome)


            atores_filme = []
            lista_ids_ator = matriz_filme_ator[obj['id']]

            for ator in lista_ids_ator:
                ator_nome = actors_abp.Find_Node(ator)['data']
                atores_filme.append(ator_nome)


            obj['atores'] = atores_filme
            obj['diretores'] = diretores_filme

            filmes_pesquisados.append(obj)
        
        JSON_filme = json.dumps(filmes_pesquisados)

        #eel.printa(JSON_filme)

        eel.populaTabelaJs(JSON_filme)















@eel.expose
def pesquisaAtorPy (nome) :
    dados = actor_trie.query(nome)

    atores_pesquisados = []

    if len(dados) <= 0:
        eel.populaTabelaJs("FALSE")
    else:
        filmes_dos_atores = {}
        for ator_tupla in dados:
            id_ator = ator_tupla[2]


            for filme in matriz_filme_ator:
                if id_ator in matriz_filme_ator[filme]:
                    filmes_dos_atores[filme] = filme

        filmes_pesquisados = []
        for filme_idx in filmes_dos_atores:
            filmes = films_abp.Find_Node(filme_idx)

            if isinstance(filmes, str) and upper(filmes) == "FALSE":
                continue
            filmes = filmes['data']
            obj = {}
            obj['nome'] = filmes['nome']
            obj['ano'] = filmes['ano']
            obj['dur'] = filmes['dur']
            obj['id'] = filmes['id']
            
            diretores_filme = []
            lista_ids_diretores = matriz_filme_diretor[obj['id']]

            
            for diretor in lista_ids_diretores:
                diretor_nome = directors_abp.Find_Node(diretor)['data']
                diretores_filme.append(diretor_nome)


            atores_filme = []
            lista_ids_ator = matriz_filme_ator[obj['id']]

            for ator in lista_ids_ator:
                ator_nome = actors_abp.Find_Node(ator)['data']
                atores_filme.append(ator_nome)


            obj['atores'] = atores_filme
            obj['diretores'] = diretores_filme

            filmes_pesquisados.append(obj)
        
        JSON_filme = json.dumps(filmes_pesquisados)

        #eel.printa(JSON_filme)

        eel.populaTabelaJs(JSON_filme)





@eel.expose
def removerPy(id):
    filme_rem = films_abp.Find_Node(int(id))['data']

    film_trie.delete(filme_rem['nome'])

    del matriz_filme_diretor[filme_rem['id']]
    del matriz_filme_ator[filme_rem['id']]

    
    # Salvando as matrizes
    outfile = open(file_matriz_filme_ator, 'wb')
    pickle.dump(matriz_filme_ator, outfile)
    outfile.close()

    outfile = open(file_matriz_filme_diretor, 'wb')
    pickle.dump(matriz_filme_diretor, outfile)
    outfile.close()

    outfile = open(file_trie_filme, 'wb')
    pickle.dump(film_trie, outfile)
    outfile.close()






@eel.expose
def pesquisaDiretorPy (nome) :
    dados = director_trie.query(nome)

    diretores_pesquisados = []

    if len(dados) <= 0:
        eel.populaTabelaJs("FALSE")
    else:
        filmes_dos_diretores = {}
        for diretor_tupla in dados:
            id_diretor = diretor_tupla[2]


            for filme in matriz_filme_diretor:
                if id_diretor in matriz_filme_diretor[filme]:
                    filmes_dos_diretores[filme] = filme

        filmes_pesquisados = []
        for filme_idx in filmes_dos_diretores:
            filmes = films_abp.Find_Node(filme_idx)

            if isinstance(filmes, str) and upper(filmes) == "FALSE":
                continue
            filmes = filmes['data']
            obj = {}
            obj['nome'] = filmes['nome']
            obj['ano'] = filmes['ano']
            obj['dur'] = filmes['dur']
            obj['id'] = filmes['id']
            
            diretores_filme = []
            lista_ids_diretores = matriz_filme_diretor[obj['id']]

            
            for diretor in lista_ids_diretores:
                diretor_nome = directors_abp.Find_Node(diretor)['data']
                diretores_filme.append(diretor_nome)


            atores_filme = []
            lista_ids_ator = matriz_filme_ator[obj['id']]

            for ator in lista_ids_ator:
                ator_nome = actors_abp.Find_Node(ator)['data']
                atores_filme.append(ator_nome)


            obj['atores'] = atores_filme
            obj['diretores'] = diretores_filme

            filmes_pesquisados.append(obj)
        
        JSON_filme = json.dumps(filmes_pesquisados)

        #eel.printa(JSON_filme)

        eel.populaTabelaJs(JSON_filme)




@eel.expose
def inserirFilmePy(nome, dur, ano, atores, diretores):
    atores = atores.split(';')
    diretores = diretores.split(';')

    atores_ids =  []
    diretores_ids = []

    for ator in atores:
        retorno = actor_trie.query(ator)
        print(retorno)
        if len(retorno) != 1:
            novo_id = novoId(actors_abp)
            nodo = {"id": novo_id, "data": ator}
            print(nodo)
            actors_abp.Add_Node(nodo)
            actor_trie.insert(ator, novo_id)
            atores_ids.append(novo_id)
        else:
            atores_ids.append(retorno[2])



    for diretor in diretores:
        retorno = director_trie.query(diretor)
        print(retorno)
        if len(retorno) != 1:
            novo_id = novoId(directors_abp)
            nodo = {"id": novo_id, "data": diretor}
            print(nodo)
            directors_abp.Add_Node(nodo)
            director_trie.insert(ator, novo_id)
            diretores_ids.append(novo_id)
        else:
            diretores_ids.append(retorno[2])



    retorno = film_trie.query(nome)
    print(retorno)
    if len(retorno) != 1:
        #NOVO FILME
        novo_id = novoId(films_abp)
        
        data_filme = {}
        data_filme['nome'] = nome
        data_filme['ano'] = ano
        data_filme['dur'] = dur
        data_filme['id'] = novo_id

        nodo = {"id": novo_id, "data": data_filme}
        print(nodo)

        films_abp.Add_Node(nodo)

        film_trie.insert(nome, novo_id)

        matriz_filme_ator[novo_id] = atores_ids

        matriz_filme_diretor[novo_id] = diretores_ids

    salvaTudo()













def novoId(abp):
    maior = abp.Find_Maximum_Node()
    return maior['id'] + 1







        
eel.start('main.html', port=32514)













