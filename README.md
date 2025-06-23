# keyword-detection-tool
This tool detect keyword in real time and trigger any other function for implement into the Commpanion project.

## Installation

```bash
pip install -r requirements.txt
```

### Prérequis pour PyAudio (Windows avec Qualcomm X Plus)
```bash
# Si erreur avec PyAudio, installer via:
pip install pipwin
pipwin install pyaudio
```

## Utilisation rapide

```python
from wakeword_detector import WakeWordDetector

# Créer le détecteur
detector = WakeWordDetector(threshold=0.5)

# Définir une action
def on_wake(word, score):
    print(f"Détecté: {word}")

# Enregistrer l'action
detector.register_callback('alexa', on_wake)

# Démarrer l'écoute
detector.start()
```

## Structure modulaire

```
.
├── wakeword_detector.py   # Module principal
├── test_wakeword.py       # Script de test
├── requirements.txt       # Dépendances
└── models/               # Dossier pour modèles custom (optionnel)
    └── hey_companion.onnx
```

## Test

Lancer le script de test :
```bash
python test_wakeword.py
```

## Personnalisation

### Créer un modèle personnalisé

1. Enregistrer des échantillons audio de votre phrase
2. Utiliser [openWakeWord training](https://github.com/dscripka/openWakeWord#training-new-models)
3. Placer le modèle `.onnx` dans `models/`

### Modifier le seuil de détection

- `threshold=0.3` : Sensible (plus de détections)
- `threshold=0.5` : Équilibré (défaut)
- `threshold=0.7` : Strict (moins de faux positifs)

## Architecture

Le système est conçu de manière modulaire :

- **WakeWordDetector** : Classe principale gérant la détection
- **Callbacks** : Actions déclenchées lors de détections
- **Thread séparé** : Traitement audio non-bloquant
- **Queue** : Communication thread-safe

## Exemple d'intégration

```python
# Intégration avec assistant vocal
def activate_assistant(word, score):
    # 1. Jouer son de confirmation
    play_sound("ding.wav")
    
    # 2. Démarrer STT
    text = speech_to_text()
    
    # 3. Traiter la commande
    process_command(text)

detector.register_callback('hey_companion', activate_assistant)
```

## Performance

- CPU usage : ~5-10% sur Qualcomm X Plus
- RAM : ~100MB
- Latence : <100ms

## Licence

GNUv3