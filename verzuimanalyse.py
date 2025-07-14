def analyse_verzuim(filename, contents, sbi_code='6420', periode='2025KW2'):
    return {}


async def analyse_meerdere(files):
    results = []
    for file in files:
        try:
            contents = await file.read()
            result = analyse_verzuim(file.filename, contents)
        except Exception as exc:
            result = {"filename": getattr(file, "filename", "unknown"), "error": str(exc)}
        results.append(result)
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
