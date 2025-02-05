import pandas as pd

def ler_excel(caminho:str, pagina:str):
    # É necessário especificar o dtype de CPF, para que ele não interprete
    #  essa coluna como numérica e ignore o 0 na frente dos CPFs
    df = pd.read_excel(caminho,sheet_name=pagina, dtype={"CPF" : str, "CEP" : str, "NRO_ENDERECO" : str})
    return df