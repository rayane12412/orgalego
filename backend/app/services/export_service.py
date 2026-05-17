"""Service d'export des diagnostics (PDF, Excel) - implémentation minimale."""

import io
import json
from app.schemas.diagnosis import Diagnosis


def export_diagnosis_to_json(diagnosis: Diagnosis) -> bytes:
    """Export simple en JSON."""
    return json.dumps(diagnosis.model_dump(), indent=2, ensure_ascii=False).encode("utf-8")


def export_diagnosis_to_pdf(diagnosis: Diagnosis) -> bytes:
    """Export PDF via matplotlib (version minimale, à enrichir).

    Pour le MVP on génère un PDF textuel simple. Une version plus aboutie
    utilisera reportlab ou un template HTML+weasyprint.
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
    except ImportError:
        # Si matplotlib n'est pas dispo, on retourne du JSON dans un fichier "PDF"
        return export_diagnosis_to_json(diagnosis)

    buf = io.BytesIO()
    with PdfPages(buf) as pdf:
        fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 portrait
        ax.axis("off")
        text = "OrgaLego - Rapport de diagnostic\n\n"
        text += f"Calculé le : {diagnosis.computed_at}\n\n"

        if diagnosis.community_result:
            text += f"Modularité : {diagnosis.community_result.modularity}\n"
            text += f"Nombre de communautés : {diagnosis.community_result.n_communities}\n\n"

        if diagnosis.best_archetype:
            text += f"Archétype dominant : {diagnosis.best_archetype.archetype_name}\n"
            text += f"École : {diagnosis.best_archetype.school}\n"
            text += f"Similarité : {diagnosis.best_archetype.similarity}\n\n"

        text += "Recommandations :\n"
        for reco in diagnosis.recommendations:
            text += f"  [{reco.severity}] {reco.message}\n"

        ax.text(0.05, 0.95, text, va="top", ha="left", fontsize=10, family="monospace")
        pdf.savefig(fig)
        plt.close(fig)

    return buf.getvalue()
