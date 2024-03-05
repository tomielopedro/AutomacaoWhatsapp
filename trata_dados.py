import pandas as pd
import os

class ProcessamentoDados:

    def __init__(self, arquivo_excel):
        self.df = pd.read_excel(arquivo_excel)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

# FORMATAR COLUNAS
    def formatar_numero(self, numero_telefone):
        # Formata o numero para ter 10 caracteres 
        # Coloca o Código do pais na frente do numero
        codigo_pais = '55' 
        if len(numero_telefone) == 11:
            return f'{codigo_pais}{numero_telefone[0:2]}{numero_telefone[3:]}'
        elif len(numero_telefone) == 10:
            return f'{codigo_pais}{numero_telefone}'
    
    def tratar_numero(self):
        # Aplicando a função para formatar o número de telefone
        self.df['Celular'] = self.df['Celular'].apply(lambda x: '{:.0f}'.format(x))
        self.df['Celular'] = self.df['Celular'].apply(self.formatar_numero)
        self.df = self.df.dropna(subset=['Celular'])
        self.df = self.df.rename(columns={'Celular': 'Telefone'})
        
    def formatar_em_string(self):
        self.df['Hora'] = self.df['Hora'].apply(lambda x: ', '.join(x))
        self.df['Serviço'] = self.df['Serviço'].apply(lambda x: ', '.join(x))
        self.df['Profissional'] = self.df['Profissional'].apply(lambda x: ', '.join(x))
    
    def remover_colunas(self, colunas):
    # Verifica se as colunas estão presentes no DataFrame antes de tentar removê-las
        colunas_existentes = [coluna for coluna in colunas if coluna in self.df.columns]
        if colunas_existentes:
            self.df = self.df.drop(colunas_existentes, axis=1)
            print(f"Colunas removidas: {colunas_existentes}")

        else:
            print("Nenhuma das colunas especificadas está presente no DataFrame.")

# DATA
    def formatar_data(self):
        # Formata a data para o formato brasileiro e transoforma a coluna em datetime
        formato_data_hora = '%d/%m/%Y'
        
        self.df['Data Reserva'] = pd.to_datetime(self.df['Data Reserva'], format=formato_data_hora)
        
    def criar_coluna_dia(self):
        # Mapeamento dos dias da semana em português
        dias_da_semana = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    # Aplica o mapeamento na coluna 'Dia'
        self.df['Dia'] = self.df['Data Reserva'].dt.strftime('%A').map(dias_da_semana)

    def criar_coluna_data(self):
        # Cria uma coluna que tenha apenas dia e mes
        self.df['Data'] = self.df['Data Reserva'].dt.strftime('%d/%m')
        self.df = self.df.drop('Data Reserva', axis=1)

# PROFISSIONAIS
    def remover_profissionais(self, profissionais):
        # Remove Profissionais Selecionados
        profissionais_existentes = self.df['Profissional'].unique()
        profissionais_validos = [profissional for profissional in profissionais if profissional in profissionais_existentes]
        self.df = self.df[~self.df['Profissional'].isin(profissionais_validos)]
        print(f'Profissionais Removidos: {profissionais_validos}')
    
