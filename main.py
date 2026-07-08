import cv2
import pyautogui
import time

try:
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
except AttributeError:
    from mediapipe.python.solutions import hands as mp_hands
    from mediapipe.python.solutions import drawing_utils as mp_draw

pyautogui.FAILSAFE = True

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

def contar_dedos(hand_landmarks):
    dedos = []

    # Polegar
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        dedos.append(1)
    else:
        dedos.append(0)

    # Outros 4 dedos
    pontas = [8, 12, 16, 20]
    bases = [6, 10, 14, 18]

    for ponta, base in zip(pontas, bases):
        if hand_landmarks.landmark[ponta].y < hand_landmarks.landmark[base].y:
            dedos.append(1)
        else:
            dedos.append(0)

    return dedos.count(1)

cap = cv2.VideoCapture(0)

# --- CONFIGURAÇÕES DE TEMPO ---
tempo_confirmacao = 1.0  # Tempo (em segundos) que você precisa MANTER o gesto parado
tempo_espera = 2.0       # Cooldown após o disparo de um comando

# --- VARIÁVEIS DE CONTROLE ---
gesto_estavel = None
tempo_inicio_gesto = 0
ultimo_comando = 0

print("=== Controle por Gestos (Com Confirmação) Ativado ===")
print("\n")
print("5 Dedos (Mão aberta): Play / Pause")
print("1 Dedo  (Indicador) : Avançar 10s")
print("2 Dedos (Paz e amor): Voltar 10s")
print("3 Dedos             : Próximo Vídeo")
print("Pressione 'q' na janela da câmera para encerrar.")
print("Segure o gesto firme por 1.0s para confirmar a ação.")
print("\n")

while cap.isOpened():
    sucesso, frame = cap.read()
    if not sucesso:
        continue

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(frame_rgb)

    tempo_atual = time.time()
    texto_status = "Aguardando gesto..."

    if resultado.multi_hand_landmarks:
        for hand_landmarks in resultado.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            total_dedos = contar_dedos(hand_landmarks)

            if tempo_atual - ultimo_comando > tempo_espera:

                if total_dedos != gesto_estavel:
                    gesto_estavel = total_dedos
                    tempo_inicio_gesto = tempo_atual
                    texto_status = f"Estabilizando ({total_dedos} dedos)..."

                else:
                    tempo_segurado = tempo_atual - tempo_inicio_gesto

                    if tempo_segurado >= tempo_confirmacao:

                        if total_dedos == 5:
                            pyautogui.press('k')
                            texto_status = "CONFIRMADO: Play / Pause"

                        elif total_dedos == 1:
                            pyautogui.press('l')
                            texto_status = "CONFIRMADO: Avançar 10s"

                        elif total_dedos == 2:
                            pyautogui.press('j')
                            texto_status = "CONFIRMADO: Voltar 10s"

                        elif total_dedos == 3:
                            pyautogui.hotkey('shift', 'n')
                            texto_status = "CONFIRMADO: Proximo Video"

                        ultimo_comando = tempo_atual
                        gesto_estavel = None
                    else:
                        progresso = int((tempo_segurado / tempo_confirmacao) * 100)
                        texto_status = f"Confirmando ({total_dedos} dedos): {progresso}%"
    else:
        gesto_estavel = None

    cv2.putText(frame, texto_status, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imshow('Controle por Gestos - YouTube', frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()