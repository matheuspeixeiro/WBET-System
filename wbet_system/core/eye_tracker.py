import cv2
import dlib
import numpy as np
from wbet_system.config.settings import (
    SHAPE_PREDICTOR_PATH,
    WEBCAM_INDEX,
    DEBUG_WINDOW_WIDTH,
    DEBUG_WINDOW_HEIGHT
)

CALIBRATION_POINTS = ["center", "left", "right", "up", "down"]

class EyeTracker:
    def __init__(self):
        print(f"Loading shape predictor from: {SHAPE_PREDICTOR_PATH}")
        try:
            self.detector = dlib.get_frontal_face_detector()
            self.predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
        except Exception as e:
            print(f"Error loading dlib model: {e}")
            exit()

        self.l_start, self.l_end = 42, 48
        self.r_start, self.r_end = 36, 42

        self.gaze_calibration_ranges = {}
        self.gaze_sensitivity_x = 0.15
        self.gaze_sensitivity_y = 0.15

        self.last_gaze_vector = (0, 0)
        self.gaze_direction = "N/A"

    def _get_eye_landmarks(self, landmarks, eye_points):
        return np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in eye_points])

    def _get_gaze_vector(self, eye_landmarks, gray_frame):
        min_x, min_y = np.min(eye_landmarks, axis=0)
        max_x, max_y = np.max(eye_landmarks, axis=0)

        # recorte do olho
        eye_img = gray_frame[min_y:max_y, min_x:max_x]
        if eye_img.size == 0:
            return (0, 0)

        # equaliza e aplica threshold adaptativo
        eye_img = cv2.equalizeHist(eye_img)
        _, thresh = cv2.threshold(eye_img, 50, 255, cv2.THRESH_BINARY_INV)

        # centro da pupila via momentos
        moments = cv2.moments(thresh)
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
        else:
            cx, cy = eye_img.shape[1] // 2, eye_img.shape[0] // 2

        # normaliza deslocamento em relação ao centro do ROI
        dx = (cx - eye_img.shape[1] / 2) / (eye_img.shape[1] / 2)
        dy = (cy - eye_img.shape[0] / 2) / (eye_img.shape[0] / 2)

        return (dx, dy)

    def _classify_gaze(self, gaze_vector):
        dx, dy = gaze_vector
        dx_threshold = self.gaze_sensitivity_x
        dy_threshold = self.gaze_sensitivity_y

        if dx > dx_threshold and dy < -dy_threshold: return "up_right"
        if dx > dx_threshold and dy > dy_threshold: return "down_right"
        if dx < -dx_threshold and dy < -dy_threshold: return "up_left"
        if dx < -dx_threshold and dy > dy_threshold: return "down_left"

        if abs(dx) <= dx_threshold and abs(dy) <= dy_threshold: return "center"

        if dx > dx_threshold: return "right"
        if dx < -dx_threshold: return "left"
        if dy < -dy_threshold: return "up"
        if dy > dy_threshold: return "down"

        return "center"

    def apply_calibration(self, calibration_data):
        self.gaze_calibration_ranges = calibration_data

        if "left" in calibration_data and "right" in calibration_data:
            left_dx, _ = calibration_data["left"]
            right_dx, _ = calibration_data["right"]
            self.gaze_sensitivity_x = (abs(left_dx) + abs(right_dx)) / 3

        if "up" in calibration_data and "down" in calibration_data:
            _, up_dy = calibration_data["up"]
            _, down_dy = calibration_data["down"]
            self.gaze_sensitivity_y = (abs(up_dy) + abs(down_dy)) / 3

        print(f"Calibração aplicada: thresholds -> X={self.gaze_sensitivity_x:.3f}, Y={self.gaze_sensitivity_y:.3f}")

    def process_frame(self, frame):
        frame_resized = cv2.resize(frame, (DEBUG_WINDOW_WIDTH, DEBUG_WINDOW_HEIGHT))
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray, 1)

        self.gaze_direction = "N/A"

        for face in faces:
            landmarks = self.predictor(gray, face)
            left_eye_landmarks = self._get_eye_landmarks(landmarks, range(self.l_start, self.l_end))
            right_eye_landmarks = self._get_eye_landmarks(landmarks, range(self.r_start, self.r_end))

            gaze_vector_left = self._get_gaze_vector(left_eye_landmarks, gray)
            gaze_vector_right = self._get_gaze_vector(right_eye_landmarks, gray)

            avg_gaze_vector = ((gaze_vector_left[0] + gaze_vector_right[0]) / 2,
                               (gaze_vector_left[1] + gaze_vector_right[1]) / 2)

            self.last_gaze_vector = avg_gaze_vector
            self.gaze_direction = self._classify_gaze(avg_gaze_vector)

            cv2.putText(frame_resized, f"Olhar: {self.gaze_direction}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame_resized, f"Vetor: ({avg_gaze_vector[0]:.2f}, {avg_gaze_vector[1]:.2f})",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            break

        return frame_resized, self.gaze_direction


def run_calibration(tracker, cap):
    calibration_data = {}
    for point in CALIBRATION_POINTS:
        print(f"\nOlhe para: {point.upper()} e pressione [ESPAÇO] quando pronto.")
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            processed_frame, _ = tracker.process_frame(frame)
            cv2.putText(processed_frame, f"Olhe para {point.upper()} e pressione ESPACO",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imshow("Calibration", processed_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # espaço
                dx_vals, dy_vals = [], []
                for _ in range(30):
                    ret, frame = cap.read()
                    if not ret:
                        continue
                    tracker.process_frame(frame)
                    dx, dy = tracker.last_gaze_vector
                    dx_vals.append(dx)
                    dy_vals.append(dy)

                calibration_data[point] = (np.mean(dx_vals), np.mean(dy_vals))
                print(f"{point} registrado: {calibration_data[point]}")
                break

            if key == ord('q'):
                return None

    cv2.destroyWindow("Calibration")
    return calibration_data


if __name__ == "__main__":
    tracker = EyeTracker()
    cap = cv2.VideoCapture(WEBCAM_INDEX)

    if not cap.isOpened():
        print("Erro ao abrir a webcam.")
        exit()

    # === ETAPA 1: Calibração ===
    calibration = run_calibration(tracker, cap)
    if calibration:
        tracker.apply_calibration(calibration)

    # === ETAPA 2: Rastreamento Normal ===
    print("Calibração concluída! Agora rastreando o olhar. Pressione 'q' para sair.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, gaze = tracker.process_frame(frame)
        cv2.imshow("Eye Tracking - Gaze-Based-Computer-Control", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
