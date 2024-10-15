from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avaliacoes2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Habilita CORS para permitir requisições do frontend

# Tabela de associação entre Professores e Turmas
professor_turma = db.Table('professor_turma',
    db.Column('professor_id', db.Integer, db.ForeignKey('professor.id'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True)
)

# Modelo para Professores
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    turmas = db.relationship('Turma', secondary=professor_turma, back_populates='professores')

# Modelo para Turmas
class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    professores = db.relationship('Professor', secondary=professor_turma, back_populates='turmas')

# Modelo para Funções
class Funcao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    funcionarios = db.relationship('Funcionario', backref='funcao', lazy=True)

# Modelo para Funcionários
class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    funcao_id = db.Column(db.Integer, db.ForeignKey('funcao.id'), nullable=False)

# Modelo para Avaliações de Professores (14 perguntas)
class AvaliacaoProfessor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    avaliacao_1 = db.Column(db.String(), nullable=False)
    avaliacao_2 = db.Column(db.String(), nullable=False)
    avaliacao_3 = db.Column(db.String(), nullable=False)
    avaliacao_4 = db.Column(db.String(), nullable=False)
    avaliacao_5 = db.Column(db.String(), nullable=False)
    avaliacao_6 = db.Column(db.String(), nullable=False)
    avaliacao_7 = db.Column(db.String(), nullable=False)
    avaliacao_8 = db.Column(db.String(), nullable=False)
    avaliacao_9 = db.Column(db.String(), nullable=False)
    avaliacao_10 = db.Column(db.String(), nullable=False)
    avaliacao_11 = db.Column(db.String(), nullable=False)
    avaliacao_12 = db.Column(db.String(), nullable=False)
    avaliacao_13 = db.Column(db.String(), nullable=False)
    avaliacao_14 = db.Column(db.String(), nullable=False)
    sugestoes = db.Column(db.Text, nullable=True)


# Modelo para Avaliações de Funcionários (6 perguntas)
class AvaliacaoFuncionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
    avaliacao_1 = db.Column(db.String(), nullable=False)
    avaliacao_2 = db.Column(db.String(), nullable=False)
    avaliacao_3 = db.Column(db.String(), nullable=False)
    avaliacao_4 = db.Column(db.String(), nullable=False)
    avaliacao_5 = db.Column(db.String(), nullable=True)
    sugestoes = db.Column(db.Text, nullable=True)

# Modelo para Avaliações de Gestores (4 perguntas)
class AvaliacaoGestor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gestor_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
    avaliacao_1 = db.Column(db.String(), nullable=False)
    avaliacao_2 = db.Column(db.String(), nullable=False)
    avaliacao_3 = db.Column(db.String(), nullable=False)
    avaliacao_4 = db.Column(db.String(), nullable=True)
    sugestoes = db.Column(db.Text, nullable=True)

# Inicializar o banco de dados
with app.app_context():
    db.create_all()

# Endpoint para listar todas as turmas
@app.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = Turma.query.all()
    return jsonify([{'id': turma.id, 'nome': turma.nome} for turma in turmas])

# Endpoint para obter professores de uma turma específica
@app.route('/turmas/<int:turma_id>/professores', methods=['GET'])
def get_professores_por_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    professores = turma.professores

    return jsonify([
        {
            'id': professor.id,
            'nome': professor.nome,
            'turmas': [turma.nome for turma in professor.turmas]  # Lista de nomes das turmas
        } for professor in professores
    ])

# Endpoint para listar funções
@app.route('/funcoes', methods=['GET'])
def get_funcoes():
    funcoes = Funcao.query.all()
    return jsonify([{'id': funcao.id, 'nome': funcao.nome} for funcao in funcoes])

# Endpoint para listar funcionários por função
@app.route('/funcoes/<int:funcao_id>/funcionarios', methods=['GET'])
def get_funcionarios_por_funcao(funcao_id):
    funcionarios = Funcionario.query.filter_by(funcao_id=funcao_id).all()
    return jsonify([{'id': funcionario.id, 'nome': funcionario.nome} for funcionario in funcionarios])

# Endpoint para registrar uma avaliação de professor
@app.route('/avaliacao_professor', methods=['POST'])
def avaliar_professor():
    data = request.get_json()
    print(data)
    # Certifique-se de que todas as avaliações são fornecidas
    required_fields = [f'avaliacao_{i}' for i in range(1, 15)]
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'O campo {field} é obrigatório.'}), 400

    avaliacao = AvaliacaoProfessor(
        professor_id=data['professor_id'],
        turma_id=data['turma_id'],
        avaliacao_1=data['avaliacao_1'],
        avaliacao_2=data['avaliacao_2'],
        avaliacao_3=data['avaliacao_3'],
        avaliacao_4=data['avaliacao_4'],
        avaliacao_5=data['avaliacao_5'],
        avaliacao_6=data['avaliacao_6'],
        avaliacao_7=data['avaliacao_7'],
        avaliacao_8=data['avaliacao_8'],
        avaliacao_9=data['avaliacao_9'],
        avaliacao_10=data['avaliacao_10'],
        avaliacao_11=data['avaliacao_11'],
        avaliacao_12=data['avaliacao_12'],
        avaliacao_13=data['avaliacao_13'],
        avaliacao_14=data['avaliacao_14'],
        sugestoes=data.get('sugestoes', '')
    )
    db.session.add(avaliacao)
    db.session.commit()
    return jsonify({'message': 'Avaliação de professor registrada com sucesso!'}), 201


