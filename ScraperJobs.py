import csv
from pathlib import Path
from jobspy import scrape_jobs


def main() -> None:
    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor"],
            search_term="Engenheiro de Dados",
            location="Brasil",
            results_wanted=20,
            hours_old=72,  # Vagas postadas nas ultimas 72 horas
        )
    except Exception as exc:
        print(f"Erro ao coletar vagas: {exc}")
        return

    output_path = Path(__file__).resolve().parent / "vagas_extraidas.csv"
    try:
        jobs.to_csv(output_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
    except Exception as exc:
        print(f"Erro ao salvar arquivo CSV: {exc}")
        return

    print(f"Encontradas {len(jobs)} vagas.")
    print(f"Arquivo salvo em: {output_path}")


if __name__ == "__main__":
    main()
