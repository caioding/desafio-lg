import pandas as pd

def popular_planilha():
    dados = {
        "CPF" : ["57014540297", "93337205291"],
        "DATA_NASCIMENTO" : ["26/07/1974", "27/07/1986"],
        "NOME" : ["BENEVALDO PEREIRA GONCALVES", "BRUNO PEREIRA GONCALVES"],
        "NOME_MAE" : ["ROSA NUNES PEREIRA GONCALVES", "ROSA NUNES PEREIRA GONCALVES"],
        "CEP" : ["69086486", "69415000"],
        "NRO_ENDERECO" : ["8045", "s/n"]
    }

    df = pd.DataFrame(dados)

    df["DATA_NASCIMENTO"] = pd.to_datetime(df["DATA_NASCIMENTO"], format='%d/%m/%Y')
    df["DATA_NASCIMENTO"] = df["DATA_NASCIMENTO"].dt.strftime('%d/%m/%Y')

    # O terminal deve estar dentro de bot_eleitor, 
    # para encontrar o caminho relativo
    caminho_planilha = r'planilha/RelacaoEleitor.xlsx'

    df.to_excel(caminho_planilha, index=False)
    print("Dados dos alunos adicionados na planilha!")
    