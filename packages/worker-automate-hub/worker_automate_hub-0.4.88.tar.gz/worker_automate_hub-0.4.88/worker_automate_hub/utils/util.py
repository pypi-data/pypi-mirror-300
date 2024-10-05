import asyncio
import math
import os
import io
import re
import subprocess
import time
import warnings
import getpass
from pathlib import Path

import aiohttp
import cv2
import psutil
import pyautogui
import pyperclip
from PIL import Image 
from prompt_toolkit.shortcuts import checkboxlist_dialog
from pytesseract import pytesseract
from rich.console import Console

from worker_automate_hub.config.settings import load_worker_config
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.updater import get_installed_version

from worker_automate_hub.utils.get_creds_gworkspace import GetCredsGworkspace
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

console = Console()

ASSETS_PATH = "assets"

global_variables = {}

def set_variable(key, value):
    global_variables[key] = value

def get_variable(key):
    return global_variables.get(key, None)

async def worker_sleep(multiplier):
    # Função que espera o tempo configurado multiplicado por um fator
    timeout_multiplicador = get_variable("timeout_multiplicador")
    if timeout_multiplicador is None:
        raise ValueError("O timeout multiplicador não foi definido")
    console.log(f"Aguardando {(timeout_multiplicador * multiplier)} segundos...", style="bold yellow")
    await asyncio.sleep(timeout_multiplicador * multiplier)


async def get_system_info():
    worker_config = load_worker_config()
    max_cpu = psutil.cpu_percent(interval=10.0)
    cpu_percent = psutil.cpu_percent(interval=1.0)
    memory_info = psutil.virtual_memory()

    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "maxCpu": f"{max_cpu}",
        "maxMem": f"{memory_info.total / (1024 ** 3):.2f}",
        "usoCpu": f"{cpu_percent}",
        "usoMem": f"{memory_info.used / (1024 ** 3):.2f}",
        "situacao": "{'status': 'em desenvolvimento'}",
    }


async def get_new_task_info():
    worker_config = load_worker_config()
    atual_version = get_installed_version("worker-automate-hub")
    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "versao": atual_version,
    }


def multiselect_prompt(options, title="Select options"):
    result = checkboxlist_dialog(
        values=[(option, option) for option in options],
        title=title,
        text="Use space to select multiple options.\nPress Enter to confirm your selection.",
    ).run()

    if result is None:
        console.print("[red]No options selected.[/red]")

async def kill_process(process_name: str):
    try:
        # Obtenha o nome do usuário atual
        current_user = os.getlogin()

        # Liste todos os processos do sistema
        result = await asyncio.create_subprocess_shell(
            f'tasklist /FI "USERNAME eq {current_user}" /FO CSV /NH',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            err_msg = f"Erro ao listar processos: {stderr.decode().strip()}"
            logger.error(err_msg)
            console.print(err_msg, style="bold red")
            return

        if stdout:
            lines = stdout.decode().strip().split("\n")
            for line in lines:
                # Verifique se o processo atual corresponde ao nome do processo
                if process_name in line:
                    try:
                        # O PID(Process ID) é a segunda coluna na saída do tasklist
                        pid = int(line.split(",")[1].strip('"'))
                        await asyncio.create_subprocess_exec(
                            "taskkill", "/PID", str(pid), "/F"
                        )
                        log_msg = f"Processo {process_name} (PID {pid}) finalizado."
                        logger.info(log_msg)
                        console.print(
                            f"\n{log_msg}\n",
                            style="bold green",
                        )
                    except Exception as ex:
                        err_msg = f"Erro ao tentar finalizar o processo {process_name} (PID {pid}): {ex}"
                        logger.error(err_msg)
                        console.print(
                            err_msg,
                            style="bold red",
                        )
        else:
            log_msg = f"Nenhum processo chamado {process_name} encontrado para o usuário {current_user}."
            logger.info(
                log_msg,
                None,
            )
            console.print(
                log_msg,
                style="bold yellow",
            )

    except Exception as e:
        err_msg = f"Erro ao tentar matar o processo: {e}"
        logger.error(err_msg)
        console.print(err_msg, style="bold red")


async def find_element_center(image_path, region_to_look, timeout):
    try:
        counter = 0
        confidence_value = 1.00
        grayscale_flag = False

        while counter <= timeout:
            try:
                element_center = pyautogui.locateCenterOnScreen(
                    image_path,
                    region=region_to_look,
                    confidence=confidence_value,
                    grayscale=grayscale_flag,
                )
            except Exception as ex:
                element_center = None
                console.print(
                    f"[{counter+1}] - Elemento não encontrado na posição: {region_to_look}"
                )

            if element_center:
                console.print(
                    f"[{counter+1}] - Elemento encontrado na posição: {region_to_look}\n",
                    style="green",
                )
                return element_center
            else:
                counter += 1

                if confidence_value > 0.81:
                    confidence_value -= 0.01

                if counter >= math.ceil(timeout / 2):
                    grayscale_flag = True

                await worker_sleep(1)

        return None
    except Exception as ex:
        console.print(
            f"{counter} - Buscando elemento na tela: {region_to_look}",
            style="bold yellow",
        )
        return None


def type_text_into_field(text, field, empty_before, chars_to_empty):
    try:
        if empty_before:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)

        field.type_keys(text, with_spaces=True)

        if str(field.texts()[0]) == text:
            return
        else:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)
            field.type_keys(text, with_spaces=True)

    except Exception as ex:
        logger.error("Erro em type_text_into_field: " + str(ex), None)
        console.print(f"Erro em type_text_into_field: {str(ex)}", style="bold red")


