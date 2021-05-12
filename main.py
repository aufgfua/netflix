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
        #eel.populaTabelaJs("FALSE")
        print('dados 0')
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

            diretores_filme = lista_ids_diretores


            atores_filme = []
            lista_ids_ator = matriz_filme_ator[obj['id']]
            atores_filme = lista_ids_ator

            obj['atores'] = atores_filme
            obj['diretores'] = diretores_filme

            filmes_pesquisados.append(obj)
        
        #JSON_filme = json.dumps(filmes_pesquisados)

        eel.printa('1234')

        #eel.populaTabelaJs(JSON_filme)


        
eel.start('main.html', port=32514)













