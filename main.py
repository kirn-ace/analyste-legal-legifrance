from typing import Annotated

from mistralai import agents
from pydantic import Field


@agents.tool(model_access="direct")
def citation_legifrance(
    identifiant: Annotated[
        str,
        Field(
            description=(
                "Identifiant Legifrance exact du texte : LEGITEXT... (code, loi, decret) "
                "ou LEGIARTI... (article de code)."
            )
        ),
    ],
) -> dict[str, str]:
    """Donne l'URL officielle Legifrance et la forme de citation d'un texte ou d'un article."""
    identifiant = identifiant.strip()
    if identifiant.startswith("LEGIARTI"):
        url = f"https://www.legifrance.gouv.fr/codes/article_lc/{identifiant}"
        nature = "article de code"
    elif identifiant.startswith("LEGITEXT"):
        url = f"https://www.legifrance.gouv.fr/loda/id/{identifiant}"
        nature = "texte"
    else:
        raise agents.ToolError(
            f"'{identifiant}' n'est pas un identifiant Legifrance reconnu "
            "(attendu : LEGITEXT... ou LEGIARTI...)."
        )
    return {
        "identifiant": identifiant,
        "nature": nature,
        "url": url,
        "citation": f"Legifrance, {nature} {identifiant} : {url}",
    }


INSTRUCTIONS = """Tu es un analyste de donnees juridiques specialise dans le droit francais.
Tu reponds toujours en francais, de maniere claire, structuree et integralement sourcee.

Regles strictes :
- Pour toute question portant sur un article, un code, une loi, un decret, une ordonnance ou une decision de justice, utilise systematiquement les outils du serveur MCP "openlegi" pour recuperer le texte officiel a jour depuis Legifrance. Ne reponds jamais sur le contenu d'un article de memoire.
- Cite chaque information juridique par sa reference exacte (code, article, numero, identifiant LEGITEXT/LEGIARTI) et son URL Legifrance, via l'outil citation_legifrance.
- L'utilisateur peut te poser des questions de suivi dans la meme conversation : tu te souviens de tous les echanges precedents de la session.
- Tu ne disposes d'aucun outil d'execution de code : analyse les textes toi-meme, sans jamais executer de code arbitraire.
- Si un texte est introuvable, abroge ou ambigu, dis-le explicitement et propose des pistes de recherche precises.
"""

agent = agents.Agent(
    model="mistral-large-4",
    name="analyste-legal-legifrance",
    instructions=INSTRUCTIONS,
    tools=[citation_legifrance],
    mcps={
        "openlegi": agents.RemoteMCP(
            url="https://mcp.openlegi.fr/legifrance/mcp",
            auth_header_env_vars={"Authorization": "OPENLEGI_TOKEN"},
            model_access="direct",
        )
    },
)
