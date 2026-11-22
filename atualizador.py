# Importa a biblioteca nativa do Python para manipular o banco de dados SQLite
import sqlite3

# Importa a biblioteca para capturar a data e a hora atuais do sistema
from datetime import datetime

# Conecta ao arquivo de banco de dados "promocoes.db"
conexao = sqlite3.connect("promocoes.db")

# Cria o cursor responsável por executar comandos SQL no banco
cursor = conexao.cursor()

# Garante que a tabela "ofertas" exista no banco de dados
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ofertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        loja TEXT NOT NULL,
        titulo TEXT NOT NULL UNIQUE,
        categoria TEXT NOT NULL,
        imagem_url TEXT NOT NULL,
        preco_antigo REAL NOT NULL,
        preco_atual REAL NOT NULL,
        link_oficial TEXT NOT NULL,
        data_atualizacao TEXT NOT NULL
    )
""")

# Comando SQL DELETE: procura e apaga definitivamente o notebook antigo do banco de dados
cursor.execute("DELETE FROM ofertas WHERE titulo = ?", ("Notebook Core i5 16GB RAM SSD 512GB",))

# Salva a exclusão do produto antigo imediatamente no banco
conexao.commit()


# Define a função que cadastra uma oferta nova ou atualiza uma oferta existente
def registrar_ou_atualizar_oferta(loja, titulo, categoria, imagem_url, preco_antigo, preco_novo, link_oficial):

    # Captura a data e hora atual no formato brasileiro (Dia/Mês/Ano Hora:Minuto)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Consulta se o produto já está cadastrado no banco
    cursor.execute("SELECT id, preco_atual FROM ofertas WHERE titulo = ?", (titulo,))

    # Guarda o resultado da consulta (None se não existir)
    produto_existente = cursor.fetchone()

    # Se o produto ainda NÃO existe no banco, insere ele como novo registro
    if produto_existente is None:

        # Grava os dados do produto no banco de dados
        cursor.execute("""
            INSERT INTO ofertas (loja, titulo, categoria, imagem_url, preco_antigo, preco_atual, link_oficial, data_atualizacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (loja, titulo, categoria, imagem_url, preco_antigo, preco_novo, link_oficial, agora))

        # Confirma no terminal que o novo produto foi inserido
        print(f"[NOVO] Produto exibido no site: {titulo}")

    # Se o produto JÁ existe no banco, apenas atualiza as informações dele
    else:

        # Extrai o ID e o preço salvo anteriormente
        id_produto, preco_salvo = produto_existente

        # Atualiza imagem, preços, link e horário da verificação
        cursor.execute("""
            UPDATE ofertas
            SET preco_antigo = ?, preco_atual = ?, imagem_url = ?, link_oficial = ?, data_atualizacao = ?
            WHERE id = ?
        """, (preco_antigo, preco_novo, imagem_url, link_oficial, agora, id_produto))

        # Confirma no terminal que o produto foi atualizado
        print(f"[ATUALIZADO] Produto sincronizado: {titulo}")

    # Salva todas as alterações no arquivo promocoes.db
    conexao.commit()


# --- LISTA DE OFERTAS QUE DEVEM APARECER NO SITE ---

ofertas_coletadas = [
    {
        "loja": "Kabum",
        # Novo modelo Asus Vivobook que substitui o Core i5 antigo
        "titulo": 'Notebook Asus Vivobook Go 15 E1504fa Amd Ryzen 5 7520u 16gb Ram 512gb SSD Linux Keepos Tela 15,6" LED Fhd Black - Nj1288',
        "categoria": "Informática",
        # Caminho da foto salva na sua pasta assets/img/ (ou cole o link https://... da imagem da Kabum)
        "imagem_url": "assets/img/vivobook.jpg",
        # Preço original antes do desconto (use ponto no lugar da vírgula)
        "preco_antigo": 3599.00,
        # Preço promocional atual
        "preco_novo": 2799.00,
        # Link oficial da página desse produto na Kabum
        "link_oficial": "https://www.kabum.com.br"
    },
    {
        "loja": "Amazon",
        "titulo": "Fone de Ouvido Bluetooth Cancelamento de Ruído",
        "categoria": "Eletrônicos",
        "imagem_url": "assets/img/fone.jpg",
        "preco_antigo": 599.00,
        "preco_novo": 419.00,
        "link_oficial": "https://www.amazon.com.br"
    },
    {
        "loja": "Magazine Luiza",
        "titulo": 'Monitor IPS 27" Full HD 144Hz HDMI/DisplayPort',
        "categoria": "Informática",
        "imagem_url": "assets/img/monitor.jpg",
        "preco_antigo": 1450.00,
        "preco_novo": 1099.00,
        "link_oficial": "https://www.magazineluiza.com.br"
    }
]

# Percorre a lista e envia cada produto para ser gravado no banco de dados
for item in ofertas_coletadas:
    registrar_ou_atualizar_oferta(
        item["loja"],
        item["titulo"],
        item["categoria"],
        item["imagem_url"],
        item["preco_antigo"],
        item["preco_novo"],
        item["link_oficial"]
    )

# Fecha a conexão com o banco de dados
conexao.close()