async def wait_element_ready_win(element, trys):
    max_trys = 0

    while max_trys < trys:
        try:
            if element.wait("exists", timeout=2):
                await worker_sleep(1)
                if element.wait("exists", timeout=2):
                    await worker_sleep(1)
                    if element.wait("enabled", timeout=2):
                        element.set_focus()
                        await worker_sleep(1)
                        if element.wait("enabled", timeout=1):
                            return True

        except Exception as ex:
            logger.error("wait_element_ready_win -> " + str(ex), None)
            console.print(
                f"Erro em wait_element_ready_win: {str(ex)}", style="bold red"
            )

        max_trys = max_trys + 1

    return False


async def login_emsys(config, app, task):

    from pywinauto.application import Application

    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message="32-bit application should be automated using 32-bit Python",
    )

    await worker_sleep(10)
    # await asyncio.sleep(10)
    # Testa se existe alguma mensagem no Emsys
    console.print("Testando se existe alguma mensagem no Emsys...")
    window_message_login_emsys = await find_element_center(
        "assets/emsys/window_message_login_emsys.png", (560, 487, 1121, 746), 15
    )

    # Clica no "Não mostrar novamente" se existir
    console.print("Clicando no 'Não mostrar novamente' se existir...")
    if window_message_login_emsys:
        pyautogui.click(window_message_login_emsys.x, window_message_login_emsys.y)
        pyautogui.click(
            window_message_login_emsys.x + 383, window_message_login_emsys.y + 29
        )
        console.print("Mensagem de login encontrada e fechada.", style="bold green")

    # Ve se o Emsys esta aberto no login
    console.print("Verificando se o Emsys esta aberto no login...")
    image_emsys_login = await find_element_center(
        "assets/emsys/logo_emsys_login.png", (800, 200, 1400, 700), 60
    )

    # if image_emsys_login == None:
    #     image_emsys_login = await find_element_center(
    #     "assets/emsys/logo_emsys_linx_login.png", (800, 200, 1400, 700), 60
    # )

    if image_emsys_login:
        console.print("Aguardando a janela de login ficar pronta...")
        if await wait_element_ready_win(app["Login"]["Edit2"], 80):
            console.print("Procurando o icone disconect_database...")
            disconect_database = await find_element_center(
                "assets/emsys/disconect_database.png", (1123, 452, 1400, 578), 60
            )

            if disconect_database:
                # Realiza login no Emsys
                console.print("Realizando login no Emsys...")
                type_text_into_field(config["user"], app["Login"]["Edit2"], True, "50")
                pyautogui.press("tab")
                type_text_into_field(
                    config["pass"],
                    app["Login"]["Edit1"],
                    True,
                    "50",
                )
                pyautogui.press("enter")

                # Seleciona a filial do emsys
                console.print("Seleciona a filial do emsys...")
                selecao_filial = await find_element_center(
                    "assets/emsys/selecao_filial.png", (480, 590, 820, 740), 15
                )

                console.print(f"Selecao filial via imagem: {selecao_filial}")
                if selecao_filial == None:
                    screenshot_path = take_screenshot()
                    selecao_filial = find_target_position(
                        screenshot_path, "Grupo", 0, -50, attempts=15
                    )
                    console.print(f"Selecao filial localização de texto: {selecao_filial}")
                    if selecao_filial == None:
                        selecao_filial = (700, 639)
                        console.print(f"Selecao filial posição fixa: {selecao_filial}")

                    pyautogui.click(selecao_filial)
                    console.print(f"Escrevendo [{task["configEntrada"]["filialEmpresaOrigem"]}] no campo filial...")
                    pyautogui.write(task["configEntrada"]["filialEmpresaOrigem"])
                    

                else:                    
                    console.print(f"Escrevendo [{task["configEntrada"]["filialEmpresaOrigem"]}] no campo filial...")
                    type_text_into_field(
                        task["configEntrada"]["filialEmpresaOrigem"],
                        app["Seleção de Empresas"]["Edit"],
                        True,
                        "50",
                    )
                pyautogui.press("enter")

                button_logout = await find_element_center(
                    "assets/emsys/button_logout.png", (0, 0, 130, 150), 60
                )

                if button_logout:
                    console.print(
                        "Login realizado com sucesso.", style="bold green"
                    )
                    return {
                        "sucesso": True,
                        "retorno": "Logou com sucesso no emsys!",
                    }
        else:
            log_msg = "Elemento de login não está pronto."
            logger.info(log_msg)
            console.print(log_msg, style="bold red")
            return {"sucesso": False, "retorno": "Falha ao logar no EMSys!"}
    
    else:
        log_msg = "A tela de login nao foi encontrada."
        logger.info(log_msg)
        console.print(log_msg, style="bold red")
        return {"sucesso": False, "retorno": log_msg}


