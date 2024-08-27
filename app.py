import cv2
import mediapipe as mp
import pyautogui as py
import math

mp_hands = mp.solutions.hands #captura o contorno das maos
mp_drawing = mp.solutions.drawing_utils #desenha o contorno das maos

#inicando o mediapipe para capturar as maos
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0) #define a captura de imagem

#obtendo o tamanho da tela
screen_width, screen_height = py.size()

#funcao para calcular a distancia entre dois pontos
def calculate_distance(p1, p2):
    # return math.sqrt((p1.x - p2.x))**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)

#loop para processar os frames da webcam
while True:
    ret, frame = cap.read()
    if not ret: #caso nao consiga capturar o video
        print("Câmera não encontrada!")
        break

    #convertendo a imagem para rgb
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #processando a imagem para detecter as maos
    result = hands.process(frame_rgb)

    #obtendo as dimensoes do frame
    frame_height, frame_width, _ = frame.shape

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            #extraido as coordenadas do ponto 8 (dedo indicador) e ponto 4 (dedao)
            index_finger_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            #calculando a distancia etre o polegar e o indicador
            distance = calculate_distance(index_finger_tip, thumb_tip)

            x = int(index_finger_tip.x * frame_width)
            y = int(index_finger_tip.y * frame_height)

            #invertendo o eixo x e ajustando o eixo y
            screen_x = screen_width - (screen_width / frame_width * x)
            screen_y = screen_height / frame_height * y

            py.moveTo(screen_x, screen_y)

            #se a distancia for menor que certo limite, considera um clique
            if distance < 0.05:
                py.click()

            #desenhando os landmarks da mao
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        #exibindo o frame na tela
        cv2.imshow("Hand tracking", frame)

        #para fechar o programa ao pressionar a tecla "q"
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#liberacao dos recursos
cap.release()
cv2.destroyAllWindows()
        

