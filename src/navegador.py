from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from datetime import datetime


def acessar_internet(URL='https://www.google.com', app=None):
    """
    Acessa uma URL utilizando um navegador web.

    Args:
    - URL (str): A URL para acessar. Padrão é 'https://www.google.com'.
    - app: Um objeto controlador do navegador. Padrão é None.

    Returns:
    Uma mensagem indicando que a URL está sendo acessada.
    Ou caso navegador não seja fornecido retorna um aviso
    """
    if app:
        app.get(URL)
        sleep(2)
        return f"Acessando {URL}..."
    if app == None:
        raise ValueError("Navegador não fornecido")



def fazer_login(email=None, senha=None, app=None):
    try:
        WebDriverWait(app, 15).until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys(email)
        WebDriverWait(app, 15).until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys(senha)
        sleep(0.7)
        app.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        sleep(2)
    except (NoSuchElementException, TimeoutException) as e:
        print("Login não realizado")
        raise e
    except Exception as erro:
        raise erro
    else:
        try:
            erro = app.find_element(By.XPATH, '//*[@id="NotiflixNotify-1" and contains(@mensagem-notiflix, "Usuário inexistente ou senha inválida")]')
            if erro:
                raise ValueError
        except ValueError as e:
            raise ValueError("Login ou Senha invalidos.")
        except Exception:
            pass
        return "Login Realizado."
    

def verificação_de_login(app):
    try:
        falha_no_login = WebDriverWait(app, 15).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="nx-message nx-with-icon"]')))
        if falha_no_login:
            raise ValueError(falha_no_login.text)
    except:
        pass

def selecionar_empresa(app, empresa='1'):
    try:
        select = WebDriverWait(app, 15).until(EC.element_to_be_clickable((By.ID, 'empresaSelect')))
        empresa = str(empresa)

        empresa_nome = None

        for option in select.find_elements(By.TAG_NAME, 'option'):
            if option.get_attribute('value') == empresa:
                empresa_nome = option.text
                option.click()
                break

        WebDriverWait(app, 10).until(EC.element_to_be_clickable((By.ID, 'continuarEmpresa'))).click()

        if empresa_nome:
            print("Empresa selecionada: ", empresa_nome)
            return empresa_nome
        else:
            print("Empresa não encontrada ou processo encerrado. Encerrando o processo...")
            raise NoSuchElementException

    except (NoSuchElementException, TimeoutException) as erro:
        raise NoSuchElementException
    except Exception as erro:
        print(f"ERRO ao selecionar empresa: {erro}")
        raise erro
    except NoSuchElementException:
        print("Finalizado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


def abrir_estoque(app):
    try:
        WebDriverWait(app, 10).until(EC.element_to_be_clickable((By.ID, 'estoque'))).click()
        WebDriverWait(app, 10).until(EC.element_to_be_clickable((By.ID, 'baixarXMLPage'))).click()
    except Exception as erro:
        print(f"ERRO ao abrir estoque")
        app.quit()
    else:
        sleep(1)
    

def selecionar_data(app):
    try:
        mes_atual = datetime.now().month - 1
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        mes_extenso = meses[mes_atual]

        select_mes = WebDriverWait(app, 15).until(EC.presence_of_element_located((By.XPATH, "//select[1]")))
        for option in select_mes.find_elements(By.TAG_NAME, "option"):
            if option.text == mes_extenso:
                option.click()
                break

        select_ano = WebDriverWait(app, 15).until(EC.presence_of_element_located((By.XPATH, "//select[2]")))
        ano_selecionado = str(datetime.now().year)  # Ano atual dinâmico
        for option in select_ano.find_elements(By.TAG_NAME, "option"):
            if option.text == ano_selecionado:
                option.click()
                break

        print(f"Mês selecionado: {mes_extenso}, Ano selecionado: {ano_selecionado}")
        return mes_extenso

    except Exception as erro:
        print(f"ERRO ao selecionar data: {erro}")
        app.quit()
        raise


def selecionar_data_anterior(app):
    try:
        mes_anterior = datetime.now().month - 2
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

        if mes_anterior < 0:
            mes_anterior = 11  # Dezembro do ano anterior
            ano_selecionado = str(datetime.now().year - 1) #ano anterior se for janeiro
        else:
            ano_selecionado = str(datetime.now().year) #ano atual

        mes_extenso = meses[mes_anterior]

        select_mes = WebDriverWait(app, 15).until(EC.presence_of_element_located((By.XPATH, "//select[1]")))
        select_ano = WebDriverWait(app, 15).until(EC.presence_of_element_located((By.XPATH, "//select[2]")))

        for option in select_mes.find_elements(By.TAG_NAME, "option"):
            if option.text == mes_extenso:
                option.click()
                break

        for option in select_ano.find_elements(By.TAG_NAME, "option"):
            if option.text == ano_selecionado:
                option.click()
                break

        print(f"Mês selecionado: {mes_extenso}, Ano selecionado: {ano_selecionado}")
        return mes_extenso

    except Exception as erro:
        print(f"ERRO ao selecionar data do mês anterior: {erro}")
        app.quit()
        raise


    
def iniciar_download_xml(app):
    try:
        botao_download = WebDriverWait(app, 10).until(
            EC.element_to_be_clickable((By.ID, 'baixarXML'))
        )
        botao_download.click()
        print("Download do XML iniciado")
        return True
    except Exception as e:
        print(f"ERRO ao iniciar download: {e}")
        return False


def verificação_de_erro_emissão(app):
    try:
        erro_message = WebDriverWait(app, 5).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="nx-message nx-with-icon"]')))
        if "Erro!" in erro_message.text:
            print("Mensagem: ", erro_message.text)
            app.quit()
            return True
    except TimeoutException:
        pass
    except Exception as e:
        print(f"Erro ao verificar emissão de erro")


def verificação_de_emissão(app):
    print("Gerando XML...")
    while True:
        try:
            WebDriverWait(app, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "block-ui-message") and contains(text(), "Gerando XML\'s...")]'))
                )
            sleep(3.5)
        except TimeoutException:
            break
        except Exception as e:
            print(f"Erro ao verificar emissão de XML")
            break
                

def verificação_de_erro_especifico(app):
    sleep(1)
    try:
        erro_message = app.find_element(By.XPATH, '//*[@id="NotiflixNotify-2" and contains(@mensagem-notiflix, "Ops.. Ocorreu um problema.")]')
        if erro_message:
            print("Erro encontrado: Ops... Ocorreu um problema.")
            print("Recomendado fazer verificação no sistema ou entrar em contato com a empresa.")
            return True
    except NoSuchElementException:
        return False
    except Exception as e:
        print(f"Erro na verificação de erro de sistema")
        

        