# WhatsappAutomation

## Descrição
Esse projeto foi feito para automatizar uma tarefa repetitiva que tomava muito tempo em um salão de beleza.

A tarefa é mandar mensagem de confirmação para todas as clientes que possuem horário na semana. Como o sistema não possui essa ferramente nativamente então decidi cria-la.

O projeto consiste em 3 partes principais:
-  Buscar os dados no sistema.
-  Tratar esses dados.
-  Enviar as mensagens de confirmação com base nos dados.

As duas primeiras entapas são escritas em Python e a ultima utiliza JavaScript. Cada uma delas possui seu arquivo separado e são chamadas apenas para a execução no arquivo main.py.

Abaixo vou descrever detalhadamente como funciona cada um desses arquivos.

## Sumário
- [Buscar Dados](#buscar-dados)
- [Tratar Dados](#tratar-dados)
- [Enviar Mensagens](#enviar-mensagem)
- [Main](#main)

# Buscar dados:
Essa é a primeira etapa do código, consiste em usar a ferramenta *Selenium* para entrar no sistema da empresa e baixar os dados necessários para o tratamento e envio de mensagens.

O código é todo POO e sua execução se deve a instancia da classe *Automacao* dentro do arquivo main.py.

Essa parte foi dividida em 4 sub-etapas:

### -Login

        A parte de Login e Acesso aos relatorios consiste em apenas acessar uma URL e preencher dos dados selecionados,

    Login(email, senha), Relatorios(data_inical, data_final)
### - Acessar Relatórios

         A parte de Login e Acesso aos relatorios consiste em apenas acessar uma URL e preencher dos dados selecionados,


### - Excluir arquivos antigos

        Excluir arquivos antigos: Toda vez que um novo arquivo é baixado precisamos substituir o arquivo que ja estava na pasta para colocar o novo arquivo que contém o mesmo nome do antigo. Fazemos esse processo utilizando a biblioteca nativa OS do python.

### - Baixar novo Arquivo

        Baixar novo arquivo: Baixa o arquivo em uma pasta pré definida com a data especificada e no formato .xlsx.

Em suma essa parte do código pega o arquivo e coloca em uma pasta que será acessada posteriormente pelo código que trata os dados.


# Tratar Dados
Essa é a principal parte do projeto e a mais importante. 
Essa etapa garante que todos os dados etejam corretamente formatados para que possam ser enviados posteriormente.

Temos várias sub-etapas, elas são bem abstraidas em funções diferentes dentro do código para facilitar o entendimento em futuras atualizações e/ou correções.

Um coisa muito importante nesse código é a ordem que as funções são chamadas dentro dele, é muito importante seguir essa ordem.

Trabalhamos principalmente com a biblioteca Pandas para tratar o arquivo .xlsx quem é baixado do sistema 

Para esse tratamento são esperadas as seguintes colunas no DataFrame:

 - Data Cadastro Reserva 
 - Data Reserva
 - Hora
 - Cliente	
 - Celular	
 - Data Cadastro Cliente	
 - E-mail	
 - Profissional	
 - Serviço	
 - Origem	
 - Status
 - Observação	
 - Data Comanda	
 - Número	
 - Quem Cadastrou


## Todas as funções acima ficam dentro de outra funçao para ordenar a ordem de execução, a baixo está a ordem que as funções devem obedecer



- [remover_colunas(colunas_tirar)](#remover_colunas)

- [self.remover_profissionais(profissionais_remover)](#remover_profissionais)

- [remover_clientes(clientes_remover)](#remover_cliente)

- [filtrar_status(status)](#fitrar_status)

- [formatar_data()](#formtar_data)

- [tratar_numero()](#tratar_numero)

- [criar_coluna_nome()](#criar_coluna_nome)

- [criar_coluna_dia()](#criar_coluna_dia)

- [criar_coluna_data()](#criar-colunas)

- [mapear_servicos(servicos_mapear)](#mapear-serviços)

- [agrupar_df(agregacoes)](#agrupar-dataframe)

- [tratar_hora_e_servico()](#tratar-hora-e-serviço)

- [-formatar_em_string()](#tratar-dados)

### Filtra Dados
                
Como o arquivo baixado do sistema vem com muitas informações, precisamos filtrar o DataFrame para ficarmos apenas com as informações relevantes:


A tarefa de filtrar esses dados foi definida nas seguintes funções:


#### -remover_colunas()

        recebe como parametro todas as colunas que desejamos remover, esses parametros são passados ao instanciar a classe.

### -remover_profissionais() 

        essa função recebe como parametro o nome dos profissionais que desejamos remover.Esse parametro é passado ao instanciar a classe.

#### -remover_cliente() 

        essa função recebe como parametro o nome dos clientes que desejamos remover.Esse parametro é passado ao instanciar a classe.

#### -fitrar_status() 

        essa função recebe como parametro o tipo de Status desejamos manter.Esse parametro é passado ao instanciar a classe.O arquivo baixado vem com 3 possíveis tipos de Status de agendamento: Agendado, Confirmado e Cancelado.


        

## Formatar Dados:

Após ficarmos apenas com os dados relevantes no DataFrame, vamos trata-los a fim de que fiquem no padrão esperado.


#### -formtar_data() 

        Essa função garante que a coluna Data só contenha datas no formato d/m/Y

#### -tratar_numero() 
        Essa função executa uma função chamada formatar_numero() que é muito importante.

        -formatar_numero() -garante que os numeros contidos no DataFrame contanham 12 numeros e sejam no formato XX XX XXXXXXXX

#### fortmatar_em_string() 

        Essa função transforma em string as colunas HORA, PROFISSIONAL e SERVIÇO que anteriormente eram lista
                
                

                
## Criar Colunas
As funções a seguir criam colunas novas no DataFrame que contém dados importantes:
                        
#### -criar_coluna_dia() 

        Essa função cria uma nova coluna no DataFrame que contem o dia da semana em que a data selecionada se refere.

#### -criar_coluna_nome() 
        
        Essa função cria uma nova coluna no DataFrame que contém apenas o primeiro nome dos clientes.


## As próximas funções merecem uma seção específica, pois todas os tratamentos anteriores trabalham para que as funções a seguir funcionem bem



### Mapear Serviços

                Nessa Parte chamamos a função mapear(servicos) que recebe como parametro um dicionario.

                Esse dicionario contem como*chave* o valor no qual desejamos que apareçam no DataFrame e como *valor* os valores que ja vem por padrão.

                Muitas vezes os nomes padrões não estão na condição de ser enviados pela mensagem. 

                Essa função itera sobre a coluna que contem os serviços e faz a devida substuição.

### Agrupar DataFrame

                Nessa parte chamamos a função agrupar_df() essa função recebe como parametro uma serie de regras de agregação

                Essas regras garantem que as colunas HORA, PROFISSIONAL e SERVIÇO sejam uma lista de informações. Enquanto as colunas TELEFONE, DIA, NOME, STATUS, DATA contenham apenas um valor.


                Por padrão o DataFrame vem com cada linha correspondendo a um agendamento, porém pode ocorrer o caso da mesma cliente possuir mais de um agendamento.

                Essa função une o df de acordo com o cliente, fazendo com que
                todos os serviços e horarios de cada cliente fiquem em uma unica linha.

                

### Tratar Hora e Serviço

                Nessa parte chamamos a função tratar_hora_e_servico()

                Esse função garante que a horario agendado corresponda exatamente com o serviço agendado, essa função foi implementada pois ao agrupar o DataFrame estavam ocorrendo desordenamento entre os horarios e serviços nas linhas que contianham mais de um agendamento.


### Salvar DataFrame

                Nessa parte chamamos as função salvar_csv()

                Essa função exclui os arquivos da pasta e armazena um novo arquivo  que contem o mesmo nome do antigo porém agora com os dados atualizados. 

                Esse arquivo é salvo em .csv para poder ser lido pelo JavaScrip.


        

Em suma esse arquivo de código faz um tratamento minucioso nos dados e garante ao arquivo que envia as mensagens uma facilidade por não precisar se preocupar em nada do tratamento dos dados.

 
 # Enviar Mensagem 

 Esse é o arquivo mais simples. 
 

 Seu código consiste em ler o arquivo tratados utiliazando a biblioteca *csv-parser* 

 Gera um Qr Code com a biblioteca *qrcode-terminal*. Fazemos a leitura desse Qr code com o whatsapp que vai enviar as mensagens.

 Logo em seguida o código itera sobre os arquivo mandando a mensagem escolhida para cada numero de telefone.


 # Main 

 Esse arquivo é responsavel por unir os outros 3.

 Nele passamos todos os parametros exigidos para as classes

        - Automacao
        - ProcessamentoDados

Assim como utilizamos a biblioteca *subprocess* para executar o arquivo JavaScript dentro do python.







