import requests
import json

from botcity.web import WebBot, Browser, By
from botcity.maestro import *
BotMaestroSDK.RAISE_NOT_CONNECTED = False
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from botcity.plugins.http import BotHttpPlugin

import planilha.planilha as planilha
from planilha.popular_planilha import popular_planilha
import e_mail.e_mail as e_mail
from pdf.pdf import salvar_pdf_CPF_titulo, criar_pdf_CPF_eleitor, merge_pdfs
import so.so as so
from so.so import apagar_arquivos


def navegar_tse(bot:WebBot, caminho:str, pagina:str):
    df = planilha.ler_excel(caminho, pagina)
    dados_eleitores = []
    
    for index, linha in df.iterrows():
        cpf = linha["CPF"]
        nasc = linha["DATA_NASCIMENTO"]
        nome = linha["NOME"]
        mae = linha["NOME_MAE"]
        cep = linha["CEP"]
        nro = linha["NRO_ENDERECO"]
        dados = {
            "cpf" : cpf,
            "nome" : nome,
            "data_nascimento" : nasc,
            "nome_mae" : mae,
            "cep" : cep,
            "nro_endereco" : nro
        }

        bot.browse('https://www.tse.jus.br/servicos-eleitorais/titulo-eleitoral')
        print("Navegando pelo site do TSE...")
        bot.maximize_window()
        bot.wait(3000)

        # No primeiro acesso, é preciso aceitar os cookies 
        # pra evitar que o popup bloqueie elementos do site
        if index == 0:
            aceitar_cookies = bot.find_element('//*[@id="modal-lgpd"]/div/div/div[2]/button', By.XPATH)
            aceitar_cookies.click()
        
        # Função "Título de Eleitor"
        # //*[@id="menu-lateral-res"]/ul/li[8]/a
        # acessar_titulo = bot.find_element('//*[@id="menu-lateral-res"]/ul/li[8]/a', By.XPATH)
        # acessar_titulo.click()
        # bot.wait(10000)

        # Função nº 10 no site
        # //*[@id="content"]/app-root/div/app-atendimento-eleitor/div[1]/app-menu-option[10]/button/div/span[1]
        consultar_numero = bot.find_element('//*[@id="content"]/app-root/div/app-atendimento-eleitor/div[1]/app-menu-option[10]/button/div/span[1]', By.XPATH)
        consultar_numero.click()
        bot.wait(1000)
        
        # Input CPF
        # //*[@id="modal"]/div/div/div[2]/div[2]/form/div[1]/div[1]/input
        # Input Data de Nascimento
        # //*[@id="modal"]/div/div/div[2]/div[2]/form/div[1]/div[2]/input
        # Input Nome da Mãe
        # //*[@id="modal"]/div/div/div[2]/div[2]/form/div[1]/div[3]/div/input
        input_cpf = bot.find_element('//*[@id="modal"]/div/div/div[2]/div[2]/form/div[1]/div[1]/input', By.XPATH)
        input_nasc = bot.find_element('//*[@id="modal"]/div/div/div[2]/div[2]/form/div[1]/div[2]/input', By.XPATH)
        input_mae = bot.find_element('//*[@id="modal"]/div/div/div[2]/div[2]/form/div[1]/div[3]/div/input', By.XPATH)
        
        input_cpf.send_keys(cpf)
        bot.wait(1000)
        input_nasc.send_keys(nasc)
        bot.wait(1000)
        input_mae.send_keys(mae)
        bot.wait(1000)
        
        # Botão Entrar
        # //*[@id="modal"]/div/div/div[2]/div[2]/form/div[2]/button[2]
        acessar = bot.find_element('//*[@id="modal"]/div/div/div[2]/div[2]/form/div[2]/button[2]', By.XPATH)
        acessar.click()
        
        # Tempo de espera para acessar os dados da página do eleitor
        bot.wait(10000)
        eleitor = recuperar_dados_eleitorais(bot, dados)
        
        # Criar pdf da pagina do eleitor
        endereco = verificar_cep(bot,cep)
        
        salvar_pdf_CPF_titulo(bot, cpf)
        criar_pdf_CPF_eleitor(bot, cpf, nome, endereco, eleitor)
        
        bot.wait(3000)
        merge_pdfs(cpf)
        
        e_mail.enviar_email_anexo('caio.faneco@ifam.edu.br', f'Eleitor - {nome}', f'Segue em anexo o PDF com os dados de {nome}:', f'pdf/{cpf}.pdf')

        
        dados_eleitores.append(eleitor)
        
        
        apagar_arquivos(cpf)

    print("Navegação concluída!\n")
    bot.wait(3000)
    bot.stop_browser()
    return dados_eleitores


