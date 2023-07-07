# Depósito de arquivos com replicação usando Python e Docker Networks

## A aplicação

a aplicação implementada segue o modelo cliente-servidor e
funciona em dois modos:

- i) modo depósito

- ii) modo recuperação.

No modo depósito, o cliente informa ao servidor o arquivo a ser armazenado e o nível
de replicação desejado, que expressa, em última instância a quantidade
de réplicas que serão armazenadas. O servidor então guarda as “N” cópias do
arquivo em containers de armazenamento diferentes.

No modo recuperação, o cliente informa o nome do arquivo que deverá ser
recuperado. O servidor encontra o arquivo nas replicas e devolve ao cliente.

A aplicação é também responsável por manter a consistência das réplicas. Ou seja,
se o cliente mudar o número de replicações para um certo arquivo, o sistema
aumenta ou diminui a quantidade de réplicas conforme for solicitado.

## Tecnologias:

Foir utilizada a linguagem de programação Python para o desenvolvimento dos seviços. 
As aplicações desenvolvidas em Python foram containerizadas usando o docker, e foi 
criada uma rede virtual para a comunicação entre os containers gerados.

## Funcionamento:

### Serviços Implementados:

- Conjunto e diversidade dos serviços (quantos serviços são oferecidos? Permite flexibilidade e modularidade?)
- Decisões de projeto e criatividade (como os problemas foram contornados?)

No projeto foram implementados 3 serviços principais:

1. O Servidor principal (FileServer)

Esse é o servidor onde o cliente vai fazer requisições de armazenamento....

...explica como funciona

2. As Réplicas de armazenamento (StorageReplicas)

Aqui é onde os arquivos são efetivamente armazenados...

... explica como funciona

3. O cliente

Aqui é onde as requisções são feitas para o servidor principal....

... epxlica como funciona

### Funcionalidades:

- Completude (tudo o que foi solicitado foi entregue?)
- Diversidade de funcionamento da aplicação (o que faz a aplicação? Tem quantas funcionalidades? Modos de operação?)

O cliente da aplicação fornece 3 comandos para o usuário:

1. DEPOSIT

    nesse comando, o cliente fornece para o servidor o arquivo e o nível de tolerância a falhas desejada,
    a partir disso o servidor armazena os arquivos nas réplicas, de acordo com o nível de replicação 
    requisitado. exemplo:

        DEPOSIT ./meuarquivo.txt 3

    onde "meuarquivo.txt" é o caminho do arquivo no qual se deseja depositar, e "3" é o nível de
    tolerância a falhas desejado.

2. RETRIEVE

3. CHANGE_REPLICATION