async def api_simplifica(
    urlSimplifica: str,
    status: str,
    observacao: str,
    uuidsimplifica: str,
    numero_nota,
    valor_nota,
):

    data = {
        "uuid_simplifica": uuidsimplifica,
        "status": status,
        "numero_nota": numero_nota,
        "observacao": observacao,
        "valor_nota": valor_nota,
    }

    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            async with session.post(f"{urlSimplifica}", data=data) as response:
                data = await response.text()
                log_msg = f"\nSucesso ao enviar {data}\n para o simplifica"
                console.print(
                    log_msg,
                    style="bold green",
                )
                logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao comunicar com endpoint do Simplifica: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.info(err_msg)


def add_start_on_boot_to_registry():
    import winreg as reg

    try:
        # Caminho para a chave Run
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        # Nome da chave
        key_name = "worker-startup"

        # Caminho para o executável no diretório atual
        directory_value = os.path.join(os.getcwd(), "worker-startup.bat")

        # Acessar a chave de registro
        registry_key = reg.OpenKey(
            reg.HKEY_CURRENT_USER, registry_path, 0, reg.KEY_SET_VALUE
        )

        # Adicionar ou modificar o valor
        reg.SetValueEx(registry_key, key_name, 0, reg.REG_SZ, directory_value)

        # Fechar a chave de registro
        reg.CloseKey(registry_key)

        log_msg = f"Chave {key_name} adicionada ao registro com sucesso com o valor '{directory_value}'!"
        console.print(
            f"\n{log_msg}\n",
            style="bold green",
        )
        logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao adicionar ao registro: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)


