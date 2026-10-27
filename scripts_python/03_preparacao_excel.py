from pathlib import Path
import pandas as pd

pasta_projeto = Path(__file__).resolve().parent.parent

arquivo_csv = (
    pasta_projeto
    / "dados_tratados"
    / "resumo_atrasos_estado_mes.csv"
)

arquivo_excel = (
    pasta_projeto
    / "dados_tratados"
    / "base_entregas.xlsx"
)

resumo = pd.read_csv(
    arquivo_csv,
    sep=",",
    decimal=".",
    dtype={"mes_compra": str}
)

resumo.to_excel(
    arquivo_excel,
    sheet_name="Base_mensal",
    index=False,
    engine="openpyxl"
)

print("Base Excel criada:")
print(arquivo_excel)