# Importa o SQLite para ler os dados salvos no arquivo "promocoes.db"
import sqlite3

# Importa o Flask (para criar o servidor web) e o render_template (para enviar dados ao HTML)
from flask import Flask, render_template

# Cria a aplicação web informando que a pasta atual ('.') guarda tanto o HTML quanto subpastas como 'assets'
app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")


# Define uma função auxiliar para transformar números (ex: 3499.0) em moeda brasileira ("R$ 3.499,00")
def formatar_moeda(valor):
    # Formata com 2 casas decimais e troca pontos e vírgulas para o padrão brasileiro
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# Define a rota principal ("/") do site, ou seja, o que acontece quando alguém abre a página inicial
@app.route("/")
def pagina_inicial():
    # Abre a conexão com o banco de dados criado pelo seu script atualizador.py
    conexao = sqlite3.connect("promocoes.db")

    # Configura o banco para devolver os resultados como dicionários (permitindo acessar pelo nome da coluna)
    conexao.row_factory = sqlite3.Row

    # Cria o cursor para executar comandos de consulta SQL
    cursor = conexao.cursor()

    # Busca todas as ofertas cadastradas, ordenando das mais recentes para as mais antigas (DESC)
    cursor.execute("SELECT * FROM ofertas ORDER BY id DESC")

    # Guarda todas as linhas encontradas em uma variável
    registros = cursor.fetchall()

    # Fecha a conexão com o banco após terminar a leitura
    conexao.close()

    # Cria uma lista vazia que vai armazenar os produtos já prontos e formatados para o HTML
    lista_ofertas = []

    # Percorre cada linha vinda do banco de dados, uma por uma
    for item in registros:
        # Pega o preço antigo e o preço atual do produto
        antigo = item["preco_antigo"]
        atual = item["preco_atual"]

        # Lógica de decisão: só calcula porcentagem de desconto se o preço atual for menor que o antigo
        if atual < antigo:
            # Calcula o percentual de desconto e arredonda para número inteiro
            desconto = round(((antigo - atual) / antigo) * 100)
        else:
            # Se o preço ainda não caiu desde o cadastro inicial, o desconto é zero
            desconto = 0

        # Monta um pacote organizado com os dados tratados e adiciona na lista final
        lista_ofertas.append({
            "loja": item["loja"],
            "titulo": item["titulo"],
            "imagem": item["imagem_url"],
            "preco_antigo": formatar_moeda(antigo),
            "preco_atual": formatar_moeda(atual),
            "desconto": desconto,
            "link": item["link_oficial"],
            "data": item["data_atualizacao"]
        })

    # Abre o "index.html" e envia a "lista_ofertas" para dentro dele com o nome "ofertas"
    return render_template("index.html", ofertas=lista_ofertas)


# Verifica se este arquivo está sendo executado diretamente e liga o servidor em modo de testes (debug=True)
if __name__ == "__main__":
    app.run(debug=True)