def create_worker_bat():
    try:
        # Caminho do diretório atual
        current_dir = os.getcwd()
        nome_arquivo = "worker-startup.bat"

        # Conteúdo do arquivo
        # cd %USERPROFILE%
        bat_content = f"""@echo off
cd {current_dir}   
pipx install worker-automate-hub --force     
start /min "" "worker" "run"
"""

        # Caminho completo para o arquivo
        bat_file_path = os.path.join(current_dir, nome_arquivo)

        # Escrevendo o conteúdo no arquivo
        with open(bat_file_path, "w") as file:
            file.write(bat_content.strip())

        log_msg = f"Arquivo {nome_arquivo} criado com sucesso em {bat_file_path}!"
        console.print(
            f"\n{log_msg}\n",
            style="bold green",
        )
        logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao criar o arquivo {nome_arquivo}: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)


def take_screenshot() -> Path:   
    screenshot_path = Path.cwd() / "temp" / "screenshot.png"      
    screenshot_path.parent.mkdir(parents=True, exist_ok=True)    
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    
    return screenshot_path


def preprocess_image(image_path):
    # Carregar a imagem
    image = cv2.imread(str(image_path))

    # Converter para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar threshold binário
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Remover ruído com medianBlur
    denoised_image = cv2.medianBlur(binary_image, 3)

    # Aumentar o contraste
    contrast_image = cv2.convertScaleAbs(denoised_image, alpha=1.5, beta=0)

    return contrast_image


def take_target_position(
    screenshot_path: Path, target_text: str, vertical=0, horizontal=0
) -> tuple | None:

    selected_image = Image.open(screenshot_path).convert("L")

    # Configurações do pytesseract
    # custom_config = r'--oem 3 --psm 6'

    # Extrair dados do texto usando pytesseract
    text_data = pytesseract.image_to_data(
        selected_image,
        output_type=pytesseract.Output.DICT,
        lang="por",  # , config=custom_config
    )

    # Identificar a posição do texto desejado
    field_center = None
    for i, text in enumerate(text_data["text"]):
        if len(text) > 0:
            if target_text.lower() in str(text).lower():
                x = text_data["left"][i]
                y = text_data["top"][i]
                w = text_data["width"][i]
                h = text_data["height"][i]
                # Centralizando nas coordenadas do campo
                field_center = (x + w // 2, y + h // 2)
                break

    # Aplicar as modificações de posição
    if field_center:
        field_center = (field_center[0] + horizontal, field_center[1] + vertical)

    return field_center


def find_target_position(
    screenshot_path: Path,
    target_text: str,
    vertical_pos: int = 0,
    horizontal_pos: int = 0,
    attempts: int = 5,
) -> tuple | None:
    attempt = 0
    target_pos = None

    while attempt < attempts:
        target_pos = take_target_position(
            screenshot_path,
            target_text,
            vertical=vertical_pos,
            horizontal=horizontal_pos,
        )
        console.print(f"Tentativa {attempt + 1} - Posição: {target_pos}")
        if target_pos is not None:
            log_msg = f"Posição do campo [{target_text}] encontrada na tentativa [{attempt + 1}], com valor de: {target_pos}"
            console.print(log_msg, style="green")
            logger.info(log_msg)
            return target_pos

        attempt += 1

    # Caso não tenha encontrado após todas as tentativas
    log_msg = f"Não foi possível encontrar o campo [{target_text}] em [{attempts}] tentativas!"
    console.print(log_msg, style="red")

    return None

def select_model_capa():
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "Documento", 0, 140, 5)
    if field == None:
        return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Documento'"}
    pyautogui.click(field)
    worker_sleep(1)
    pyautogui.write("Nfe")
    pyautogui.hotkey("enter")
    #Procura o tipo de documento "NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077"
    while True:
        screenshot_path = take_screenshot()
        field_doc = find_target_position(screenshot_path, "77", 0, 140, 5)
        if field_doc is not None:

            break
        else:
            pyautogui.click(field)
            pyautogui.hotkey("enter")
            pyautogui.hotkey("down")
            pyautogui.hotkey("enter")
            pyautogui.hotkey("tab")
            worker_sleep(2)

    return {"sucesso": True, "retorno": f"Modelo Selecionado"}


