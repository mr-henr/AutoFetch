import os
from time import sleep
from selenium.common.exceptions import TimeoutException
import zipfile
from pathlib import Path

def listar_arquivos(pasta):
    return set(os.listdir(pasta))


def aguardar_inicio_download(pasta, lista_de_arquivos, timeout=90):
    try:
        tempo = 0
        while tempo<timeout:
            arquivos_atualizados = listar_arquivos(pasta)
            novos_arquivos = arquivos_atualizados - lista_de_arquivos
            if novos_arquivos:
                return True
            sleep(1)
            tempo += 1
    except TimeoutException:
        print("O download do arquivo XML não foi iniciado. Verifique o sistema.")
    except Exception as e:
        print(f"Erro {e} na função aguardar_inicio_download")


def aguardar_conclusão_do_download(pasta, lista_de_arquivos, timeout=90):
    try:
        tempo = 0
        while tempo<timeout:
            arquivos_atualizados = listar_arquivos(pasta)
            novos_arquivos = arquivos_atualizados - lista_de_arquivos
            if not any(arquivo.endswith('.crdownload') for arquivo in novos_arquivos):
                print("Download concluído.")
                sleep(4)
                break
            sleep(1)
            tempo += 1
        sleep(4)
        arquivo_final = next(iter(novos_arquivos))
        return arquivo_final
    except TimeoutException:
        print("O download do arquivo XML não foi finalizado. Verifique o sistema.")
    except Exception as e:
        print(f"Erro {e} na função aguardar_conclusão_do_download")


def criar_pasta_empresa(pasta, mes, empresa):
    """
    Cria a pasta do mês dentro da pasta da empresa se ela não existir.

    :param pasta: Caminho principal onde as pastas de empresas estão localizadas.
    :param mes: Nome do mês para criar a pasta.
    :param empresa: Nome da empresa para criar a pasta.
    """
    pasta_empresa = Path(pasta, empresa)
    pasta_mes = Path(pasta_empresa, mes)
    if not pasta_mes.exists():
        os.makedirs(pasta_mes)
    sleep(5)
    return pasta_mes


def extrair_e_mover_arquivos(pasta_inicial, pasta_destino, arquivo):
    # Convertendo os caminhos para objetos Path
    pasta_inicial = Path(pasta_inicial)
    pasta_destino = Path(pasta_destino)

    # Verificando se as pastas foram corretamente criadas
    if not pasta_inicial.is_dir():
        raise ValueError(f"O diretorio {pasta_inicial} não existe.")
    if not pasta_destino.is_dir():
        raise ValueError(f"O diretorio {pasta_destino} não existe.")
    
    # Verificando caminho do arquivo xml.zip
    xml_zip = pasta_inicial / arquivo
    if not xml_zip.is_file():
        raise FileNotFoundError(f"O arquivo {arquivo} não foi encontrado.")

    # Movendo o arquivo xml.zip para pasta de destino
    xml_zip_final = pasta_destino / arquivo
    xml_zip.rename(xml_zip_final)

    # Extraindo xml.zip
    with zipfile.ZipFile(xml_zip_final, 'r') as zip_ref:
        zip_ref.extractall(pasta_destino)

    # Excluindo arquivo zip
    xml_zip_final.unlink()
    sleep(3)