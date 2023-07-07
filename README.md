'# MATA 59 – Redes de computadores I Prof. Gustavo B. Figueiredo

# Especificação do trabalho de MATA59

## Objetivo

Este trabalho objetiva promover um entendimento aprofundado do
funcionamento e importância das aplicações de redes. Para tal, o estudante deverá
implementar um “deposito de arquivo com replicação”. A definição dos serviços
dependerá dos requisitos da aplicação concebida e deverão ser também
especificados e codificados por cada equipe.

## A aplicação

a aplicação implementada deverá seguir o modelo cliente-servidor e
deverá funcionar em dois modos: i) modo depósito e ii) modo recuperação. No
modo depósito, o cliente informa ao servidor o arquivo a ser armazenado e o nível
de tolerância a falhas requerido, que expressa, em última instância a quantidade
de réplicas que serão armazenadas. O servidor então guarda as “N” cópias do
arquivo em locais (dispositivos) diferentes.

No modo recuperação, o cliente informa o nome do arquivo que deverá ser
recuperado. O servidor encontrará o arquivo (de alguns dos locais replicados) e
devolverá ao cliente.

A aplicação é também responsável por manter a consistência das réplicas. Ou seja,
se o cliente mudar o número de replicações para um certo arquivo, o sistema deve
aumentar ou diminuir a quantidade de réplicas conforme a última solicitação.

## Grupos

O trabalho deverá ser realizado por equipes contento não mais que 4
componentes.

## Linguagem de programação:

O trabalho poderá ser feito em qualquer linguagem de programação. É importante salientar que a escolha da linguagem será usada na avaliação caso eventuais limitações venham a impossibilitar a implementação de todas as camadas.

## Requisito:

A implementação deve ser feita obrigatoriamente usando sockets.

## Avaliação:

A avaliação do trabalho será feita com apresentação em vídeo e
através da análise do código-fonte e da sua documentação. As equipes deverão
apresentar o funcionamento da aplicação e a interação entre todas as camadas.
Serão considerados os seguintes critérios para julgamento dos trabalhos:

1. Completude (tudo o que foi solicitado foi entregue?)

2. Corretude (tudo o que foi entregue está correto e devidamente implementado?)

3. Conjunto e diversidade dos serviços (quantos serviços são oferecidos? Permite flexibilidade e modularidade?)

4. Diversidade de funcionamento da aplicação (o que faz a aplicação? Tem quantas funcionalidades? Modos de operação?)

5. Decisões de projeto e criatividade (como os problemas foram contornados?)

## Datas:

A data limite para entrega é: 06/07/2023
