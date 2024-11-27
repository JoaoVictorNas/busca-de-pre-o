from bs4 import BeautifulSoup
import requests
import pymysql
import streamlit as st

st.set_page_config(page_title="Busca de Preço")
st.write("Faça a busca de preço")
st.button("executar")

# Abrir a conexão com o banco ==================================================
def abrirBanco():
    try:
        con = pymysql.connect(
            host='db_melhor_colc.vpshost2821.mysql.dbaas.com.br',
            database='db_melhor_colc',
            user='db_melhor_colc',
            password='a426pRcVE@n@BL',
            port=3306
        )
        print("Conexão com o banco de dados aberta.")
        return con
    except pymysql.MySQLError as err:
        print("Erro ao conectar ao MySQL (PyMySQL):", err)
        return None
    except Exception as e:
        print("Erro inesperado:", e)
        return None


# Buscar URLs da tabela produto_url ============================================
def obterUrls(con):
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT sku, URL_Emcompre FROM produtos_url")
            urls = cursor.fetchall()
        return urls
    except pymysql.MySQLError as err:
        print("Erro ao buscar URLs no banco:", err)
        return []


# Salvar preços na tabela produtos_precos ======================================
def salvarPreco(con, sku, precoBhan, precoVista, precoPrazo):
    try:
        with con.cursor() as cursor:
            cursor.execute("""
                INSERT INTO produtos_precos (sku, precoBhan, precoVista, precoPrazo)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                precoBhan = VALUES(precoBhan),
                precoVista = VALUES(precoVista),
                precoPrazo = VALUES(precoPrazo)
            """, (sku, precoBhan, precoVista, precoPrazo))
        con.commit()
        print(f"Preços salvos para SKU {sku}: Bhan - {precoBhan}, Vista - {precoVista}, Prazo - {precoPrazo}")
    except pymysql.MySQLError as err:
        print("Erro ao salvar preços no banco:", err)


# Buscar dados no site =========================================================
def site(con):
    urls = obterUrls(con)
    if not urls:
        print("Nenhuma URL encontrada no banco.")
        return

    for sku, url in urls:
        try:
            html = requests.get(url).content
            soup = BeautifulSoup(html, 'html.parser')
            precos = soup.find_all("span", class_="price")
            precoVista = precos[2].text.strip() if len(precos) > 2 else None
            precoPrazo = precos[1].text.strip() if len(precos) > 1 else None
            precoBhan = precos[0].text.strip() if len(precos) > 0 else None

            if precoVista or precoPrazo:
                salvarPreco(con, sku, precoBhan, precoVista, precoPrazo)
            else:
                print(f"Nenhum preço encontrado para SKU {sku} na URL: {url}")
        except Exception as e:
            print(f"Erro ao buscar preços para SKU {sku} na URL {url}:", e)


# MAIN =========================================================================
def main():
    print("Fazer pesquisas de preço")
    print("========================")
    print("1- Fazer pesquisa no site")

    op = input('Digite o número das plataformas: ')

    con = abrirBanco()

    if con is not None:
        if op == "1":
            site(con)
        con.close()
        print("Conexão com o banco de dados encerrada.")


# CHAMA O MAIN =================================================================
if __name__ == "__main__":
    main()
