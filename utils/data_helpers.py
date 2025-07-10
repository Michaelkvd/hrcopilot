def analyse_verzuimdata(data):
    # Placeholder voor verzuimanalyse
    return f"Analyse van verzuimdata uitgevoerd op {len(data)} datapunten."

def analyse_hrdata(huidige, vorige):
    verschil = {k: huidige[k] - vorige.get(k, 0) for k in huidige}
    return {
        "verschillen": verschil,
        "samenvatting": "Belangrijkste verschillen zijn geanalyseerd en klaar voor HR-MT bespreking."
    }