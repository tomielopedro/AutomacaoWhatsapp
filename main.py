from busca_dados import Automacao
from trata_dados import ProcessamentoDados
import subprocess

# Executar o código Python primeiro

# Variaveis de parametro ARQUIVO BUSCA_DADOS
url = ''
email_login = ''
senha_login = ''
url_relatorios = ""
acrescentar_inicial = ''
acrescentar_final = ''

# Chamando Classe
automacao = Automacao()
automacao.buscar_dados(url, email_login, senha_login, url_relatorios, acrescentar_inicial, acrescentar_final)


# Variaveis de parametros ARQUIVO TRATA_DADOS
arquivo_entrada = r"planilhas\Avec SalãoVIP - Sistema de Administração.xlsx"
caminho_saida = r"./planilha_tratada/agendamentos.csv"
colunas_para_tirar = ['Data Cadastro Reserva', 'Data Cadastro Cliente', 'E-mail', 'Origem', 'Observação',
                     'Data Comanda', 'Número', 'Quem Cadastrou']
profissionais_remover = [""]
servicos_remover = ['']
clientes_remover = [""]
status = [""]
servicos_mapeados = {
    'Manicure Diana': 'Manicure',
    'Pedicure Diana': 'Pedicure',
    'Box Braids': 'Trança',
    'Topo': 'Trança',
    'Topo detalhado': 'Trança',
    'Tiara': 'Trança',
    'Tiara Detalhada': 'Trança',
    'Lateral': 'Trança',
    'Lateral Detalhada': 'Trança',
    'Boxeadora': 'Trança',
    'Boxeadora Detalhada': 'Trança',
    'Ghana Braids': 'Trança',
    'Ghana Braids Detalhada': 'Trança',
    'Fulani': 'Trança',
    'Fulani Braids': 'Trança',
    'Gypsy Braids': 'Trança',
    'Goddes': 'Trança',
    'Faux Locs': 'Trança',
    'Dreads Locs': 'Trança',
    'Quadril': 'Trança',
    'Coxa Joelho': 'Trança',
    'Cachos Organicos': 'Trança',
    'Acessórios': 'Trança',
    'Bubbles': 'Trança',
    'Tranças 1 a 2': 'Trança',
    'Tranças 3 a 4': 'Trança',
    'Tranças 5 a 6': 'Trança',
    'Maquiagem definitiva Retoque Mês': 'Retoque Maquiagem Definitiva',
    'Maquiagem definitiva anual': 'Maquiagem Definitiva',
    'Maquiagem meio olho': 'Maquiagem Definitiva Olho',
    'Tratamento Qalisa Ultra PM': 'Tratamento Qalisa Ultra',
    'Tratamento Qalisa Ultra G': 'Tratamento Qalisa Ultra',
    'Tratamento Qalisa PM': 'Tratamento Qalisa',
    'Tratamento Qalisa G': 'Tratamento Qalisa',
    'Alisamento Masculino': 'Alisamento',
    'Alisamento Progressivo': 'Alisamento',
    'Corte Masculino Segunda a Quinta': 'Corte',
    'Corte Feminino Segunda a Quinta': 'Corte',
    'Corte feminino sem escova': 'Corte',
    'Corte Feminino Sexta e Sabado': 'Corte',
    'Corte Jessica': 'Corte',
    'Corte Masculino Sexta e Sábado': 'Corte',
    'Corte Pós Alisamento Seg à Qui': 'Corte',
    'Corte Pós Alisamento Sex e Sab': 'Corte',
    'Corte Sem Escova Virginia': 'Corte',
    'Corte virginia c escova outros profissionais': 'Corte',
    'Corte Bordado Com Escova': 'Corte com Escova',
    'Corte Com Escova': 'Corte com Escova',
    'Corte e Barba até Quinta-feira': 'Corte e Barba',
    'Corte e Barba Sexta e sábado': 'Corte e Barba',
    'Medium Blond M': 'Mechas',
    'Contorno Suave': 'Mechas',
    'Contorno Super': 'Mechas',
    'Mechas Com Virginia': 'Mechas',
    'Mechas Rui': 'Mechas',
    'Mechas com Samira': 'Mechas',
    'Medium Blond G': 'Mechas',
    'Mechas Jessica': 'Mechas',
    'Mechas rudi jessica': 'Mechas',
    'Jessica': 'Mechas',
    'Mechas Blond Rudi Curto': 'Mechas',
    'Mechas Blond Rudi Extra': 'Mechas',
    'Mechas Blond Rudi Médio': 'Mechas',
    'Mechas Blond Rudi Longo': 'Mechas',
    'Super Blond G': 'Mechas',
    'Super Blond M': 'Mechas',
    'Super Blond P': 'Mechas',
    'Medium Blond P': 'Mechas',
    'Morena Iluminada G': 'Mechas',
    'Morena Iluminada M': 'Mechas',
    'Morena Iluminada P': 'Mechas',
    'Global G': 'Mechas',
    'Global M': 'Mechas',
    'Global P': 'Mechas',
    'Cliente antiga': 'Mechas',
    'Cliente nova': 'Mechas',
    'Mechas Mega': 'Mechas',
    'Tonalizante Masculino.': 'Tonalizante',
    'Coloração Club': 'Tonalizante',
    'Tonalizante assistente': 'Tonalizante',
    'Mega Hair': 'Mega Hair',
    'Interlace a Faixa': 'Mega Hair',
    'Mega Hair Tirar': 'Mega Hair',
    'Penteado Virginia': 'Penteado',
    'Penteado Noiva e Debutante': 'Penteado',
    'Escova Lisa': 'Escova',
    'Escova Crespa': 'Escova',
    'Escova Corte Segquinta': 'Escova',
    'Escova Corte Sextasabado': 'Escova',
    'Escova mechas': 'Escova',
    'Escova Noiva e Debutante': 'Escova',
    'Finalização Jessica': 'Finalização',
    'Finalização com babyliss': 'Finalização',
    'Reconstrução Capilar Miracle': 'Reconstrução Capilar',
    'Ozônioterapia Completo': 'Ozônioterapia',
    'Ozônioterapia Serviço': 'Ozônioterapia',
    'Maquiagem Social Sex sab': 'Maquiagem',
    'Maquiagem Miri': 'Maquiagem',
    'Maquiagem Infantil': 'Maquiagem',
    'Maquiagem Noiva e Debutante Miri': 'Maquiagem',
    'Maquiagem Pós Mechas': 'Maquiagem',
    'Maquiagem Jaque': 'Maquiagem',
    'Maquiagem Social Jaque':'Maquiagem',
    'Maquiagem modelo': 'Maquiagem',
    'Maquiagem samira ter quin': 'Maquiagem',
    'Maquiagem noiva e debutante': 'Maquiagem'}
agregacoes = {
    'Hora': lambda hora: list(hora),
    'Telefone': 'first',
    'Profissional': lambda profissional: list(profissional),
    'Status': 'first',
    'Data': 'first',
    'Dia': 'first',
    'Nome': 'first',
    'Serviço': lambda servico: list(servico)
}

# Chamando Classe
processador = ProcessamentoDados(arquivo_entrada)
processador.processar_dados(colunas_para_tirar, profissionais_remover, clientes_remover, status, servicos_mapeados, agregacoes, servicos_remover)
processador.salvar_csv(caminho_saida)


# Em seguida, executar o código JavaScript
caminho_script_js = r'whatsapp-automation.js'
subprocess.run(['node', caminho_script_js])