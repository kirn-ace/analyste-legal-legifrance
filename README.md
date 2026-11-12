# analyste-legal-legifrance

Agent analyste de données juridiques spécialisé dans le droit français, adossé au serveur MCP [openlegi.fr](https://mcp.openlegi.fr/legifrance/mcp) (Legifrance).

## Fonctionnalités

- Analyse de textes juridiques (codes, lois, décrets, ordonnances, décisions) à partir des sources officielles Legifrance
- Citations sourcées via l’outil local `citation_legifrance` (identifiants `LEGITEXT` / `LEGIARTI` et URL Legifrance)
- Accès au texte à jour via le MCP distant **openlegi** (variable d’environnement `OPENLEGI_TOKEN`)
- Conversation multi-tours : l’agent conserve le contexte de la session

## Stack

- Python ≥ 3.12
- `mistralai-agents==1.1.2`
- Modèle : `mistral-large-4`
- Entrypoint : `main:agent`

## Déploiement

Le déploiement est géré (image Docker basée sur `uv`, commande `agents run-worker`). L’interaction utilisateur se fait via **Vibe**.

## Fichiers principaux

| Fichier | Rôle |
|---------|------|
| `main.py` | Agent, instructions et outil `citation_legifrance` |
| `pyproject.toml` | Dépendances et entrypoint Mistral Agents |
| `Dockerfile` | Image de production du worker |
