# projeto IEFP
Título do Projeto: Sistema de Login e Logs

Descrição: O sistema de login e logs é um projeto que visa criar um sistema de autenticação de usuários e registro de logs de atividades.

Funcionalidades:

Autenticação de usuários
Registro de logs de atividades
Visualização de logs

Tecnologias Utilizadas:

Python
Flask
HTML
CSS
JavaScript

Banco de dados:
MongoDB

Arquitetura do Projeto:

O projeto é dividido em três partes principais:
Autenticação de usuários: responsável por verificar as credenciais do usuário e autenticá-lo no sistema.
Registro de logs: responsável por registrar as atividades do usuário no sistema.
Visualização de logs: responsável por exibir os logs registrados.

Componentes do Projeto:
app.py: responsável por executar o aplicativo e definir as rotas.
DB.py: responsável por interagir com o banco de dados e realizar operações de CRUD.
logs.py: responsável por registrar e visualizar os logs.
templates: pasta que contém os arquivos HTML para a interface do usuário.
static: pasta que contém os arquivos estáticos, como CSS e JavaScript.
Instalação e Execução:

Clone o repositório do GitHub.
Instale as dependências necessárias com pip install -r requirements.txt.
Mude o banco de dados que vai ser acessado no codigo, use o seu proprio mongoDB e o configure
Execute o aplicativo com python app.py.
Acesse o sistema em http://localhost:5000.