def download_xml(google_drive_folder_id, get_gcp_token, get_gcp_credentials, chave_nota):

    try:
        console.print("Verificando a existência do arquivo no Google Drive...\n")
        chave_nota = f"{chave_nota}.xml"
        gcp_credencial = GetCredsGworkspace(token_dict=get_gcp_token['conConfiguracao'], credentials_dict=get_gcp_credentials['conConfiguracao'])
        creds = gcp_credencial.get_creds_gworkspace()

        if not creds:
            console.print(f'Erro ao obter autenticação para o GCP...\n')
            return {"sucesso": False, "retorno": f"Erro ao obter autenticação para o GCP"}

        # Inicializando o serviço do Google Drive
        drive_service = build("drive", "v3", credentials=creds)

        # Query para procurar o arquivo com o nome da chave da nota
        query = f"'{google_drive_folder_id}' in parents and name contains '{chave_nota}'"
        results = drive_service.files().list(
            q=query,
            pageSize=10,  # Reduzindo o número de resultados
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            fields="files(id, name)"
        ).execute()

        # Verificando se o arquivo foi encontrado
        items = results.get('files', [])

        if not items:
            console.print(f'Nenhum arquivo com o nome {chave_nota} foi encontrado...\n')
            return {"sucesso": False, "retorno": f"Nenhum arquivo com o nome {chave_nota} foi encontrado no Google Drive"}

        # Pegando o primeiro arquivo encontrado
        file_id = items[0]['id']
        file_name = items[0]['name']
        console.print(f'Arquivo {file_name} encontrado. Iniciando o download...\n')

        # Definindo o caminho local para salvar o arquivo
        file_path = os.path.join(os.path.expanduser('~'), 'Downloads', file_name)

        # Iniciando o download
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            console.print(f"Download {int(status.progress() * 100)}% concluído.")

        console.print(f"Arquivo {file_name} baixado com sucesso e salvo em {file_path}.\n")
        return {"sucesso": True, "retorno": f"Arquivo {file_name} baixado com sucesso"}

    except Exception as e:
        console.print(f'Erro ao baixar o arquivo do Google Drive, erro: {e}...\n')
        return {"sucesso": False, "retorno": f"Erro ao baixar o arquivo do Google Drive, erro: {e}"}

def get_xml(xml_file):
    username = getpass.getuser()
    xml_name = f"{xml_file}.xml"
    path_to_xml = f"C:\\Users\\{username}\\Downloads\\{xml_name}"
    pyautogui.click(926, 765)
    worker_sleep(2)
    pyautogui.write(path_to_xml)
    worker_sleep(2)
    pyautogui.click(1480, 795)
    worker_sleep(2)

