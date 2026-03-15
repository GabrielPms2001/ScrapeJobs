import pandas as pd
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine

# Caminho base do projeto (duas pastas acima do arquivo atual)
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
JSON_PATH = DATA_DIR / "vaga_indeed.jsonl"

if not JSON_PATH.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {JSON_PATH}")

# =============================
# 2. CONEXÃO SQL SERVER
# =============================

SERVER = "localhost"  # exemplo: localhost ou DESKTOP-XXXX
DATABASE = "Database_Empregos"

engine = create_engine(
    f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# =============================
# 4. LEITURA DO JSONL
# =============================
df = pd.read_json(JSON_PATH, lines=True)

#pd.options.display.max_columns = None

# =============================
# 5. ENRIQUECIMENTO
# =============================

df['_data_coleta'] = datetime.now()
df['_Plataforma'] = "Indeed"

# =============================
# 6. TRATAMENTO DE DADOS
# =============================

df["Categoria"] = df["cargo_busca"].fillna("Sem categoria").astype(str)
df["Titulo"] = df["titulo"].fillna("Sem título").astype(str)
df["Empresa"] = df["empresa"].fillna("Sem empresa").astype(str)
df["Local"] = df["local"].fillna("Sem localização").astype(str)
df["Data_de_postagem"] = None
df["Link"] = df["link"].fillna("Sem link").astype(str)
df["Imagem_Logo"] = None

# =============================
# 7. AJUSTES FINAIS
# =============================

df = df.drop(
    columns=["cargo_busca", "titulo", "local", "date_posted", "link", "Logo_image", "empresa"],
    errors="ignore"
)


# =============================
# 8. SALVAR NO SQL SERVER
# =============================
df.to_sql(
    "Vagas",          # nome da tabela
    engine,              # conexão SQL Server
    if_exists="append", # replace ou append -> replace apaga a tabela e cria uma nova, append adiciona os dados na tabela existente
    index=False
)

# =============================
# 9. VALIDAÇÃO FINAL
# =============================

print("✅ Carga concluída com sucesso no SQL Server")

print("\nPrimeiras linhas:")
print(df.head())

print("\nTipos das colunas:\n")
print(df.dtypes)