def recuperar_dados_eleitorais(bot:WebBot, dados:dict):
    # Título Eleitoral
    Xtitulo = '//*[@id="content"]/app-root/div/app-consultar-numero-titulo-eleitor/div[1]/div[1]/p[1]/b'
    # Situação
    Xsituacao = '//*[@id="content"]/app-root/div/app-consultar-numero-titulo-eleitor/div[1]/div[1]/p[2]/span'
    # Seção
    Xsecao = '//*[@id="content"]/app-root/div/app-consultar-numero-titulo-eleitor/div[1]/app-box-local-votacao/div/div/div[2]/div[1]/span[2]'
    # Zona
    Xzona = '//*[@id="content"]/app-root/div/app-consultar-numero-titulo-eleitor/div[1]/app-box-local-votacao/div/div/div[2]/div[3]/span[2]'
    # Local
    Xlocal = '//*[@id="content"]/app-root/div/app-consultar-numero-titulo-eleitor/div[1]/app-box-local-votacao/div/div/div[1]/div[1]/span[2]'
    # Endereço
    Xendereco = '//*[@id="content"]/app-root/div/app-consultar-numero-titulo-eleitor/div[1]/app-box-local-votacao/div/div/div[1]/div[2]/span[2]'
    # Bairro
    Xbairro = '//*[@id="content"]/app-root/div/app-consultar-numero-titulo-eleitor/div[1]/app-box-local-votacao/div/div/div[1]/div[4]/span[2]'
    # Município
    Xmunicipio = '//*[@id="content"]/app-root/div/app-consultar-numero-titulo-eleitor/div[1]/app-box-local-votacao/div/div/div[1]/div[3]/span[2]'
    # País
    Xpais = '//*[@id="content"]/app-root/div/app-consultar-numero-titulo-eleitor/div[1]/app-box-local-votacao/div/div/div[2]/div[2]/span[2]'

    titulo = bot.find_element(Xtitulo, By.XPATH).text
    bot.wait(500)
    situacao = bot.find_element(Xsituacao, By.XPATH).text
    bot.wait(500)
    secao = bot.find_element(Xsecao, By.XPATH).text
    bot.wait(500)
    zona = bot.find_element(Xzona, By.XPATH).text
    bot.wait(500)
    local = bot.find_element(Xlocal, By.XPATH).text
    bot.wait(500)
    endereco = bot.find_element(Xendereco, By.XPATH).text
    bot.wait(500)
    bairro = bot.find_element(Xbairro, By.XPATH).text
    bot.wait(500)
    municipio = bot.find_element(Xmunicipio, By.XPATH).text
    bot.wait(500)
    pais = bot.find_element(Xpais, By.XPATH).text
    bot.wait(500)

    dados_eleitorais = {
        "nro_titulo" : titulo,
        "situacao" : situacao,
        "secao" : secao,
        "zona" : zona,
        "local_votacao" : local,
        "endereco_votacao" : endereco,
        "bairro" : bairro,
        "municipio_uf" : municipio,
        "pais" : pais
    }
    
    # O dicionário dados já deve ter os dados extraídos da planilha para 
    # que esta operação gere um dicionário que possa virar um JSON depois
    dados.update(dados_eleitorais)
    print(f'Dados de {dados["nome"]}:',dados)

    return dados


def navegar_dados(dados_eleitores:list):
    print("Iniciando operações no banco de dados...")
    for eleitor in dados_eleitores:
        atualizar_banco(eleitor)
    
    print("Todas as operações com o banco foram finalidas!")


def atualizar_banco(eleitor:dict):
    url = 'http://127.0.0.1:5000/eleitor'
    
    body = {
        "cpf": eleitor["cpf"],
        "nome": eleitor["nome"],
        "data_nascimento": eleitor["data_nascimento"],
        "nome_mae": eleitor["nome_mae"],
        "cep": eleitor["cep"],
        "nro_endereco": eleitor["nro_endereco"],
        "nro_titulo": eleitor["nro_titulo"],
        "situacao": eleitor["situacao"],
        "secao": eleitor["secao"],
        "zona": eleitor["zona"],
        "local_votacao": eleitor["local_votacao"],
        "endereco_votacao":eleitor["endereco_votacao"],
        "bairro": eleitor["bairro"],
        "municipio_uf": eleitor["municipio_uf"],
        "pais": eleitor["pais"]
    }
    
    try:
        resposta = requests.post(url, json=body)
        
        if resposta.status_code == 200:
            print(f'Dados de {eleitor["nome"]} inseridos no banco com sucesso!')
        else:
            print(f'Erro ao inserir o eleitor no banco. Status code: {resposta.status_code}')
            
    except Exception as ex:
        print(f'Erro ao atualizar o banco com os dados de {eleitor["nome"]}: {ex}')
    
    
def verificar_cep(bot:WebBot,cep):
    http = BotHttpPlugin(f' https://viacep.com.br/ws/{cep}/json/?')
    retorno_json = http.get_as_json()
    return retorno_json

    
def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    bot.headless = False

    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()

    try:
        popular_planilha()
        dados_eleitores = navegar_tse(bot, r'planilha\RelacaoEleitor.xlsx', "Sheet1")
        navegar_dados(dados_eleitores)
        
    except Exception as ex:
        print(ex)



def not_found(label):
    print(f"Element not found: {label}")

if __name__ == '__main__':
    main()
