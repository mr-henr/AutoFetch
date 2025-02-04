from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from processo import navegador, armazenamento
from time import sleep

def main(login, senha, pasta_final, mes_anterior=False):

    # Instalação e configuração do Chrome Driver
    servico = Service(ChromeDriverManager().install())
    prefs = {'download.default_directory': pasta_final}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', prefs)

    Conta_ID = login  # Recebe o ID
    Conta_senha = senha  # Recebe a Senha
    
    empresa = 0
    while True:
        print(" ")
        # Fazendo Login
        try:
            navegador_chrome = webdriver.Chrome(service=servico, options=options)
            URL_access = navegador.acessar_internet('https://simulador-autofetch.netlify.app', navegador_chrome)
            login = navegador.fazer_login(Conta_ID, Conta_senha, navegador_chrome)
        except ValueError as e:
            print(e)
            navegador_chrome.quit()
            break
        except Exception:
            print(f"ERRO durante tentativa de Login")
            break
        else:
            if empresa == 0:
                print(URL_access)
                print(login)
                print(' ')

        # Selecionando empresa no site
        try:
            empresa += 1
            Empresa_nome = navegador.selecionar_empresa(navegador_chrome, empresa)
        except NoSuchElementException:
            break
        except Exception as e:
            print(f"ERRO: {e}")

        # Processo para captar a XML
        try:
            navegador.abrir_estoque(navegador_chrome)
            if mes_anterior:
                Mês = navegador.selecionar_data_anterior(navegador_chrome)
            else:
                Mês = navegador.selecionar_data(navegador_chrome)
            Arquivos = armazenamento.listar_arquivos(pasta_final)
            navegador.iniciar_download_xml(navegador_chrome)
            sleep(1.5)
        except Exception:
            print("Erro no processo de captação da XML")
            break

        # Verificando situação das XML's
        if navegador.verificação_de_erro_emissão(navegador_chrome):
            print('_' * 89)
            continue

        try:
            navegador.verificação_de_emissão(navegador_chrome)
        except Exception:
            print("ERRO EXCEPTION 1")
        else:
            try:
                verificar_erro = navegador.verificação_de_erro_especifico(navegador_chrome)
                if verificar_erro:
                    navegador_chrome.quit()
                    print('_' * 89)
                    continue
            except Exception:
                print("ERRO EXCEPTION 2")
            else:
                print("Download Iniciado...")

        armazenamento.aguardar_inicio_download(pasta_final, Arquivos)
        sleep(1.5)
        arquivo_final = armazenamento.aguardar_conclusão_do_download(pasta_final, Arquivos)
        navegador_chrome.quit()
        pasta_mes = armazenamento.criar_pasta_empresa(pasta_final, Mês, Empresa_nome)
        armazenamento.extrair_e_mover_arquivos(pasta_final, pasta_mes, arquivo_final)
        print('_' * 89)
    navegador_chrome.quit()

