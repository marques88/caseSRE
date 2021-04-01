# caseSRE

aplicação para coletar as últimas postagens do Twitter

# API

A aplicação foi desenvolvida em python que possibilita a utilização da biblioteca tweepy, para apresentação dos tweets foi utilizado o angular

## Arquitetura

O case conta com as maquinas da api , angular , mongodb , graylog , zabbix e elasticsearch

Está em anexo a arquitetura do case

## Execução

É necessario realizar o download do arquivo case-sre.zip no github, após descompactar deve acessar a pasta e executar o arquivo docker-compose.

Quando as maquinas subirem no docker pasta acessar o endereço do angular (http://localhost:4201/) para pesquisar os tweets.
