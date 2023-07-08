# Documentação do Software: Depósito de arquivos com replicação usando Python e Docker Containers

## Visão Geral da aplicação

O software implementado é um sistema cliente-servidor que permite o armazenamento e recuperação de arquivos. Ele segue o modelo no qual um cliente interage com um servidor para realizar as operações desejadas. O sistema opera em três modos principais:

- i) Modo Depósito: Nesse modo, o cliente informa ao servidor o arquivo a ser armazenado e o nível de replicação desejado. O nível de replicação determina a quantidade de réplicas que serão armazenadas do arquivo. O servidor é responsável por armazenar "N" cópias do arquivo em diferentes containers de armazenamento.

- ii) Modo Recuperação: Nesse modo, o cliente informa o nome do arquivo que deseja recuperar. O servidor localiza o arquivo nas réplicas disponíveis e o retorna ao cliente.

- iii) Modo de Alteração de número de réplicas: O software também é responsável por manter a consistência das réplicas. Isso significa que, se o cliente alterar o número de replicações para um determinado arquivo, o sistema irá aumentar ou diminuir a quantidade de réplicas de acordo com a solicitação.

## Tecnologias:

Foi utilizada a __linguagem de programação Python__ para o desenvolvimento dos serviços. As aplicações desenvolvidas em Python foram conteinerizadas usando o __docker__, onde a comunicação entre os containers gerados é por meio de uma rede virtual desenvolvida no processo.

## Funcionamento:

### Componentes do sistema:

O software é composto por três componentes principais:



1. O __Servidor principal (FileServer)__ representa um servidor para armazenamento e recuperação de arquivos. Ele recebe conexões de clientes e processa as solicitações enviadas pelos clientes. O servidor também se comunica com as réplicas de armazenamento para realizar as operações de armazenamento e recuperação de arquivos.  


#### Atributos:  
   - host (str): O endereço IP ou nome do host do servidor.  
   - port (int): A porta na qual o servidor está ouvir conexões.  
   - storage_replicas (list): Uma lista de réplicas de armazenamento. Cada réplica é representada por um dicionário contendo o endereço IP (ou nome do host) e a porta.


#### Métodos:
____init__(self, host: str, port: int, storage_replicas: list) -> None__  
>Este método inicializa um objeto FileServer. Ele recebe o endereço IP (ou nome do host) do servidor, a porta do servidor e uma lista de réplicas de armazenamento como argumentos. Os valores recebidos são atribuídos aos atributos correspondentes.

__start(self) -> None__  
>Este método inicia o servidor. Ele cria um socket do tipo TCP/IP, vincula o socket ao endereço IP e porta especificados e começa a ouvir por conexões. O método entra em um loop infinito onde aceita conexões de clientes e inicia uma nova thread para lidar com cada cliente.

__handle_client(self, client_socket) -> None__  
>Este método lida com um cliente conectado. Ele recebe o socket do cliente como argumento. O método recebe a solicitação do cliente, analisa o comando solicitado e chama o método apropriado para lidar com a solicitação. Em seguida, ele envia a resposta de volta ao cliente e fecha a conexão.

__deposit(self, file_name: str, replication_level: int, data: str) -> str__  
>Este método é chamado quando um cliente solicita o depósito de um arquivo. Ele recebe o nome do arquivo, o nível de replicação desejado e os dados do arquivo como argumentos. O método verifica se o número de réplicas de armazenamento é suficiente para atender ao nível de replicação desejado. Em seguida, ele envia o arquivo para as réplicas de armazenamento correspondentes, uma por uma, e aguarda a confirmação do sucesso de cada réplica. O método atualiza o mapeamento de replicação do arquivo e retorna uma mensagem de conclusão.

__retrieve(self, file_name: str) -> str__  
>Este método é chamado quando um cliente solicita a recuperação de um arquivo. Ele recebe o nome do arquivo como argumento. O método tenta recuperar o arquivo das réplicas de armazenamento, uma por uma, até encontrar uma réplica que contenha o arquivo. O conteúdo do arquivo é retornado ou, se nenhum arquivo for encontrado, uma mensagem de arquivo não encontrado é retornada.

