from botcity.web import WebBot, By

from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

import os, shutil

def merge_pdfs(cpf):
    arq_cpf_titulo = f'pdf\\{cpf}_titulo.pdf'
    arq_cpf_eleitor = f'pdf\\{cpf}_eleitor.pdf'
    
    arq_saida = f'pdf\\{cpf}.pdf'

    merger = PdfMerger()

    with open(arq_cpf_eleitor, 'rb') as pdf_eleitor, open(arq_cpf_titulo, 'rb') as pdf_titulo:
        merger.append(pdf_eleitor)
        merger.append(pdf_titulo)

    with open(arq_saida, 'wb') as pdf_final:
        merger.write(pdf_final)

    merger.close()


def salvar_pdf_CPF_titulo(bot:WebBot, cpf):
    nome_arq = f'{cpf}_titulo.pdf'
    arq_destino = os.path.join('pdf', nome_arq)
    
    # Clica no botão de salvar pdf
    salvar_titulo = bot.find_element('//*[@id="visual-portal-wrapper"]/div[4]/div/div/ul/li/a', By.XPATH)
    salvar_titulo.click()
    
    bot.wait(3000)
    
    # Pega o arquivo mais recente na raiz do diretorio
    download_dir = os.getcwd()
    
    lista_arquivos = os.listdir(download_dir)
    caminho_completo_arquivos = [os.path.join(download_dir, f) for f in lista_arquivos]
    arquivo_mais_recente = max(caminho_completo_arquivos, key=os.path.getctime)
    
    # Renomeia e move o arquivo para a pasta pdf
    shutil.move(arquivo_mais_recente, arq_destino)
    print(f"Arquivo {cpf} movido com sucesso")
    
    
def criar_pdf_CPF_eleitor(bot, cpf, nome, endereco, eleitor):
    arq_logo = r'resources\banner.png'
    arq_destino = f'pdf\\{cpf}_eleitor.pdf'
    
    # Cria o documento PDF
    pdf = SimpleDocTemplate(arq_destino, pagesize=A4)
    
    # Estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Title']
    estilo_normal = estilos['Normal']
    estilo_centralizado = ParagraphStyle(name='Centralizado', parent=estilos['Normal'], alignment=1)  # 1 é para centralizar
    
    # Parágrafo de texto
    # paragrafo = Paragraph(texto, estilo_normal)
    
    # Cabeçalho com imagem e título
    imagem = Image(arq_logo, width=320, height=50)
    titulo = Paragraph(f"{nome}", estilo_titulo)
    
    # Data e hora atual no formato brasileiro
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    paragrafo_data_hora = Paragraph(f"Data e Hora: {data_hora_atual}", estilo_normal)

    titulo_endereco = secao_endereco = Paragraph("ENDEREÇO DO ELEITOR", estilo_centralizado)
    
    endereco_texto = f"""
    CEP: {endereco['cep']}<br/>
    Logradouro: {endereco['logradouro']}<br/>
    Bairro: {endereco['bairro']}<br/>
    Cidade: {endereco['localidade']} - {endereco['uf']}<br/>
    Estado: {endereco['estado']}<br/>
    """
    paragrafo_endereco = Paragraph(endereco_texto, estilo_normal)
        
    titulo_dados_eleitorais = Paragraph("DADOS ELEITORAIS", estilo_centralizado)
    
    dados_eleitorais_texto = f"""
    Número do título: {eleitor['nro_titulo']}<br/>
    Situação: {eleitor['situacao']}<br/>
    Seção: {eleitor['secao']}<br/>
    Zona: {eleitor['zona']}<br/>
    Local de votação: {eleitor['local_votacao']}<br/>
    Endereço de votação: {eleitor['endereco_votacao']}<br/>
    Bairro da votação: {eleitor['bairro']}<br/>
    Município/UF: {eleitor['municipio_uf']}<br/>
    País: {eleitor['pais']}
    """
    paragrafo_dados_eleitorais = Paragraph(dados_eleitorais_texto, estilo_normal)
    
    # Adiciona os elementos ao documento
    elementos = [
        imagem, Spacer(1, 12), titulo, Spacer(1, 12), paragrafo_data_hora, Spacer(1, 24),
        titulo_endereco, Spacer(1, 12), paragrafo_endereco, Spacer(1, 24),
        titulo_dados_eleitorais, Spacer(1, 12), paragrafo_dados_eleitorais
    ]
    
    # Gera o PDF com os elementos
    pdf.build(elementos)
