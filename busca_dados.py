import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep as sl
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Automacao:
    def __init__(self) -> None:
        self.service = Service(ChromeDriverManager().install())
        # Obtém o diretório de trabalho atual
        current_directory = os.getcwd()
        # Define o diretório de download como relativo ao diretório de trabalho atual
        self.prefs = {
            "download.default_directory": os.path.join(current_directory, "planilhas"),
            "download.prompt_for_download": False,  # Desativa a caixa de diálogo de download
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }

        # Configurando as opções do navegador com as preferências
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('prefs', self.prefs)
        self.options.add_argument('--verbose')  # Adiciona modo verbose para ver mensagens de depuração
        self.options.add_argument('--headless') # argumento para esconder o navegador
        self.options.add_argument('--log-level=3') # argumento para retirar os logs do navegador do console
        # Inicializando o navegador com as opções configuradas
        self.webdriver = webdriver.Chrome(service=self.service, options=self.options)
        # Configurando o serviço do ChromeDriver
        self.service = Service(ChromeDriverManager().install())

    def fazer_login(self, url, email, senha):
        self.webdriver.get(url)
        self.form_email = self.webdriver.find_element(By.XPATH, '//*[@id="formEmail"]').send_keys(email)
        sl(1)
        self.form_senha = self.webdriver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/form/div[2]/input').send_keys(senha)
        self.botao_entrar = self.webdriver.find_element(By.XPATH,' /html/body/div[6]/div[1]/div/div[2]/form/button').click()
        print('Login Realizado')
    
    def acessar_relatorios(self, url_relatorios):
        self.webdriver.get(url_relatorios)
        print('Relatorios 0051 Acessado')
    
    def preencher_data_inicial(self, data_inicial):
        data = self.webdriver.find_element(By.XPATH, '//*[@id="variaveis"]/div[1]/span[1]/div/input')
        data.click()
        data.send_keys(data_inicial)
        print(f'Data inicial: {data_inicial}')
    
    def preencher_data_final(self, data_final):
        # preenchendo data final
        data = self.webdriver.find_element(By.XPATH, '//*[@id="variaveis"]/div[1]/span[2]/div/input')
        data.click()
        data.send_keys(data_final)
        print(f'Data Final: {data_final}')

    def remover_arquivos(self):
        
        diretorio = r".\planilhas"

        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print("Diretório criado.")
        else:
            print("Diretório já existe.")

        # Listando os arquivos no diretório
        arquivos = os.listdir(diretorio)
        # Verificando se há arquivos no diretório

        if arquivos:
        # Iterando sobre cada arquivo no diretório e excluindo-o
            for arquivo in arquivos:
                caminho_arquivo = os.path.join(diretorio, arquivo)
                if os.path.isfile(caminho_arquivo):
                    os.remove(caminho_arquivo)
        
            print("Todos os arquivos antigos foram excluidos com sucesso!")
        else:
            print("Nenhum arquivo encontrado no diretório.")

    def baixar_arquivo(self):
        botao_buscar = self.webdriver.find_element(By.XPATH, '//*[@id="variaveis"]/div[1]/span[5]/a').click()
        sl(3)
        botao_baixar_arquivo = self.webdriver.find_element(By.XPATH, '//*[@id="tableFilter_wrapper"]/div[3]/a[2]').click()

    def buscar_dados(self, url_site, email, senha, url_relatorios, data_inicial, data_final):
        print(100*'=')
        print('Automação iniciada com sucesso!')
        self.fazer_login(url_site, email, senha)

        self.acessar_relatorios(url_relatorios)

        self.preencher_data_inicial(data_inicial)
        self.preencher_data_final(data_final)

        self.remover_arquivos()
        sl(3)
        self.baixar_arquivo()
        sl(3)
        print('Arquivo Baixado Com Sucesso!')



