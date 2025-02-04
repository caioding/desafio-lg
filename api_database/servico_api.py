from flask import Flask, make_response, jsonify, request, Response
import mysql.connector


import repository.eleitor as eleitor

# Instanciar
app_api = Flask('api_database')
app_api.config['JSON_SORT_KEYS'] = False

# Implementar a lógica de programação

# --------------------------------------------------------
#           Inicio: Serviços da api usuário
# --------------------------------------------------------

# Rota pra inicio da API
@app_api.route("/", methods=["GET"])
def hello_world():
    return "API do Eleitor - OK"

# Inserir eleitor
@app_api.route('/eleitor', methods=['POST'])
def criar_eleitor():
    # Captura o JSON com os dados enviados pelo cliente
    eleitor_json = request.json  # corpo da requisição
    sucesso = False
    _mensagem = ""

    try:
        # Verifica se o CPF já existe
        if eleitor.existe_eleitor(eleitor_json['cpf']):
            raise Exception("CPF ja cadastrado.")
        
        eleitor.criar_eleitor(eleitor_json)
        sucesso = True
        _mensagem = 'Eleitor inserido com sucesso'
    except Exception as ex:
        _mensagem = f'Erro: Inclusao do eleitor: {ex}'
    
    return make_response(
        # Formata a resposta no formato JSON
        jsonify(
            status=sucesso,
            mensagem=_mensagem
        )
    )
# Fim: criar_eleitor()


# Atualizar eleitor
@app_api.route('/eleitor', methods=['PUT'])
def atualizar_eleitor():
    # Construir um Request
    # Captura o JSON com os dados enviado pelo cliente
    eleitor_json = request.json # corpo da requisição
    cpf = str(eleitor_json['cpf'])
    try:
        if eleitor.existe_eleitor(cpf) == True:
            eleitor.atualizar_eleitor(eleitor_json)
            sucesso = True
            _mensagem = 'Eleitor alterado com sucesso'
        else:
            sucesso = False
            _mensagem = 'Eleitor nao existe'
    except Exception as ex:
        sucesso = False
        _mensagem = f'Erro: Alteracao do eleitor: {ex}'
    
    return make_response(
        # Formata a resposta no formato JSON
        jsonify(
                status = sucesso,
                mensagem = _mensagem
        )
    )
#Fim de atualizar_eleitor


# Deletar eleitor
@app_api.route('/eleitor/<cpf>', methods=['DELETE'])
def deletar_eleitor(cpf):
    try:
        if eleitor.existe_eleitor(cpf) == True:
            eleitor.deletar_eleitor(cpf)
            sucesso = True
            _mensagem = 'Eleitor deletado com sucesso'
        else:
            sucesso = False
            _mensagem = 'Eleitor nao existe'
    except Exception as ex:
        sucesso = False
        _mensagem = f'Erro: Exclusao de eleitor: {ex}'
    
    return make_response(
        # Formata a resposta no formato JSON
        jsonify(
                status = sucesso,
                mensagem = _mensagem
        )
    )
# Fim: deletar_eleitor


# Serviço: Obter eleitor pelo cpf
@app_api.route('/eleitor/<cpf>', methods=['GET'])
def obter_eleitor_cpf(cpf):
    # Declarando uma tupla vazia
    eleitor_cpf = ()
    sucesso = False
    if eleitor.existe_eleitor(cpf) == True:
        eleitor_cpf = eleitor.obter_eleitor_cpf(cpf)
        sucesso = True
        _mensagem = 'Eleitor encontrado com sucesso'
    else:
        sucesso = False
        _mensagem = 'Eleitor nao existe'
    # Construir um Response
    return make_response(
        # Formata a resposta no formato JSON
        jsonify(
                status = sucesso,
                mensagem = _mensagem,
                dados = eleitor_cpf
        )
    )
# Fim: obter_eleitor_cpf


# Serviço: Obter a lista de eleitores
@app_api.route('/eleitor', methods=['GET'])
def lista_eleitor():
    lista_eleitor = list()
    lista_eleitor = eleitor.listar_eleitor()
    if len(lista_eleitor) == 0:
        sucesso = False
        _mensagem = 'Lista de eleitores vazia'
    else:
        sucesso = True
        _mensagem = 'Lista de eleitores'

    # Construir um Response
    return make_response(
        # Formata a resposta no formato JSON
        jsonify(
                status = sucesso,
                mensagem = _mensagem,
                dados = lista_eleitor
        )
    )
# Fim: lista_eleitor()

# -- Fim: Serviços da api eleitor ------------------------


# Levantar/Executar API REST: api_database
app_api.run()



