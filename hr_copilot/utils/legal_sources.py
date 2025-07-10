def check_legality(document):
    if "beëindigingsovereenkomst" in document.lower():
        return "Let op: controleer of aan alle vereisten voor een VSO is voldaan, zoals bedenktijd en transitievergoeding."
    return "Document is juridisch niet direct risicovol, maar laat altijd controleren door een jurist."