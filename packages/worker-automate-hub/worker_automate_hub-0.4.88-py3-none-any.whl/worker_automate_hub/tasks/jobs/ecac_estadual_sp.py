import asyncio
import requests
from pathlib import Path
import io
import shutil
import uuid
import os
import time
from datetime import datetime

import zipfile
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from playwright.async_api import async_playwright

import pyautogui
from rich.console import Console

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.api.client import sync_get_config_by_name
from worker_automate_hub.utils.logger import logger

from worker_automate_hub.utils.get_creds_gworkspace import GetCredsGworkspace
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build


console = Console()


def find_and_click(image_path, description, confidence=0.8, write_text=None, wait_time=2):
    element = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    if element:
        pyautogui.click(element)
        console.print(f"[green]'{description}' encontrado e clicado.[/green]")
        if write_text:
            pyautogui.write(write_text, interval=0.05)
            console.print(f"[green]Texto '{write_text}' inserido em '{description}'.[/green]")
        time.sleep(wait_time)
    else:
        raise Exception(f"[red]Elemento '{description}' não encontrado![/red]")
    

def compactar_diretorio(diretorio, nome_arquivo_zip):
    arquivos = [os.path.join(diretorio, arquivo) for arquivo in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, arquivo))]

    with zipfile.ZipFile(nome_arquivo_zip, 'w') as zipf:
        for arquivo in arquivos:
            zipf.write(arquivo, os.path.basename(arquivo))


def send_email(smtp_server, smtp_port, smtp_user, smtp_password, message_text, subject, to, diretorio):

    nome_arquivo_zip = 'Consulta ECAC Estadual SP.zip'
    full_path = os.path.join(diretorio, nome_arquivo_zip)
    compactar_diretorio(diretorio, full_path)

    message = create_message_with_attachment(smtp_user, to, subject, message_text, full_path)
    send_message(smtp_server, smtp_port, smtp_user, smtp_password, smtp_user, to, message)


def create_message_with_attachment(sender, to, subject, message_text, file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    if file:
        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        main_type, sub_type = content_type.split('/', 1)
        with open(file, 'rb') as f:
            attachment = MIMEBase(main_type, sub_type)
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            attachment.add_header('Content-Transfer-Encoding', 'base64')
            message.attach(attachment)

    # raw_message = base64.urlsafe_b64encode(message.as_bytes())
    # raw_message = raw_message.decode()
    # return {'raw': raw_message}
    return message.as_string()


def send_message(smtp_server, smtp_port, smtp_user, smtp_password, sender, recipient, message):
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender, recipient, message)
            logger.info('Mensagem enviada com sucesso')
    except Exception as error:
        logger.error('Ocorreu um erro ao enviar a mensagem: %s' % error)