# Endpoint para registrar uma avaliação de funcionário
@app.route('/avaliacao_funcionario', methods=['POST'])
def avaliar_funcionario():
    data = request.get_json()
    avaliacao = AvaliacaoFuncionario(
        funcionario_id=data['funcionario_id'],
        avaliacao_1=data['avaliacao_1'],
        avaliacao_2=data['avaliacao_2'],
        avaliacao_3=data['avaliacao_3'],
        avaliacao_4=data['avaliacao_4'],
        avaliacao_5=data.get('avaliacao_5', ''),
        sugestoes=data.get('sugestoes', '')
    )
    db.session.add(avaliacao)
    db.session.commit()
    return jsonify({'message': 'Avaliação de funcionário registrada com sucesso!'}), 201

# Endpoint para registrar uma avaliação de gestor
@app.route('/avaliacao_gestor', methods=['POST'])
def avaliar_gestor():
    data = request.get_json()
    avaliacao = AvaliacaoGestor(
        gestor_id=data['gestor_id'],
        avaliacao_1=data['avaliacao_'],
        avaliacao_2=data['avaliacao_2'],
        avaliacao_3=data['avaliacao_3'],
        avaliacao_4=data.get('avaliacao_4', ''),
        sugestoes=data.get('sugestoes', '')
    )
    db.session.add(avaliacao)
    db.session.commit()
    return jsonify({'message': 'Avaliação de gestor registrada com sucesso!'}), 201

# Endpoint para adicionar um novo professor com turmas
@app.route('/add_professor', methods=['POST'])
def add_professor():
    data = request.get_json()

    # Verifica se o nome e as turmas foram fornecidos
    if 'nome' not in data or not data['nome']:
        return jsonify({'error': 'Nome do professor é obrigatório.'}), 400

    if 'turmas' not in data or not isinstance(data['turmas'], list):
        return jsonify({'error': 'É necessário fornecer uma lista de turmas.'}), 400

    novo_professor = Professor(nome=data['nome'])

    # Associar o professor às turmas
    for turma_id in data['turmas']:
        turma = Turma.query.get(turma_id)
        if turma:
            novo_professor.turmas.append(turma)

    db.session.add(novo_professor)
    db.session.commit()
    return jsonify({'message': 'Professor adicionado com sucesso!'}), 201

# Endpoint para adicionar um novo funcionário
@app.route('/add_funcionario', methods=['POST'])
def add_funcionario():
    try:
        data = request.get_json()
    
        # Verifica se o nome e a função foram fornecidos
        if 'nome' not in data or not data['nome']:
            return jsonify({'error': 'Nome do funcionário é obrigatório.'}), 400
    
        if 'funcao_id' not in data:
            return jsonify({'error': 'ID da função é obrigatório.'}), 400
    
        novo_funcionario = Funcionario(nome=data['nome'], funcao_id=data['funcao_id'])
        db.session.add(novo_funcionario)
        db.session.commit()
        return jsonify({'message': 'Funcionário adicionado com sucesso!'}), 201
    except Exception as e:
        print(f"erro: {e}")

# Endpoint para adicionar um novo gestor
@app.route('/add_gestor', methods=['POST'])
def add_gestor():
    data = request.get_json()

    # Verifica se o nome e a função foram fornecidos
    if 'nome' not in data or not data['nome']:
        return jsonify({'error': 'Nome do gestor é obrigatório.'}), 400

    if 'funcao_id' not in data:
        return jsonify({'error': 'ID da função é obrigatório.'}), 400

    novo_gestor = Funcionario(nome=data['nome'], funcao_id=data['funcao_id'])  # Assume que gestores também são funcionários
    db.session.add(novo_gestor)
    db.session.commit()
    return jsonify({'message': 'Gestor adicionado com sucesso!'}), 201

# Endpoint para adicionar uma nova turma
@app.route('/add_turma', methods=['POST'])
def add_turma():
    data = request.get_json()

    # Verifica se o nome da turma foi fornecido
    if 'nome' not in data or not data['nome']:
        return jsonify({'error': 'Nome da turma é obrigatório.'}), 400

    nova_turma = Turma(nome=data['nome'])
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify({'message': 'Turma adicionada com sucesso!'}), 201

# Endpoint para listar todos os professores
@app.route('/professores', methods=['GET'])
def get_professores():
    professores = Professor.query.all()
    return jsonify([
        {
            'id': professor.id,
            'nome': professor.nome,
            'turmas': [turma.nome for turma in professor.turmas]  # Listar as turmas associadas
        } for professor in professores
    ])

# Endpoint para listar todos os gestores
@app.route('/gestores', methods=['GET'])
def get_gestores():
    gestores = Funcionario.query.filter(Funcao.nome == 'Gestor Escolar').all()  # Filtra funcionários com a função "Gestor"
    return jsonify([{'id': gestor.id, 'nome': gestor.nome, 'funcao_id': gestor.funcao_id} for gestor in gestores])

# Endpoint para adicionar uma nova função
@app.route('/add_funcao', methods=['POST'])
def add_funcao():
    data = request.get_json()

    # Verifica se o nome da função foi fornecido
    if 'nome' not in data or not data['nome']:
        return jsonify({'error': 'Nome da função é obrigatório.'}), 400

    nova_funcao = Funcao(nome=data['nome'])
    db.session.add(nova_funcao)
    db.session.commit()
    return jsonify({'message': 'Função adicionada com sucesso!'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
