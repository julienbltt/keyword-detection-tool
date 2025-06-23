#!/usr/bin/env python3
"""
Script de test pour le détecteur de mot de réveil.
Démonstration de l'architecture modulaire.
"""

import logging
import time
import os
from datetime import datetime

import openwakeword.utils
from wakeword_detector import WakeWordDetector
import openwakeword

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Actions modulaires à déclencher
class WakeWordActions:
    """Classe contenant les actions à exécuter lors de la détection."""
    
    @staticmethod
    def on_hey_companion(wakeword: str, score: float):
        """Action déclenchée pour 'Hey Companion'."""
        print(f"\n🎯 DÉTECTION: {wakeword} (confiance: {score:.2%})")
        print(f"⏰ Heure: {datetime.now().strftime('%H:%M:%S')}")
        
        # Exemple d'actions possibles :
        print("🔊 Assistant activé ! Que puis-je faire pour vous ?")
        
        # Ici, vous pourriez :
        # - Déclencher l'écoute STT
        # - Allumer une LED
        # - Jouer un son de confirmation
        # - Activer d'autres modules
        
        # Simulation d'une action
        print("💡 Exécution de l'action...")
        time.sleep(1)
        print("✅ Action terminée\n")
    
    @staticmethod
    def on_alexa(wakeword: str, score: float):
        """Action pour un autre mot de réveil (exemple)."""
        print(f"\n📢 Autre mot détecté: {wakeword} ({score:.2%})")
        print("❌ Ce n'est pas le bon mot de réveil\n")

def test_custom_model():
    """Test avec un modèle personnalisé (si disponible)."""
    custom_model_path = "models/hey_companion.onnx"
    
    if os.path.exists(custom_model_path):
        logger.info("Utilisation du modèle personnalisé")
        return [custom_model_path]
    else:
        logger.warning("Modèle personnalisé non trouvé, utilisation du modèle par défaut")
        return ['alexa']  # Modèle par défaut d'openWakeWord

def main():
    """Fonction principale de test."""
    print("🔍 Initialisation du test du détecteur de mot de réveil")
    # Vérifier si le répertoire "resources/models" existe
    if not os.path.exists("resources/models"):
        print("Download et installation de openWakeWord")
        # One-time download of all pre-trained models (or only select models)
        openwakeword.utils.download_models()
        print("✅ openWakeWord installé avec succès\n")

    print("🚀 Démarrage du test du détecteur de mot de réveil")
    print("=" * 50)
    
    # Configuration des modèles
    models = test_custom_model()
    
    # Création du détecteur avec configuration personnalisée
    detector = WakeWordDetector(
        wakeword_models=models.copy(),
        threshold=0.5,  # Ajustez selon vos besoins (0.3 = sensible, 0.7 = strict)
        chunk_size=1280,
        sample_rate=16000,
        logger=logger
    )
    
    # Enregistrement des callbacks modulaires
    actions = WakeWordActions()
    
    logger.info(f"Modèles de mot de réveil chargés: {models}")
    # Associer chaque mot de réveil à une action
    if 'alexa' in models:
        logger.info("Enregistrement du callback pour 'alexa'")
        detector.register_callback('alexa', actions.on_hey_companion)
    
    # Si vous avez un modèle personnalisé
    if 'hey_companion' in models:
        detector.register_callback('hey_companion', actions.on_hey_companion)
    
    # Démarrage de l'écoute
    print("\n🎤 Écoute active...")
    print("💬 Dites 'Hey Companion' (ou le mot configuré) pour déclencher une action")
    print("⌨️  Appuyez sur Ctrl+C pour arrêter\n")
    
    try:
        # Utilisation avec context manager
        with detector:
            # Boucle principale
            while True:
                time.sleep(0.1)
                
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
    finally:
        print("👋 Arrêt du test")

if __name__ == "__main__":
    main()