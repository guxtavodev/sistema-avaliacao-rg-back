from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avaliacoes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Habilita CORS para permitir requisições do frontend

# Modelo para Professores
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    turmas = db.relationship('Turma', secondary='professor_turma', back_populates='professores')

# Modelo para Turmas
class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(0), nullable=False)
    professores = db.relationship('Professor', secondary='professor_turma', back_populates='turmas')

# Tabela de associação entre Professores e Turmas
professor_turma = db.Table('professor_turma',
    db.Column('professor_id', db.Integer, db.ForeignKey('professor.id'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True)
)

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

# Modelo para Avaliações de Professores (8 perguntas)
class AvaliacaoProfessor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    avaliacao_ = db.Column(db.String(), nullable=False)
    avaliacao_2 = db.Column(db.String(), nullable=False)
    avaliacao_3 = db.Column(db.String(), nullable=False)
    avaliacao_4 = db.Column(db.String(), nullable=False)
    avaliacao_5 = db.Column(db.String(), nullable=False)
    avaliacao_6 = db.Column(db.String(), nullable=False)
    avaliacao_7 = db.Column(db.String(), nullable=False)
    avaliacao_8 = db.Column(db.String(), nullable=False)
    sugestoes = db.Column(db.Text, nullable=True)

# Modelo para Avaliações de Funcionários (6 perguntas)
class AvaliacaoFuncionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
    avaliacao_ = db.Column(db.String(), nullable=False)
    avaliacao_2 = db.Column(db.String(), nullable=False)
    avaliacao_3 = db.Column(db.String(), nullable=False)
    avaliacao_4 = db.Column(db.String(), nullable=False)
    avaliacao_5 = db.Column(db.String(), nullable=True)
    sugestoes = db.Column(db.Text, nullable=True)

# Modelo para Avaliações de Gestores (4 perguntas)
class AvaliacaoGestor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gestor_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
    avaliacao_ = db.Column(db.String(), nullable=False)
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
    return jsonify([{'id': professor.id, 'nome': professor.nome} for professor in professores])

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
    avaliacao = AvaliacaoProfessor(
        professor_id=data['professor_id'],
        turma_id=data['turma_id'],
        avaliacao_=data['avaliacao_'],
        avaliacao_2=data['avaliacao_2'],
        avaliacao_3=data['avaliacao_3'],
        avaliacao_4=data['avaliacao_4'],
        avaliacao_5=data['avaliacao_5'],
        avaliacao_6=data['avaliacao_6'],
        avaliacao_7=data['avaliacao_7'],
        avaliacao_8=data['avaliacao_8'],
        sugestoes=data.get('sugestoes', '')
    )
    db.session.add(avaliacao)
    db.session.commit()
    return jsonify({'message': 'Avaliação de professor registrada com sucesso!'}), 20

# Endpoint para registrar uma avaliação de funcionário
@app.route('/avaliacao_funcionario', methods=['POST'])
def avaliar_funcionario():
    data = request.get_json()
    avaliacao = AvaliacaoFuncionario(
        funcionario_id=data['funcionario_id'],
        avaliacao_=data['avaliacao_'],
        avaliacao_2=data['avaliacao_2'],
        avaliacao_3=data['avaliacao_3'],
        avaliacao_4=data['avaliacao_4'],
        avaliacao_5=data.get('avaliacao_5', ''),
        sugestoes=data.get('sugestoes', '')
    )
    db.session.add(avaliacao)
    db.session.commit()
    return jsonify({'message': 'Avaliação de funcionário registrada com sucesso!'}), 20

# Endpoint para registrar uma avaliação de gestor
@app.route('/avaliacao_gestor', methods=['POST'])
def avaliar_gestor():
    data = request.get_json()
    avaliacao = AvaliacaoGestor(
        gestor_id=data['gestor_id'],
        avaliacao_=data['avaliacao_'],
        avaliacao_2=data['avaliacao_2'],
        avaliacao_3=data['avaliacao_3'],
        avaliacao_4=data.get('avaliacao_4', ''),
        sugestoes=data.get('sugestoes', '')
    )
    db.session.add(avaliacao)
    db.session.commit()
    return jsonify({'message': 'Avaliação de gestor registrada com sucesso!'}), 20

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
