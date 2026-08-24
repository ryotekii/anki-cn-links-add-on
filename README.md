# anki-cn-extension

Créer un venv avec python 3.13 (64-bit), puis installer les dépendances :

```bash
pip install -r requirements.txt
```

En dev pour le débug et l'autocomplétion :
```bash
pip install -r requirements-dev.txt
```

Aller dans le dossier addons21 de anki et créer un lien symbolique vers cn-links
```powershell
New-Item -ItemType SymbolicLink `
  -Path "C:\Users\me\AppData\Roaming\Anki2\addons21\cn-links" `
  -Target "C:\Users\me\anki-cn-links-add-on\cn-links"
```