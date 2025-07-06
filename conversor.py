import pandas as pd

# Inicializa lista para armazenar os dados
dados = []

# Lê o arquivo txt
with open("titulos_extraidos.txt", "r", encoding="utf-8") as file:
    linhas = file.readlines()

# Extrai os dados por blocos de 4 linhas (1 título + 3 detalhes)
i = 0
while i < len(linhas):
    linha = linhas[i].strip()
    if linha and linha[0].isdigit() and ". " in linha:
        titulo = linha.split(". ", 1)[1].strip()
        autor = linhas[i+1].replace("Autor:", "").strip()
        data = linhas[i+2].replace("Data:", "").strip()
        pagina_offset = linhas[i+3].strip().replace("Página:", "").strip()
        pagina, offset = pagina_offset.split("(offset=")
        pagina = pagina.strip()
        offset = offset.replace(")", "").strip()

        dados.append({
            "Título": titulo,
            "Autor": autor,
            "Data": data,
            "Página": int(pagina),
            "Offset": int(offset)
        })

        i += 5  # Pula para o próximo bloco
    else:
        i += 1

# Cria DataFrame e exporta para Excel
df = pd.DataFrame(dados)
df.to_excel("titulos.xlsx", index=False)

print("✅ Arquivo 'titulos.xlsx' criado com sucesso!")
