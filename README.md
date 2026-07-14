# NearYa Express

## Fichiers
- `app.py` — application Streamlit (version corrigée)
- `.streamlit/config.toml` — thème (couleurs, police)
- `style.css` — feuille de style de secours (le style principal est déjà injecté dans app.py)
- `nearya_express.db` — base SQLite valide, régénérée avec les 3 comptes par défaut

## Comptes par défaut
| Utilisateur   | Mot de passe | Rôle       |
|---------------|--------------|------------|
| admin1        | admin123     | Admin      |
| commercial1   | comm123      | Commercial |
| commercial2   | comm456      | Commercial |

## Lancer l'app
```bash
pip install streamlit pandas
streamlit run app.py
```
Place les 4 fichiers (`app.py`, `.streamlit/config.toml`, `style.css`, `nearya_express.db`)
dans le même dossier avant de lancer.

## Ce qui a été corrigé
1. `nearya_express.db` contenait du texte au lieu d'une vraie base SQLite → régénérée proprement.
2. Ajout de `WAL mode` + `timeout` sur toutes les connexions → évite les erreurs
   "database is locked" quand plusieurs commerciaux utilisent l'app en même temps.
3. Toutes les opérations base de données sont maintenant dans des `try/except` →
   l'app affiche un message clair au lieu de planter.
4. Détection automatique : si `nearya_express.db` redevient corrompu un jour,
   l'app le sauvegarde (`.corrupted_....bak`) et recrée une base saine automatiquement.