__change_replication(self, file_name: str, new_replication_level: int) -> str__  
>Este método é chamado quando um cliente solicita a alteração do nível de replicação de um arquivo. Ele recebe o nome do arquivo e o novo nível de replicação desejado como argumentos. O método verifica o nível de replicação atual do arquivo e toma as medidas apropriadas para aumentar ou diminuir o número de réplicas para corresponder ao novo nível de replicação. Em seguida, ele retorna uma mensagem indicando o resultado da alteração.

   

2. O __cliente (FileClient)__ é onde as requisições são feitas para o servidor principal solicitando operações de armazenamento e recuperação de arquivos, além de definir o nível de replicação desejado. Representa um cliente para armazenamento e recuperação de arquivos em um servidor remoto. Ela permite que os clientes interajam com o servidor por meio de operações como depósito, recuperação e alteração de replicação de arquivos.


#### Métodos:
____init__(self, server_ip: str, server_port: int)__
>Este método inicializa um objeto FileClient. Ele recebe o endereço IP do servidor e a porta do servidor como argumentos e armazena esses valores nos atributos server_ip e server_port, respectivamente.

__get_socket(self) -> socket.socket__
>Este método cria e retorna um objeto de socket para comunicação com o servidor. Ele utiliza o endereço IP e a porta do servidor fornecidos durante a inicialização para estabelecer uma conexão com o servidor por meio do protocolo TCP/IP. O objeto de socket criado é retornado como resultado.

__deposit(self, file_name: str, replication_level: int)__
>Este método permite que o cliente deposite um arquivo no servidor. Ele recebe o nome do arquivo a ser depositado e o nível de replicação desejado como argumentos. O método abre o arquivo especificado no modo de leitura, lê seu conteúdo e cria uma mensagem de dados que inclui o nome do arquivo, o nível de replicação e os dados do arquivo. Em seguida, a mensagem é enviada para o servidor por meio do socket de comunicação. Após o envio, o método aguarda a resposta do servidor e imprime-a no console. O socket é fechado para liberar os recursos.

__retrieve(self, file_name: str)__
>Este método permite que o cliente recupere um arquivo do servidor. Ele recebe o nome do arquivo a ser recuperado como argumento. O método cria uma mensagem de solicitação de recuperação contendo o nome do arquivo e a envia para o servidor por meio do socket de comunicação. Em seguida, ele aguarda a resposta do servidor, que contém o conteúdo do arquivo recuperado. O conteúdo é gravado em um novo arquivo local com o mesmo nome do arquivo recuperado. O socket é fechado após a conclusão da operação.

__change_replication(self, file_name: str, new_replication_level: int)__
>Este método permite que o cliente altere o nível de replicação de um arquivo armazenado no servidor. Ele recebe o nome do arquivo e o novo nível de replicação desejado como argumentos. O método cria uma mensagem de solicitação de alteração de replicação contendo o nome do arquivo e o novo nível de replicação, e a envia para o servidor por meio do socket de comunicação. Após o envio, o método aguarda a resposta do servidor e imprime-a no console. O socket é fechado para liberar os recursos.



3. Os __Containers de Armazenamento (StorageReplica)__ são onde os arquivos são efetivamente armazenados. O servidor faz uso desses containers para garantir a redundância dos dados. Representa uma réplica de armazenamento que recebe solicitações de um servidor para realizar operações de depósito, recuperação e exclusão de arquivos. Cada réplica de armazenamento é responsável por manter os arquivos em uma pasta local.


#### Atributos:
- host (str): O endereço IP ou nome do host da réplica de armazenamento.
- port (int): A porta em que a réplica de armazenamento está ouvindo conexões.
- files_folder (str): O caminho para a pasta local onde os arquivos são armazenados.


#### Métodos:
____init__(self, host:str, port:int) -> None__
>Este método inicializa um objeto StorageReplica. Ele recebe o endereço IP (ou nome do host) da réplica de armazenamento e a porta da réplica de armazenamento como argumentos. Os valores recebidos são atribuídos aos atributos correspondentes. Além disso, ele cria uma pasta local para armazenar os arquivos, caso ainda não exista.

__deposit(self, file_name:str, data:str) -> bool__
>Este método é chamado quando a réplica de armazenamento recebe uma solicitação de depósito de um arquivo. Ele recebe o nome do arquivo e os dados do arquivo como argumentos. O método cria um arquivo local na pasta de arquivos e grava os dados fornecidos. Se o depósito for bem-sucedido, o método retorna "1". Caso contrário, retorna "0".