def delete_xml(nfe_key):
    try:
        xml_filename = f"{nfe_key}.xml"
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(download_folder, xml_filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            console.print(f"Arquivo {xml_filename} deletado com sucesso.", style="bold green")
        else:
            console.print(f"Arquivo {xml_filename} não encontrado em {download_folder}.", style="bold yellow")
    except Exception as e:
        console.print(f"Erro ao deletar o arquivo {xml_filename}: {str(e)}", style="bold red")

def config_natureza():
    pyautogui.click(869, 370)
    worker_sleep(1)
    pyautogui.write("16")
    worker_sleep(1)
    pyautogui.press("down", presses=7)
    worker_sleep(1)
    pyautogui.hotkey("enter")
    worker_sleep(1)

def config_almoxarifado(cod_almoxarifado):
    pyautogui.click(841, 390)
    worker_sleep(1)
    pyautogui.write(cod_almoxarifado)
    worker_sleep(1)
    pyautogui.press("tab")
    worker_sleep(1)
    pyautogui.click(1099, 727)

def check_itens_nota():
    pyautogui.click(631, 343)
    worker_sleep(1)
    pyautogui.click(626, 545)
    worker_sleep(1)

def check_pagamento():
    pyautogui.click(623, 374)
    worker_sleep(1)
    pyautogui.click(878, 544)
    worker_sleep(1)
    pyautogui.write("ba")
    worker_sleep(1)
    pyautogui.hotkey("enter")
    worker_sleep(1)

def check_pagamento_transferencia_cd():
    pyautogui.click(623, 374)
    worker_sleep(1)
    pyautogui.click(916, 349)
    worker_sleep(1)
    pyautogui.press("down", presses=19)
    worker_sleep(1)
    pyautogui.hotkey("enter")

def preencher_valor_restante(restante):
    pyautogui.click(1284, 351)
    worker_sleep(1)
    pyautogui.write(restante)
    worker_sleep(1)

def incluir_registro():
    pyautogui.click(594, 297)
    worker_sleep(5)
    pyautogui.click(1225, 635)
    worker_sleep(30)
    pyautogui.click(959, 564)

def finalizar_importacao():
    pyautogui.click(597, 299)
    worker_sleep(1)
    pyautogui.hotkey("enter")

async def importar_notas_outras_empresas(data_emissao, numero_nota, empresa=None):
    #Digita empresa
    data_emissao = data_emissao.replace("/", "")
    if empresa is not None:
        pyautogui.write(empresa)
    else:
        pyautogui.write("171")
    await worker_sleep(1)
    #Digita datas
    pyautogui.click(768, 428)
    await worker_sleep(1)
    pyautogui.write(data_emissao)
    await worker_sleep(1)
    pyautogui.click(859, 430)
    await worker_sleep(1)
    pyautogui.write(data_emissao)
    await worker_sleep(1)
    #Clica Campo 'Num:'"
    pyautogui.click(1014, 428)
    pyautogui.write(numero_nota)
    await worker_sleep(1)
    #Click pesquisar
    pyautogui.click(1190, 428)
    await worker_sleep(20)
    #Click em importar
    pyautogui.click(1207, 684)
    await worker_sleep(20)

# def selecionar_nota_externa(cnpj_fornecedor):
#     screenshot_path = take_screenshot()
#     field = find_target_position(screenshot_path, "de", 30, 0, 15)
#     if field == None:
#         return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Empresa'"}
#     pyautogui.click(field)
#     pyautogui.write(cnpj_fornecedor)
#     pyautogui.hotkey('tab')

def digitar_datas_emissao(data_emissao):
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "emissão", 0, 40, 15)
    if field == None:
        return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Data de emissão inicio'"}
    pyautogui.click(field)
    pyautogui.write(data_emissao)

    field = find_target_position(screenshot_path, "a", 0, 40, 15)
    if field == None:
        return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Data de emissão fim'"}
    pyautogui.click(field)
    pyautogui.write(data_emissao)

async def import_nfe():
    await worker_sleep(2)
    pyautogui.click(1138,301)
    await worker_sleep(8)
    return {"sucesso": True, "retorno": f"Clicou Importar nfe"}

def digitar_numero_nota(numero_nota):
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "Núm", 0, 60, 15)
    if field == None:
        return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Núm Nota'"}
    #pyautogui.click(field)
    pyautogui.write(numero_nota)
    console.log("Escreveu numero da nota", style="bold green")
    field = find_target_position(screenshot_path, "pesquisar", 0 ,0, 15)
    if field == None:
        return {"sucesso": False, "retorno": f"Não foi possivel encontrar o botão 'Pesquisar'"}
    console.log("Clicando em pesquisar", style="bold green")
    pyautogui.click(field)



def select_nfe(nfe_type):
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, nfe_type, 0 ,0, 15)
    if field == None:
        return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo de 'Notas de Outras Empresas'"}
    pyautogui.click(field)

    return {"sucesso": True, "retorno": f"Selecionou {nfe_type}"}

