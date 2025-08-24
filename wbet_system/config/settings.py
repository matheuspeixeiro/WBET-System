# wbet_system/config/settings.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

SHAPE_PREDICTOR_PATH = os.path.join(MODELS_DIR, "shape_predictor_68_face_landmarks.dat")

# Webcam
WEBCAM_INDEX = 0 # 0 para a câmera padrão, altere se tiver múltiplas

# Limiares de detecção (ajustar posteriormente via calibração)
EYE_ASPECT_RATIO_THRESHOLD = 0.25 # Exemplo para piscar
GAZE_THRESHOLD_X = 0.05 # Ajuste conforme necessário
GAZE_THRESHOLD_Y = 0.05 # Ajuste conforme necessário

# Dimensões da janela de depuração (se for exibir o feed da webcam)
DEBUG_WINDOW_WIDTH = 640
DEBUG_WINDOW_HEIGHT = 480