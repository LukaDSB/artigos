import requests
from bs4 import BeautifulSoup
import urllib3

# Desabilita os avisos de requisição insegura (InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extrair_titulos_paginados(url_base, publisher_alvo):
    """
    Percorre todas as páginas de submissões recentes, extraindo os títulos 
    cujos publishers contenham o valor desejado (ex: 'Alegre'), além de autor e data.
    """
    offset = 0
    passo = 20
    resultados = []
    pagina = 1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    while True:
        url = f"{url_base}?offset={offset}"
        print(f"\n➡️ Buscando na página {pagina} (offset={offset})...")

        try:
            resposta = requests.get(url, timeout=15, verify=False, headers=headers)
            resposta.raise_for_status()
            soup = BeautifulSoup(resposta.content, 'html.parser')

            trabalhos = soup.select('div.artifact-description')
            print(f"   → {len(trabalhos)} trabalhos encontrados.")

            if not trabalhos:
                break  # Fim das páginas

            for trabalho in trabalhos:
                titulo_tag = trabalho.select_one('h4.artifact-title > a')
                publisher_tag = trabalho.select_one('span.publisher')
                data_tag = trabalho.select_one('span.date')
                autor_tag = trabalho.select_one('span.author > span')

                if titulo_tag and publisher_tag:
                    titulo = titulo_tag.get_text(strip=True)
                    publisher = publisher_tag.get_text(strip=True)

                    if publisher_alvo.lower() in publisher.lower():
                        autor = autor_tag.get_text(strip=True) if autor_tag else "Autor não encontrado"
                        data_publicacao = data_tag.get_text(strip=True) if data_tag else "Data não encontrada"

                        resultados.append({
                            'titulo': titulo,
                            'pagina': pagina,
                            'offset': offset,
                            'autor': autor,
                            'data': data_publicacao
                        })

            offset += passo
            pagina += 1

        except requests.RequestException as e:
            print(f"Erro ao acessar a URL: {e}")
            break

    return resultados

# --- Execução do Script ---
if __name__ == "__main__":
    URL_BASE = "https://repositorio.ifes.edu.br/handle/123456789/100/recent-submissions"
    PUBLISHER_ALVO = "Alegre"

    print(f"Iniciando busca por títulos com publisher '{PUBLISHER_ALVO}'...\n")
    titulos_encontrados = extrair_titulos_paginados(URL_BASE, PUBLISHER_ALVO)

    total = len(titulos_encontrados)
    print(f"\n✅ Total de títulos encontrados com publisher '{PUBLISHER_ALVO}': {total}\n")

    if titulos_encontrados:
        print("--- Lista de Títulos ---")
        for i, item in enumerate(titulos_encontrados, 1):
            print(f"{i}. {item['titulo']}")
            print(f"   Autor: {item['autor']}")
            print(f"   Data: {item['data']}")
            print(f"   Página: {item['pagina']} (offset={item['offset']})\n")
    else:
        print("Nenhum título encontrado.")
