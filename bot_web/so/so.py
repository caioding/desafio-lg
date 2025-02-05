import glob
import os
import pandas

def apagar_arquivos(cpf):
    try:
        os.remove(f"pdf\\{cpf}_titulo.pdf")
        os.remove(f"pdf\\{cpf}_eleitor.pdf")
        os.remove(f"pdf\\{cpf}.pdf")
        print("removido")
    except Exception as ex:
        print(f"Erros: {ex}")