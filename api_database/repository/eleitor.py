from repository import database


# Inserir eleitor
def criar_eleitor(eleitor):
    try:
        # Manipular o banco de dados
        conect = database.criar_db()
        cursor = conect.cursor()
        
        sql = (
            "INSERT INTO eleitor (cpf, nome, data_nascimento, nome_mae, cep, nro_endereco, nro_titulo, situacao, secao, zona, local_votacao, endereco_votacao, bairro, municipio_uf, pais) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        
        dados = (
            eleitor['cpf'],
            eleitor['nome'],
            eleitor['data_nascimento'],
            eleitor['nome_mae'],
            eleitor['cep'],
            eleitor['nro_endereco'],
            eleitor['nro_titulo'],
            eleitor['situacao'],
            eleitor['secao'],
            eleitor['zona'],
            eleitor['local_votacao'],
            eleitor['endereco_votacao'],
            eleitor['bairro'],
            eleitor['municipio_uf'],
            eleitor['pais']
        )
        
        cursor.execute(sql, dados)
        conect.commit()
        
        print("Eleitor inserido com sucesso.")
        
    except Exception as ex:
        print(f'Erro: Falha na inclusão: {ex}')
    finally:
        if cursor:
            cursor.close()
        if conect:
            conect.close()

# fim: criar_eleitor(eleitor)


def existe_eleitor(cpf):
    existe = False
    try:
        conect = database.criar_db()
        cursor = conect.cursor()
        sql = "SELECT cpf FROM eleitor WHERE cpf = %s"
        cursor.execute(sql, (cpf,))
        eleitor = cursor.fetchone()
        
        # Verifica se o resultado não é None
        if eleitor is not None:
            existe = True 
        
    except Exception as ex:
        print(f'Erro na verificacao da existencia do eleitor: {ex}')
    finally:
    
        if cursor:
            cursor.close()
        if conect:
            conect.close()
    
    return existe
# fim: existe_eleitor(cpf)


def obter_eleitor_cpf(cpf):
    # criar uma tupla vazia
    eleitor = ()
    try:
        conect = database.criar_db()
        cursor = conect.cursor()
        sql = f"SELECT * FROM eleitor WHERE cpf = '{cpf}'"
        cursor.execute(sql)
        eleitor = cursor.fetchone()
    except Exception as ex:
        print(f'Erro na verificacao da existencia do eleitor: {ex}')
    finally:
        cursor.close()
        conect.close()
    return eleitor

# fim: obter_eleitor_cpf(cpf)


def listar_eleitor():
    eleitores = list()
    try:
        conect = database.criar_db()
        cursor = conect.cursor()
        sql = 'SELECT * FROM eleitor ORDER BY nome'
        cursor.execute(sql)
        listar_eleitores = cursor.fetchall()
        # Tratar dados para uma estrutura JSON
        for eleitor in listar_eleitores:
            eleitores.append(
                {
                  'cpf': eleitor[0],
                  'nome': eleitor[1],
                  'data_nascimento': eleitor[2],
                  'nome_mae': eleitor[3],
                  'cep': eleitor[4],
                  'nro_endereco': eleitor[5],
                  'nro_titulo': eleitor[6],
                  'situacao': eleitor[7],
                  'secao': eleitor[8],
                  'zona': eleitor[9],
                  'local_votacao': eleitor[10],
                  'endereco_votacao': eleitor[11],
                  'bairro': eleitor[12],
                  'municipio_uf': eleitor[13],
                  'pais': eleitor[14]
                }
            )
    except Exception as ex:
        print(f'Erro: Listar usuario: {ex}')
    finally:
        cursor.close()
        conect.close()
    
    return eleitores

# Fim: lista_eleitor()


def atualizar_eleitor(eleitor):
    try:
        # Manipular o banco de dados
        conect = database.criar_db()
        cursor = conect.cursor()
        sql = f"""
                UPDATE eleitor
                SET
                    nome = '{eleitor['nome']}', 
                    data_nascimento = '{eleitor['data_nascimento']}',
                    nome_mae = '{eleitor['nome_mae']}', 
                    cep = '{eleitor['cep']}', 
                    nro_endereco = '{eleitor['nro_endereco']}', 
                    nro_titulo = '{eleitor['nro_titulo']}', 
                    situacao = '{eleitor['situacao']}', 
                    secao = '{eleitor['secao']}', 
                    zona = '{eleitor['zona']}', 
                    local_votacao = '{eleitor['local_votacao']}', 
                    endereco_votacao = '{eleitor['endereco_votacao']}', 
                    bairro = '{eleitor['bairro']}',
                    municipio_uf = '{eleitor['municipio_uf']}', 
                    pais = '{eleitor['pais']}' 
                WHERE 
                    cpf = '{eleitor['cpf']}'
                """

        cursor.execute(sql)
        conect.commit()
    except Exception as ex:
        print(f'Erro: Falha na atualizacao: {ex}')
    finally:
        cursor.close()
        conect.close()

# Fim: atualizar_eleitor(eleitor)


def deletar_eleitor(cpf):
    try:
        # Manipular o banco de dados
        conect = database.criar_db()
        cursor = conect.cursor()
        sql = f'DELETE FROM eleitor WHERE cpf = {cpf}'
        cursor.execute(sql)
        conect.commit()
    except Exception as ex:
        print(f'Erro: Falha na deleção do eleitor: {ex}')
    finally:
        cursor.close()
        conect.close()

# Fim: deletar_eleitor(cpf)