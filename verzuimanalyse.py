"""Vereenvoudigde verzuimanalyse.

Deze functie kan zowel een geïntegreerd tekstveld als een bestand analyseren.
Wanneer er geen tekst beschikbaar is, wordt een melding teruggegeven. De analyse
beperkt zich tot een woordentelling als voorbeeld van een verkorte analyse.
"""

def analyse_verzuim(
    filename: str | None = None,
    contents: bytes | None = None,
    input_text: str | None = None,
    sbi_code: str = "6420",
    periode: str = "2025KW2",
) -> dict:
    text = ""
    if input_text:
        text = input_text
    elif contents:
        try:
            text = contents.decode("utf-8", errors="ignore")
        except Exception:
            text = ""

    if not text:
        return {"status": "geen input", "advies": "Geen tekst beschikbaar voor analyse."}

    word_count = len(text.split())
    return {"status": "ok", "verkorte_analyse": f"Ontvangen tekst bevat {word_count} woorden."}

def analyse_meerdere(files):
    """Analyseer meerdere bestanden en verzamel de resultaten."""
    results = []
    for name, data in files:
        try:
            results.append(analyse_verzuim(name, data))
        except Exception as exc:
            results.append({"filename": name, "error": str(exc)})
    return results

def genereer_pdf(markdown):
    from weasyprint import HTML
    html = HTML(string=markdown.replace('\n', '<br>'))
    return html.write_pdf()

def genereer_grafiek(data):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.bar(["Intern", "Benchmark"], [data.get("verzuimpercentage", 0), data.get("cbs_benchmark", {}).get("waarde", 0)])
    ax.set_title("Verzuim vs Benchmark")
    return fig