async def ecac_estadual_sp(task):
    """
    Processo que realiza a consulta de caixa postal do ECAC Estadual de São Paulo para os certificado SIM DISTRIBUIDORA e SIM LUBRIFICANTES.

    """
    try:
        # Obtém a resolução da tela
        screen_width, screen_height = pyautogui.size()
        console.print(f"Resolução da tela: Width: {screen_width} - Height{screen_height}...\n")
        console.print(f"Task:{task}")

        console.print("Realizando as validações inicias para execução do processo\n")
        console.print("Criando o diretório temporario ...\n")

        cd = Path.cwd()
        temp_dir = f"{cd}\\temp_certificates\\{str(uuid.uuid4())}"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        pdf_dir = os.path.join(temp_dir, "Arquivos_PDFs")
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        console.print("Obtendo configuração para execução do processo ...\n")
        try:
            config = await get_config_by_name("Ecac_Estadual_SP")
            emails_to = config['conConfiguracao']['emails']
            certificado_path = config['conConfiguracao']['CertificadoPath']
            certificado_files = config['conConfiguracao']['CertificadoFile']

            console.print("Obtendo configuração de email para execução do processo ...\n")
            smtp_config = await get_config_by_name("SMTP")

            smtp_server = smtp_config['conConfiguracao']['server']
            smtp_user = smtp_config['conConfiguracao']['user']
            smtp_pass = smtp_config['conConfiguracao']['password']
            smtp_port =  smtp_config['conConfiguracao']['port']

            get_gcp_token = sync_get_config_by_name("GCP_SERVICE_ACCOUNT")
            get_gcp_credentials = sync_get_config_by_name("GCP_CREDENTIALS")
        except Exception as e:
            console.print(f'Erro ao obter as configurações para execução do processo, erro: {e}...\n')
            return {"sucesso": False, "retorno": f"Erro ao obter as configurações para execução do processo, erro: {e}"}


        gcp_credencial = GetCredsGworkspace(token_dict=get_gcp_token['conConfiguracao'], credentials_dict=get_gcp_credentials['conConfiguracao'])
        creds = gcp_credencial.get_creds_gworkspace()

        if not creds:
            console.print(f'Erro ao obter autenticação para o GCP...\n')
            return {"sucesso": False, "retorno": f"Erro ao obter autenticação para o GCP"}


        console.print("Verificando a existência do diretório com locators...\n")
        if os.path.exists("assets/ecac_federal"):
            console.print('Diretório existe..\n')
        else:
            console.print('Diretório não existe..\n')
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o diretório com os locators para continuidade do processo, diretório: 'assets/ecac_federal'"}


        console.print('Verificando a existência dos arquivos de certificados no Google Drive...\n')
        drive_service = build("drive", "v3", credentials=creds)
        query = f"'{certificado_path}' in parents"
        results = drive_service.files().list(
            q=query,
            pageSize=1000,
            supportsAllDrives=True,  # Habilita suporte para Shared Drives
            includeItemsFromAllDrives=True,  # Inclui itens de todos os drives
            fields="files(id, name)"
        ).execute()

        items = results.get('files', [])

        if not items:
            console.print(f'Nenhum certificado encontrado...\n')
            return {"sucesso": False, "retorno": f"Nenhum certificado encontrado no diretório do Google Drive"}

        corpo_email = '''
        <html>
        <body>
            <p>Caros(as),</p>
            <p>Espero que este e-mail o encontre bem!</p>
            <p>Abaixo, segue um resumo baseado na consulta à caixa postal referente ao estado de SP.</p>
            <p>Resultado da consulta:</p>
        '''
        error_count = 0
        
        for row in certificado_files:
            try:
                empresa = row['Empresa']
                certificado = row['Certificado']
                #validade = row['Validade']
                senha = row['Senha']

                console.print(f'Procurando certificado: {certificado} para a empresa {empresa}...\n')
                drive_service = build("drive", "v3", credentials=creds)
                query = f"'{certificado_path}' in parents and name='{certificado}'"
                results = drive_service.files().list(
                    q=query,
                    pageSize=1000,
                    supportsAllDrives=True,  # Habilita suporte para Shared Drives
                    includeItemsFromAllDrives=True,  # Inclui itens de todos os drives
                    fields="files(id, name)"
                ).execute()

                items = results.get('files', [])

                if items:
                    console.print(f'Certificado: {certificado} para a empresa {empresa} encontrado...\n')
                    file_id = items[0]['id']
                    console.print(f'Certificado {certificado} encontrado. Iniciando download...\n')

                    file_path = os.path.join(temp_dir, certificado)

                    request = drive_service.files().get_media(fileId=file_id)

                    fh = io.FileIO(file_path, 'wb')
                    downloader = MediaIoBaseDownload(fh, request)
    
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        console.print(f"Download {int(status.progress() * 100)}%.")
                    
                    fh.close()

                    console.print(f"Certificado {certificado} baixado com sucesso.\n")

                    async with async_playwright() as p:
                        browser = await p.firefox.launch(headless=False)
                        console.print("Iniciando o browser")
                        context = await browser.new_context(accept_downloads=True) 
                        page = await context.new_page() 

                        await asyncio.sleep(3)

                        await page.goto('about:preferences#privacy')

                        locator_path = "assets/ecac_federal"

                        element_find_settings_image = f'{locator_path}/FindInSettings.PNG' 
                        element_view_certificates = f'{locator_path}/ViewCertificates.PNG'
                        element_your_certificates = f'{locator_path}/YourCertificates.PNG'
                        element_import_certificates = f'{locator_path}/ImportCertificate.PNG'
                        element_insert_path_certificates = f'{locator_path}/InsertPathCertificate.PNG'
                        element_open_certificates = f'{locator_path}/OpenCertificate.PNG'
                        element_pwd_certificates = f'{locator_path}/EnterPasswordCertificate.PNG'
                        element_sign_in_certificates = f'{locator_path}/SignCertificate.PNG'
                        element_confirm_certificates = f'{locator_path}/Confirm.PNG'
                        element_sign_in_certificates = f'{locator_path}/SignCertificate.PNG'
                        element_popup_certificate = f'{locator_path}/ImportCertificate_popup.PNG'


                        console.print("Importando o certificado no browser (playwright) ")
                        # Configurações
                        find_and_click(element_find_settings_image, "Configurações")
                        pyautogui.write('Cert', interval=0.05)
                        await asyncio.sleep(1)

                        # Certificados
                        find_and_click(element_view_certificates, "Certificados")
                        await asyncio.sleep(1)

                        # Meus Certificados
                        find_and_click(element_your_certificates, "Meus Certificados")
                        await asyncio.sleep(1)

                        # Importar Certificado
                        find_and_click(element_import_certificates, "Importar Certificado")
                        await asyncio.sleep(2)

                        # Inserir Caminho do Certificado e escrever o caminho do arquivo
                        find_and_click(element_insert_path_certificates, "Inserir Caminho do Certificado", write_text=file_path)
                        await asyncio.sleep(2)

                        # Abrir Certificado
                        find_and_click(element_open_certificates, "Abrir Certificado")
                        await asyncio.sleep(2)

                        # Inserir Senha do Certificado
                        find_and_click(element_pwd_certificates, "Inserir Senha do Certificado", write_text=senha)
                        await asyncio.sleep(2)

                        # Assinar Certificado
                        find_and_click(element_sign_in_certificates, "Assinar Certificado")
                        await asyncio.sleep(2)

                        # Confirmar Importação
                        find_and_click(element_confirm_certificates, "Confirmar Importação")
                        await asyncio.sleep(2)

                        element_popup_certificate = pyautogui.locateCenterOnScreen(element_popup_certificate, confidence=0.8)

                        if not element_popup_certificate:
                            await asyncio.sleep(3)
                            
                            try:
                                await page.goto('https://www.dec.fazenda.sp.gov.br/DEC/UCLogin/login.aspx', timeout=1000)
                                await asyncio.sleep(3)
                                await page.keyboard.press("Enter")
                            except:
                                await page.keyboard.press("Enter")
                                await page.goto('https://www.dec.fazenda.sp.gov.br/DEC/UCLogin/login.aspx', timeout=1000)
                                await asyncio.sleep(3)
                                await page.keyboard.press("Enter")
                            
                            await page.goto("https://www.dec.fazenda.sp.gov.br/DEC/UCServicosDisponiveis/ExibeServicosDisponiveis.aspx")
                            #await page.locator("#ConteudoPagina_tabContainerServicos_tabResponsavel_gvServicosSocio_cmdCPE_0").click()
                            await page.locator('//*[@id="ConteudoPagina_HyperLink5"]').click()
                            await page.get_by_role("link", name="Ativos").click()
                            await page.get_by_role("button", name="Todos").click()

                            message_table = await page.locator('//*[@id="ConteudoPagina_tabContainerCaixaPostal_tabAtivas_ucItensAtivos_tabContainerCaixaPostal_tabMensagens_gvMensagens"]')
                            rows = await message_table.locator("tbody tr")
                            row_count = await rows.count()

                            data_atual = datetime.now().strftime("%d/%m/%Y")

                            for i in range(row_count):
                                input_element = rows.nth(i).locator('td:nth-child(2) input[type="hidden"]')
                                hyperlink_value = await input_element.get_attribute("value")
                                
                                data_envio_element = rows.nth(i).locator('td:nth-child(5)')
                                data_envio_text = await data_envio_element.inner_text()

                                data_envio_formatada = data_envio_text.split(" ")[0]

                                if data_envio_formatada == data_atual:

                                    default_url = f"https://www.dec.fazenda.sp.gov.br/DEC/Comum/RelatorioMensagem.aspx?args={hyperlink_value}"

                                    response = requests.get(default_url)

                                    if response.status_code == 200:
                                        pdf_filename = os.path.join(pdf_dir, f"Arquivo_CaixaPostal_{i}.pdf")
                                        with open(pdf_filename, 'wb') as f:
                                            f.write(response.content)
                                    
                                        corpo_email += f'''
                                                <p>O arquivo foi baixado com sucesso e está salvo como {pdf_filename} para a empresa {empresa}.</p>
                                            '''
                                    else:
                                        corpo_email += f'''
                                        <p>Havia um arquivo disponível para a empresa {empresa}, mas não foi possível baixá-lo. Código de status: {response.status_code}.</p>
                                    '''
                                else:
                                    corpo_email += f'''
                                        <p>Mensagem disponivel para {empresa}, porém ja passou o limite da data para acesso.</p>
                                    '''

                            await context.close()
                            await browser.close()

                else:
                    console.print(f'Certificado não encontrado no Driver {certificado}...\n')
                    corpo_email += f"""
                        <p>Certificado para a empresa {empresa} não encontrado no Google Drive.</p>
                        """
                    error_count +=1
            except Exception as e:
                console.print(f'Erro na consulta para o certificado {certificado}, empresa {empresa}, erro{e}...\n')
                error_count +=1
        if error_count < len(certificado_files):
            try:
                corpo_email += '''
                    </body>
                    </html>
                    '''
                
                send_email(smtp_server, smtp_port, smtp_user, smtp_pass, corpo_email, "Consulta ECAC_Estadual - SP", emails_to,pdf_dir)
                log_msg = f"Processo concluído e e-mail disparado para área de negócio"
                console.print(log_msg)
                return {"sucesso": True, "retorno": log_msg}
            except Exception as e:
                log_msg = f"Processo concluído com sucesso, porém houve falha no envio do e-mail para área de negócio"
                console.print(log_msg)
                return {"sucesso": False, "retorno": log_msg}
        else:
            log_msg = f"Não foi possivel executar o processo para o Ecac Estadual SP"
            console.print(log_msg)
            return {"sucesso": False, "retorno": log_msg}

    except:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
        if not os.path.exists(pdf_dir):
            shutil.rmtree(pdf_dir)

        log_msg = f"Erro Processo do Ecac Estadual SP: {e}"
        logger.error(log_msg)
        console.print(log_msg, style="bold red")
        return {"sucesso": False, "retorno": log_msg}