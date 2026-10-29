import os
import re
from auto_chromedriver import make_chrome_browser
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

TIME_TO_WAIT = 10
PASTA_DOCS = os.path.join(os.path.dirname(__file__), 'anexar')

class AutoGomNet():
    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = password
        self._options = []

    def _logar_gomnet(self) -> None:
        self.browser = make_chrome_browser(*self._options)

        self.browser.get('http://gomnet-ce.enelint.global/')

        seach_input = WebDriverWait(self.browser, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, 'txtBoxLogin'))
        )

        seach_input.send_keys(self._username)

        seach_senha = WebDriverWait(self.browser, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, 'txtBoxSenha'))
        )

        seach_senha.send_keys(self._password)

        self.browser.find_element(By.ID, 'ImageButton_Login').click()

    def _anexar_arquivo(self, trab: int, sob: str, categoria: str, tipo: str, 
                    descricao: str, arquivo: str) -> None:
        self.browser.get('http://gomnet-ce.enelint.global/Upload.aspx?numtrab=' + trab + '&numsob=' + sob)
        sleep(1)
        seach_input = WebDriverWait(self.browser, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, 'drpCategoria'))
        )
        seach_input.send_keys(categoria)
        sleep(1)
        seach_input = WebDriverWait(self.browser, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, 'DropDownList1'))
        )
        seach_input.send_keys(tipo)
        sleep(1)
        seach_input = WebDriverWait(self.browser, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, 'fileUPArquivo'))
        )
        seach_input.send_keys(arquivo)
        sleep(1)
        seach_input = WebDriverWait(self.browser, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, 'txtBoxDescricao'))
        )
        seach_input.send_keys(descricao)
        sleep(1)
        seach_input = WebDriverWait(self.browser, TIME_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, 'Button_Anexar'))
        )
        seach_input.click()
        sleep(1)
        WebDriverWait(self.browser, TIME_TO_WAIT).until(
            EC.element_to_be_clickable((By.ID, 'Button_Anexar'))
        )

        sleep(1)

    def anexar_entregas(self) -> int:
        docs = os.listdir(PASTA_DOCS)

        self._logar_gomnet()

        print()
        print('INICIANDO LOOP DE ANEXOS!')
        print('--------------------')

        cont = 0

        for doc in docs:

            trab, sob_orig, *_ = doc.split('_')
            sob = sob_orig.zfill(10)

            categoria = 'EXECUCAO'
            tipo = 'OUTROS'
            descricao = 'ENTREGA DO TRABALHO'
            arquivo = os.path.join(PASTA_DOCS, doc)

            try:

                self._anexar_arquivo(trab, sob, categoria, tipo, descricao, arquivo)
                
            except Exception as e:

                print('Ocorreu um erro no documento: ' + doc)
                print(e)
                continue

            os.remove(arquivo)

            print(doc, 'anexada com sucesso!')

            cont += 1
        
        print('--------------------')
        print()

        return cont

    def anexar_atorizacoes_cavas(self) -> int:
        with open('obras.txt') as texto:
            registros = texto.readlines()

        obras = [re.split(r'\s+', registro) for registro in registros]

        self._logar_gomnet()

        cont = 0

        for obra in obras:
            
            trab, sob_orig, *_ = obra
            sob = sob_orig.zfill(10)

            categoria = 'EXECUCAO'
            tipo = 'Autorização de Alteração'
            descricao = 'AUTORIZAÇÃO PARA CAVAS ESPECIAIS'

            anexo = os.listdir(PASTA_DOCS)[0]
            arquivo = os.path.join(PASTA_DOCS, anexo)

            try:

                self._anexar_arquivo(trab, sob, categoria, tipo, descricao, arquivo)

            except Exception as e:

                print('Ocorreu um erro na obra: ' + trab)
                print(e)
                continue
            
            print(trab, 'anexada com sucesso!')

            cont += 1

        return cont