async def transmitir_nota(task, nota_fiscal, valor_nota):
    pyautogui.click(875, 596)
    logger.info("\nNota Transmitida")
    console.print("\nNota Transmitida", style="bold green")

    await worker_sleep(7)

    #Fechar transmitir nota
    console.print("Fechando a transmissão da nota...\n")

    pyautogui.click(957, 556)

    await worker_sleep(15)
    screenshot_path = take_screenshot()
    transmitir_fechar = find_target_position(screenshot_path, "fechar", attempts=15)
    if transmitir_fechar is not None:
        pyautogui.click(transmitir_fechar)
        log_msg = f'Nota Transmitida com sucesso'
        logger.info(log_msg)
        console.print(log_msg, style="bold green")
    else:
        log_msg = f'Nota não transmitida'
        logger.info(log_msg)
        console.print(log_msg, style='bold red')
        await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
        return {"sucesso": False, "retorno": log_msg}


    return{'sucesso': True, 'retorno': "Nota transmitida com sucesso"}


async def select_model_pre_venda(text_to_find : str, task):
    #Procura se o campo de select ja possui a opção que você precisa selecionada
    screenshot = take_screenshot()
    field = find_target_position(screenshot, text_to_find, 0, 0, 5)
    if field:
        return True
    else:
        retorno = await find_desired_model(text_to_find, task)
    
    if retorno:
        return retorno


async def extract_value():
    # pyautogui.click(1304, 780)
    pyautogui.doubleClick(1304, 780, interval=0.3)
    pyautogui.doubleClick(1304, 780, interval=0.3)
    pyautogui.hotkey("ctrl", "c")
    console.log(f"Valor nota copiado: {pyperclip.paste()}", style='bold green')
    valor_nota = pyperclip.paste()
    # valor_nota = re.findall(r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b', valor_nota)
    # print(valor_nota)
    return valor_nota


async def extract_nf_number():
    # screenshot_path = take_screenshot()
    # nota_fiscal_gerada = find_target_position(6395, "gerada", attempts=15)
    # pyautogui.click(nota_fiscal_gerada)
    pyautogui.click(965, 515)
    await asyncio.sleep(5)
    pyautogui.hotkey("ctrl", "c")
    nota_fiscal = pyperclip.paste()
    nota_fiscal = re.findall(r'\d+-?\d*', nota_fiscal)
    return nota_fiscal[0]

async def find_desired_model(text_to_find, task):
    #Get index do campo
    from worker_automate_hub.api.client import get_index_modelo_emsys
    index = await get_index_modelo_emsys(task['configEntrada']['filialEmpresaOrigem'], text_to_find)
    console.log(f"Indice do banco: {index['indice']}")
    # #Se não achou clica no campo modelo e sobe ate a primeira opção
    modelo_select_position = (830, 268)
    pyautogui.click(modelo_select_position)
    #Sobe para o primeiro modelo disponivel
    pyautogui.hotkey('enter')
    pyautogui.press('up', presses=15, interval=0.1)
    indice: int = int(index['indice'])
    #Seleciona o modelo com base na query "get_index_modelo_emsys"
    pyautogui.press('down', presses=indice)
    pyautogui.hotkey('tab')
    
    await worker_sleep(3)
    
    screenshot = take_screenshot()
    field = find_target_position(screenshot, text_to_find, 0, 0, 5)
    if field:
        console.log("Selecionou Modelo da nota corretamente", style='bold green')
        return True
    else:
        console.log("Modelo não selecionado corretamente", style='bold red')
        return False
    

