# Sistema de Avaliação Escolar

Este projeto é um sistema de avaliação escolar desenvolvido em Flask, que permite que alunos avaliem professores, funcionários e gestores em uma instituição de ensino. O sistema utiliza um banco de dados SQLite para armazenar as informações sobre turmas, professores, funcionários e as avaliações realizadas.

## Tecnologias Utilizadas

- **Flask**: Framework web para Python.
- **Flask-SQLAlchemy**: ORM para gerenciar o banco de dados SQLite.
- **Flask-CORS**: Habilita o suporte a CORS, permitindo que o frontend faça requisições à API.
- **SQLite**: Banco de dados leve para armazenar dados.

## Funcionalidades

- Listar turmas e professores.
- Listar funções e funcionários.
- Registrar avaliações de professores, funcionários e gestores.
- Permitir a autoavaliação dos alunos de forma estruturada.

## Estrutura do Projeto

projeto_avaliacao/ │ 
├── main.py 
├── avaliacoes.db 
├── templates/ 
│ ├── (pasta para templates HTML se necessário) 
  ├── static/ 
  │ └── css/ (pasta para arquivos CSS se necessário)
