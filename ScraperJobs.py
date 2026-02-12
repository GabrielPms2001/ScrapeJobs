import csv # Necessário para escrever o arquivo CSV corretamente
from pathlib import Path # Necessário para lidar com caminhos de arquivos de forma portátil
from jobspy import scrape_jobs # Importa a função scrape_jobs do módulo jobspy, que é responsável por coletar as vagas de emprego

# A função main é o ponto de entrada do programa. Ela tenta coletar as vagas de emprego usando a função scrape_jobs e, em seguida, salva os resultados em um arquivo CSV. Se ocorrer algum erro durante a coleta ou salvamento, ele será capturado e uma mensagem de erro será exibida.
def main() -> None: 
    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor"], # Sites de emprego para coletar as vagas
            search_term="Analista de Dados", # Termo de busca para as vagas de emprego
            location="Brasil", # Coletar vagas em todo o Brasil
            results_wanted=100, # Coletar até 100 vagas
            hours_old=72,  # Vagas postadas nas ultimas 72 horas
        )
        # A função scrape_jobs retorna uma lista de dicionários, onde cada dicionário representa uma vaga de emprego com informações como título, empresa, local, data de postagem, etc.
    except Exception as exc: 
        print(f"Erro ao coletar vagas: {exc}")
        return
        # Se ocorrer um erro durante a coleta das vagas, ele será capturado e uma mensagem de erro será exibida. O programa então retorna, encerrando a execução.
    output_path = Path(__file__).resolve().parent / "vagas_extraidas.csv"
    try:
        jobs.to_csv(output_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
    except Exception as exc:
        print(f"Erro ao salvar arquivo CSV: {exc}")
        return
# O código acima tenta salvar as vagas coletadas em um arquivo CSV. O caminho do arquivo é definido usando a biblioteca pathlib para garantir que seja portátil. Se ocorrer um erro durante o salvamento do arquivo, ele será capturado e uma mensagem de erro será exibida. O programa então retorna, encerrando a execução.
    print(f"Encontradas {len(jobs)} vagas.")
    print(f"Arquivo salvo em: {output_path}")

# O bloco if __name__ == "__main__": é uma convenção em Python que garante que a função main() seja executada apenas quando o script for executado diretamente, e não quando for importado como um módulo em outro script.
if __name__ == "__main__":
    main()
