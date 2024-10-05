import warnings

import pyautogui
from pywinauto.application import Application
from pywinauto_recorder.player import (
    set_combobox,
)
from rich.console import Console
from worker_automate_hub.api.client import sync_get_config_by_name

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    import_nfe,
    kill_process,
    login_emsys,
    type_text_into_field,
    incluir_registro,
    set_variable,
    get_xml,
    delete_xml,
    download_xml,
    worker_sleep,
    verify_nf_incuded,
)

pyautogui.PAUSE = 0.5
console = Console()


async def entrada_de_notas_207(task):
    """
    Processo que relazia entrada de notas no ERP EMSys(Linx).

    """
    try:
        #Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)
       
        #Seta config entrada na var nota para melhor entendimento
        nota = task['configEntrada']
        multiplicador_timeout = int(float(task["sistemas"][0]["timeout"]))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        #Abre um novo emsys
        await kill_process("EMSys")
        app = Application(backend='win32').start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings("ignore", category=UserWarning, message="32-bit application should be automated using 32-bit Python")
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config['conConfiguracao'], app, task)

        if return_login['sucesso'] == True:
            type_text_into_field('Nota Fiscal de Entrada', app['TFrmMenuPrincipal']['Edit'], True, '50')
            pyautogui.press('enter')
            await worker_sleep(2)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login["retorno"]}")
            console.print(f"\nError Message: {return_login["retorno"]}", style="bold red")
            return return_login
        
        await worker_sleep(6)
        #Procura campo documento
        console.print('Navegando pela Janela de Nota Fiscal de Entrada...\n')
        app = Application().connect(title="Nota Fiscal de Entrada")
        main_window = app["Nota Fiscal de Entrada"]

        console.print("Controles encontrados na janela 'Nota Fiscal de Entrada, navegando entre eles...\n")
        panel_TNotebook = main_window.child_window(class_name="TNotebook", found_index=0)
        panel_TPage = panel_TNotebook.child_window(class_name="TPage", found_index=0)
        panel_TPageControl = panel_TPage.child_window(class_name="TPageControl", found_index=0)
        panel_TTabSheet = panel_TPageControl.child_window(class_name="TTabSheet", found_index=0)
        combo_box_tipo_documento = panel_TTabSheet.child_window(class_name="TDBIComboBox", found_index=1)
        combo_box_tipo_documento.click()
        console.print("Clique select box, Tipo de documento realizado com sucesso, selecionando o tipo de documento...\n")

        await worker_sleep(2)

        set_combobox("||List", "NOTA FISCAL DE ENTRADA ELETRONICA - DANFE")
        console.print("Tipo de documento 'NOTA FISCAL DE ENTRADA ELETRONICA - DANFE', selecionado com sucesso...\n")

        await worker_sleep(4)

        #Clica em 'Importar-Nfe'
        imported_nfe  = import_nfe()
        if imported_nfe['sucesso'] == True:
            console.log(imported_nfe['retorno'], style='bold green')
        else:
            return {"sucesso": False, "retorno": f"{import_nfe['retorno']}"}

        await worker_sleep(10)

        # Download XML
        get_gcp_token = sync_get_config_by_name("GCP_SERVICE_ACCOUNT")
        get_gcp_credentials = sync_get_config_by_name("GCP_CREDENTIALS")
        env_config, _ = load_env_config()

        download_xml(env_config["XML_DEFAULT_FOLDER"], get_gcp_token, get_gcp_credentials, nota["nfe"])

        # Permanece 'XML'
        #Clica em  'OK' para selecionar
        pyautogui.click(970, 666)
        await worker_sleep(3)

        # Click Downloads
        get_xml(nota["nfe"])
        await worker_sleep(2)
        # Deleta o xml
        delete_xml(nota["nfe"])
        
        #VERIFICANDO A EXISTENCIA DE WARNINGS
        await worker_sleep(7)
        try:
            console.print("Verificando a existencia de warning após a importação do xml...\n")
            app = Application().connect(title="Warning")
            main_window = app["Warning"]
            
            console.print("Clicando em NO, para andamento do processo...\n")
            btn_no = main_window.child_window(title="&No")
            if btn_no.exists() and btn_no.is_enabled():
                btn_no.click()
            else:
                console.print("Warning - Erro após a importação do arquivo...\n")
                return {"sucesso": False, "retorno": 'Warning - Erro após a importação do arquivo, não foi encontrado o botão No para andamento do processo... \n'}
                
        except Exception as e:
            console.print("Não possui nenhum warning após a importação do xml...\n")


        await worker_sleep(7)
        app = Application().connect(title="Informações para importação da Nota Fiscal Eletrônica")
        main_window = app["Informações para importação da Nota Fiscal Eletrônica"]


        #INTERAGINDO COM A NATUREZA DA OPERACAO
        cfop = int(nota["cfop"])
        console.print(f"Inserindo a informação da CFOP, caso se aplique {cfop} ...\n")
        if cfop == 5655 or str(cfop).startswith("56"):
            combo_box_natureza_operacao = main_window.child_window(class_name="TDBIComboBox", found_index=0)
            combo_box_natureza_operacao.click()

            await worker_sleep(3)
            set_combobox("||List", "1652-COMPRA DE MERCADORIAS- 1.652")
            await worker_sleep(3)
        
        else:
            console.print("Erro mapeado, CFOP diferente de 5655 ou 56, necessario ação manual ou ajuste no robo...\n")
            return {"sucesso": False, "retorno": f"Erro mapeado, CFOP diferente de 5655 ou 56, necessario ação manual ou ajuste no robo"}


        #INTERAGINDO COM O CAMPO ALMOXARIFADO
        filialEmpresaOrigem = nota["filialEmpresaOrigem"]
        console.print(f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...\n")
        option_t_edit_class = main_window.children(class_name="TDBIEditCode")
        enabled_t_edit_class = [
            almoxarifado for almoxarifado in option_t_edit_class if almoxarifado.is_enabled()
        ]

        if (
            len(enabled_t_edit_class) > 1
        ):
            almoxarifado = enabled_t_edit_class[1]
            valor_almoxarifado = filialEmpresaOrigem + "50"
            console.print(f"Interagindo com o campo Almoxarifado, inserindo: {valor_almoxarifado}")
            almoxarifado.set_edit_text(valor_almoxarifado)
            await worker_sleep(1)
            almoxarifado.type_keys('{TAB}')
        else:
            console.print("Não há campos suficientes para interagir com Almoxarifado...\n")


        await worker_sleep(3)
        #INTERAGINDO COM CHECKBOX Utilizar unidade de agrupamento dos itens
        console.print("Verificando se a nota é do fornecedor SIM Lubrificantes \n")
        fornecedor = nota["nomeFornecedor"]
        console.print(f"Fornecedor: {fornecedor} ...\n")
        if "sim lubrificantes" in fornecedor.lower():
            console.print(f"Sim, nota emitida para: {fornecedor}, marcando o agrupar por unidade de medida...\n")
            checkbox = main_window.child_window(
                title="Utilizar unidade de agrupamento dos itens",
                class_name="TCheckBox",
            )
            if not checkbox.is_checked():
                checkbox.check()
                console.print("Realizado o agrupamento por unidade de medida... \n")
        else:
            console.print("Não foi necessario realizar o agrupamento por unidade de medida... \n")

        await worker_sleep(2)
        console.print("Clicando em OK... \n")
        btn_ok = main_window.child_window(title="Ok")
        btn_ok.click()
        await worker_sleep(8)

        # Inclui registro
        incluir_registro()
        #Verifica se a info 'Nota fiscal incluida' está na tela   
        retorno = verify_nf_incuded()
        if retorno:
            pyautogui.click(959, 564)
            return {"sucesso": True, "retorno": f"Nota Lançada com sucesso!"}
        else:
            return {"sucesso": False, "retorno": f"Erro ao lançar nota"}

    except Exception as ex:
        observacao = f"Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return {"sucesso": False, "retorno": observacao}