# SERVICOS    
    def ordenar_horario_servico_profissional(self, trios):
        # Ordenar os pares (horário, serviço) por horário
        trios_ordenados = sorted(trios, key=lambda x: x[0])
        # Separar os horários e serviços ordenados
        horarios_ordenados = [trio[0] for trio in trios_ordenados]
        servicos_ordenados = [trio[1] for trio in trios_ordenados]
        profissionais_ordenados = [trio[2] for trio in trios_ordenados]
        return horarios_ordenados, servicos_ordenados, profissionais_ordenados
        # essa função garante que os horarios correspondam aos seus respectivos serviços e profissionais
    
    def mapear_servicos(self, servicos_mapeados):
        # Mapeio os serviços e muda o nome original por nomes selecionados
        self.df['Serviço'] = self.df['Serviço'].apply(lambda x: servicos_mapeados.get(x, x))

    def tratar_hora_e_servico_profissional(self):
        self.df[['Hora', 'Serviço', 'Profissional']] = self.df.apply(lambda row: 
                                self.ordenar_horario_servico_profissional(zip(row['Hora'], row['Serviço'], row['Profissional'] )), axis=1, result_type='expand')

    def remover_servicos(self, servicos_para_excluir):
        servicos_existentes = self.df['Serviço'].unique()
        servicos_validos = [servico for servico in servicos_para_excluir if servico in servicos_existentes]
        self.df = self.df[~self.df['Serviço'].isin(servicos_validos)]
        print(f'Serviços Removidos: {servicos_validos} ')
    

# CLIENTES:
    def remover_clientes(self, clientes):
        # Remove clientes selecionados
        clientes_existentes = self.df['Cliente'].unique()
        clientes_validos = [cliente for cliente in clientes if cliente in clientes_existentes]
        self.df = self.df[~self.df['Cliente'].isin(clientes_validos)]
        print(f'Clientes Removidos: {clientes_validos} ')
    
    def criar_coluna_nome(self):
        # Coluna recebe apenas o primeiro nome do cliente
        self.df['Nome'] = self.df['Cliente'].apply(lambda x: x.split()[0])
        self.df['Nome'] = self.df['Nome'].apply(lambda x: x.capitalize())
    
 # STATUS
    def filtrar_status(self, status_atual):
        # Filtra o df por um status especifico
        status_existentes = self.df['Status'].unique()
        status_validos = [status for status in status_atual if status in status_existentes]
        self.df = self.df[self.df['Status'].isin(status_validos)]
        print(f'Status Filtrados:{status_validos}')

# AGRUPAMENTO
    def agrupar_df(self, agregacoes):
        # Agrupa o DataFrame pela coluna 'Cliente' e aplica as funções de agregação definidas
        self.df = self.df.groupby('Cliente').agg(agregacoes).reset_index()

# PROCESSAMENTO: 
    def processar_dados(self, colunas_tirar, profissionais_remover, clientes_remover, status, servicos_mapear, agregacoes, servicos_remover): 
    # Importante lembrar que as funções devem seguir exatamente essa ordem, a inversão pode gerar erros no código
        print(100*'=')
        print('Iniciando o tratamento de dados')
    # Definindo as colunas que deseja remover
        self.remover_colunas(colunas_tirar)
    
    # Filtrando o DataFrame para remover os profissionais selecionados
        self.remover_profissionais(profissionais_remover)

    # Filtrando o DataFrame para clientes diferentes dos selecionados
    
        self.remover_clientes(clientes_remover)

        self.remover_servicos(servicos_remover)

    # Filtrando o DataFrame para Status == ao selecionado
        self.filtrar_status(status)
    
    #Formatar
        self.formatar_data()
        self.tratar_numero()
    
        
        
    # Criar Colunas
        self.criar_coluna_nome()
        self.criar_coluna_dia()
        self.criar_coluna_data()
    
    # Mapeando nome dos serviços
        self.mapear_servicos(servicos_mapear)
        
    
    # Agrupamento
        self.agrupar_df(agregacoes)

    # Tratamento de colunas
        self.tratar_hora_e_servico_profissional() #muito importante
        self.formatar_em_string()



        
        print('Arquivo Tratado com Sucesso')
        print(100*'=')
  
# SALVAR DADOS
    def salvar_csv(self, caminho_saida):
        # Verificar se o diretório existe e, se não, criar o diretório
        diretorio = os.path.dirname(caminho_saida)
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        # Salvar o DataFrame como um arquivo CSV no diretório especificado
        self.df.to_csv(caminho_saida, index=False)
        print(self.df)
        print("Arquivo CSV salvo com sucesso.")