__retrieve(self, file_name:str) -> str__
>Este método é chamado quando a réplica de armazenamento recebe uma solicitação de recuperação de um arquivo. Ele recebe o nome do arquivo como argumento. O método tenta abrir o arquivo correspondente na pasta de arquivos e lê seu conteúdo. Se o arquivo for encontrado, o conteúdo é retornado como uma string. Caso contrário, retorna "-1".

__delete(self, file_name:str) -> str__
>Este método é chamado quando a réplica de armazenamento recebe uma solicitação de exclusão de um arquivo. Ele recebe o nome do arquivo como argumento. O método verifica se o arquivo existe na pasta de arquivos e o exclui. Se a exclusão for bem-sucedida, o método retorna "1". Caso contrário, retorna "0".

__start(self) -> None__
>Este método inicia a réplica de armazenamento. Ele cria um socket do tipo TCP/IP, vincula o socket ao endereço IP e à porta especificados e começa a ouvir por conexões. O método entra em um loop infinito onde aceita conexões do servidor e inicia uma nova thread para lidar com cada solicitação.

__handle_request(self, file_server_socket) -> None__
>Este método lida com uma solicitação recebida do servidor. Ele recebe o socket do servidor como argumento. O método recebe a solicitação do servidor, analisa o comando solicitado e chama o método apropriado para lidar com a solicitação. Em seguida, envia a resposta de volta ao servidor e fecha a conexão.


### Docker:
O arquivo __docker-compose.yml__ descreve a configuração de um ambiente Docker com dois serviços: __file_server__ e __storage_replica__. Esses serviços são definidos usando as imagens criadas a partir dos arquivos Dockerfile __Dockerfile.file_server__ e __Dockerfile.storage_replica__. Além disso, o arquivo __docker-compose.yml__ define uma rede chamada __file_deposit_network__ para conectar os serviços.
- Serviço __file_server__ - É responsável por executar o servidor de armazenamento e recuperação de arquivos. As configurações para esse serviço são as seguintes:  

build:
>Essa seção especifica o contexto do build e o arquivo Dockerfile a ser usado para criar a imagem do serviço file_server. O contexto é definido como o diretório atual (.) e o Dockerfile é definido como Dockerfile.file_server.  

ports:  
>Essa seção mapeia a porta 3000 do host para a porta 3000 do serviço file_server. Isso permite que o servidor seja acessado através da
porta 3000 do host.  

networks:  
>Essa seção conecta o serviço file_server à rede file_deposit_network. Essa rede permite a comunicação entre o file_server e as réplicas de armazenamento.


- serviço __storage_replica__ - Representa uma réplica de armazenamento para o servidor de armazenamento e recuperação de arquivos. As configurações para esse serviço são as seguintes:

build:
>Funciona da mesma forma que para o serviço file_server, onde o contexto é definido como o diretório atual (.) e o Dockerfile é definido como Dockerfile.storage_replica.

deploy: 
>Essa seção especifica as configurações para o modo de implantação do serviço. O modo é definido como "replicated" e o número de réplicas é definido como 5. Isso significa que serão criadas e implantadas cinco instâncias do serviço storage_replica.

networks: 
>Essa seção conecta o serviço storage_replica à rede file_deposit_network. Isso permite que as réplicas de armazenamento se comuniquem com o servidor e entre si.

- __Dockerfile.file_server__: O arquivo Dockerfile descreve a construção de uma imagem Docker que contém um servidor Python. Ele usa a imagem base oficial do Python 3.9, copia o arquivo server.py para o contêiner e define o comando padrão para iniciar o servidor Python. Com essa imagem, é possível criar um contêiner executável que inicia automaticamente o servidor quando for iniciado.
- __Dockerfile.storage_replica__: Assim como o arquivo Dockerfilme.file_server, descreve a construção de uma imagem Docker que contém uma réplica de armazenamento usando do Python 3.9, copia o arquivo storage_replica.py para o contêiner e define o comando padrão para iniciar a réplica de armazenamento. Criando um contêiner executável que inicia automaticamente a réplica de armazenamento quando for iniciado.


