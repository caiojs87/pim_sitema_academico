# Importa a classe Flask do módulo flask
from flask import Flask

# Cria uma instância da aplicação Flask
# O __name__ indica ao Flask onde está o arquivo principal da aplicação
app = Flask(__name__)

# Define uma rota (endereço) para a página inicial do site
# Quando o usuário acessa o caminho '/', a função 'home' será executada
@app.route('/')
def home():
    # Retorna um texto HTML simples para o navegador
    return "<h1>✅ Flask está funcionando!</h1>"

# Verifica se o arquivo está sendo executado diretamente
# (ou seja, não foi importado como módulo em outro arquivo)
if __name__ == '__main__':
    # Inicia o servidor Flask em modo debug
    # Isso faz com que o servidor recarregue automaticamente ao modificar o código
    # e também mostra mensagens de erro detalhadas
    app.run(debug=True)
