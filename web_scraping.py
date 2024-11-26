from bs4 import BeautifulSoup
import requests

# BUSCA NO SITE ================================================================
def site():
    html = requests.get("https://emcompre.com.br/colchao-casal-molas-ensacadas-bamboo-138x188x21cm-bf-colchoes.html").content
    soup = BeautifulSoup(html, 'html.parser')
    precos = soup.find_all("span", class_="price")
    precoVista = precos[2].text.strip() if len(precos) > 2 else "Preço à vista não encontrado."
    precoPrazo = precos[1].text.strip() if len(precos) > 1 else "Preço a prazo não encontrado."
    print("Preço à Vista:", precoVista)
    print("Preço a Prazo:", precoPrazo)

# MAIN =========================================================================
def main():
    print("Fazer pesquisas de preço")
    print("========================")
    print("1- Fazer pesquisa no site")

    op = input('Digite o número das plataformas: ')

    if op == "1":
        site()

# CHAMA O MAIN =================================================================
if __name__ == "__main__":
    main()