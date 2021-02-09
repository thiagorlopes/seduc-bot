import pandas as pd

while True:

    fontes = ["goinfra", "sinapi", "composicao"]
    text = input("Código: ")

    if not text:
        break

    text = text.lower().replace("ç", "c").replace("ã", "a")
    fonte, codigo = text.split(" ")

    print("Fonte: " + fonte)
    print("Código: " + codigo)

    if fonte in fontes:
        sintetica_filepath = f"app/data/{fonte}-sintetica.xlsx"
        analitica_filepath = f"app/data/{fonte}-analitica.xlsx"

        sintetica = pd.read_excel(sintetica_filepath)
        analitica = pd.read_excel(analitica_filepath)

        descricao = sintetica.loc[sintetica['CODIGO DA COMPOSICAO'] == codigo]['DESCRICAO DA COMPOSICAO'].values
        composicao_analitica = analitica[analitica['CODIGO DA COMPOSICAO'] == codigo]
