import cv2
from wbet_system.core.eye_tracker import EyeTracker
from wbet_system.config.settings import WEBCAM_INDEX

CALIBRATION_POINTS = ["center", "left", "right", "up", "down"]

def run_calibration():
    tracker = EyeTracker()
    cap = cv2.VideoCapture(WEBCAM_INDEX)

    if not cap.isOpened():
        print("Erro ao abrir a webcam.")
        return

    calibration_data = {}

    for point in CALIBRATION_POINTS:
        print(f"\nOlhe para: {point.upper()} e pressione [ESPAÇO] quando pronto.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame, gaze = tracker.process_frame(frame)
            cv2.putText(processed_frame, f"Olhe para {point.upper()} e pressione ESPACO",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imshow("Calibration", processed_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # espaço
                # Coletar média de 30 frames
                dx_vals, dy_vals = [], []
                for _ in range(30):
                    ret, frame = cap.read()
                    if not ret:
                        continue
                    _, _ = tracker.process_frame(frame)
                    # O vetor médio do último cálculo está em tracker.gaze_direction?
                    # Melhor salvar avg_gaze_vector dentro de tracker também.
                    dx, dy = tracker.last_gaze_vector
                    dx_vals.append(dx)
                    dy_vals.append(dy)

                calibration_data[point] = (np.mean(dx_vals), np.mean(dy_vals))
                print(f"{point} registrado: {calibration_data[point]}")
                break

            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

    cap.release()
    cv2.destroyAllWindows()
    print("Calibração finalizada:", calibration_data)
    return calibration_data


if __name__ == "__main__":
    data = run_calibration()