async def faturar_pre_venda(task):
    #Clica em Faturar
        button_faturar = (1311, 396) #find_target_position(screenshot_path, "Faturar", attempts=15)
        await worker_sleep(2)
        pyautogui.click(button_faturar)
        console.print(f"Clicou em: 'Faturar'",style='bold green')

        await worker_sleep(10)

        #Aviso "Deseja faturar pré-venda?"
        button_yes = (918, 557) #find_target_position(screenshot_path, "yes", attempts=15)
        pyautogui.click(button_yes)

        await worker_sleep(10)

        #Verifica se existe a mensagem de recalcular parcelas
        screenshot_path = take_screenshot()
        message_recalcular = find_target_position(screenshot_path, "Recalcular", attempts=5)
        #Se existir clica em nao
        if message_recalcular is not None:
            button_no = (999, 560) #find_target_position(screenshot_path, "No", attempts=15)
            pyautogui.click(button_no)
            console.log("Cliclou em 'No' na mensagem de recalcular parcelas", style="bold green") 
        else:
            logger.info(f"Mensagem de para recalcular parcelas da pre-venda nao existe")
            console.print(f"Mensagem de para recalcular parcelas da pre-venda nao existe", style="bold yellow")
        
        await worker_sleep(8)

        #Seleciona Modelo
        console.log("Selecionando o modelo...\n", style='bold green')
        retorno = await select_model_pre_venda("077", task)
        if retorno == True:
            console.log('Modelo selecionado com sucesso', style='bold green')
        else:
            await api_simplifica(task['configEntrada']['urlRetorno'], "SUCESSO", retorno['retorno'], task['configEntrada']['uuidSimplifica'], None, None)
            return {"sucesso": False, "retorno": retorno['retorno']}

        #Extrai total da Nota
        console.log("Obtendo o total da Nota...\n", style='bold green')
        valor_nota = await extract_value()
        console.print(f"\nValor NF: '{valor_nota}'",style='bold green')

        #Clicar no botao "OK" com um certo verde
        button_verde = (1180, 822) #find_target_position(screenshot_path, "Ok", attempts=15)
        pyautogui.click(button_verde)
    
        await worker_sleep(5)

        #Clicar no botao "Yes" para "Deseja realmente faturar esta pre-venda?""
        button_yes = (920, 560) #find_target_position(screenshot_path, "Ok", attempts=15)
        pyautogui.click(button_yes)

        return True


async def wait_transmit():
    console.log("Esperando transmissao da nota", style='bold green')
    aguardando_nota = True
    timeout = 30
    timeout_try = 0
    while(aguardando_nota == False or timeout >= timeout_try):
        screenshot_path = take_screenshot()
        target = find_target_position(screenshot_path, "gerando", 1, 0, 1) 
        if target:
            console.print("Aguardando nota ser transmitida...", style="bold yellow")
            timeout_try += 1
            continue
        else:
            screenshot_path = take_screenshot()
            target_nota_lancada = find_target_position(screenshot_path, "autorizado", 1, 0, 1)
            if target_nota_lancada:
                #Fechar transmitir nota
                console.print("Fechando a transmissão da nota...\n", style='bold green')
                #Clica em ok "processo finalizado"
                pyautogui.click(957, 556)

                #Clica em  fechar
                pyautogui.click(1200, 667)
                        
                aguardando_nota = False
                break
            else:
                timeout_try += 1
                pass
        await worker_sleep(1)        
    return aguardando_nota


def verify_nf_incuded():
    try:
        nota_incluida = pyautogui.locateOnScreen(ASSETS_PATH + "\\entrada_notas\\nota_fiscal_incluida.png", confidence=0.9)
        if nota_incluida:
            pyautogui.click(959, 562)
            return True
    except Exception as e:
        console.print(f"Error: {e}")
        return False
    


async def rateio_window(nota):
    screenshot_path = take_screenshot()
    
    #Clica em Selecionar todos
    field = find_target_position(screenshot_path, "todos", 0, 0, 15)
    if field == None:
        return {"sucesso": False, "retorno": f"Campo 'Selecionar Todos' não encontrado"}
    pyautogui.click(field)
    await worker_sleep(2)
    
    #Digita "Centro" 1000 + filialEmpresaOrigem
    pyautogui.click(788, 514)
    filial = 1000 + int(nota['filialEmpresaOrigem'])
    pyautogui.write(str(filial))
    pyautogui.hotkey("tab")

    #Marca "Aplicar rateio aos itens selecionados"
    pyautogui.hotkey("space")
    pyautogui.hotkey("tab")

    #Digita % Rateio
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("del")
    pyautogui.write("100")

    #Clica Incluir registro
    pyautogui.click(1161, 548)
    await asyncio.sleep(20)
    
    #Clica OK
    pyautogui.click(1200, 683)
    await worker_sleep(5)
