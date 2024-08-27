# Gesture Mouse Control

**Gesture Mouse Control** é um projeto que combina o rastreamento de mãos usando a biblioteca MediaPipe com controle de cursor e simulação de cliques usando `pyautogui`. O objetivo é transformar gestos da mão em ações do mouse, proporcionando uma maneira intuitiva e inovadora de interagir com o computador. É estritamente necessário ter uma câmera conectada para fazer o uso do programa.

## 📦 Instalação

Para começar a usar o projeto, você precisará instalar algumas bibliotecas Python. Use o seguinte comando para instalar as dependências necessárias:

```bash
pip install opencv-python mediapipe pyautogui
```

## 🛠️ Como usar

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/SEU_USUARIO/gesture-mouse-control.git
    ```
    
2. **Navegue até o diretório do projeto**:
    ```bash
    cd gesture-mouse-control
    ```
    
3. **Execute o script**:
    ```bash
    python hand_tracking_mouse.py
    ```

4. **Interaja com o script**:
    - **Movimentação do Cursor**: Mova o dedo indicador para mover o cursor do mouse na tela.
    - **Clique do Mouse**: Coloque o dedo indicador próximo ao polegar para simular um clique do mouse.

5. **Para encerrar o programa**, pressione a tecla `q` enquanto a janela do vídeo está ativa.

## 🔍 Detalhes do Código

O código Python do projeto realiza as seguintes tarefas:

1. **Importação de Bibliotecas**:
    ```python
    import cv2
    import mediapipe as mp
    import pyautogui as py
    import math
    ```
    - `cv2`: Utilizado para captura e manipulação de vídeo.
    - `mediapipe`: Usado para rastreamento e detecção de pontos-chave na mão.
    - `pyautogui`: Para movimentação do cursor e simulação de cliques do mouse.
    - `math`: Utilizado para cálculos matemáticos, como a distância entre pontos.

2. **Configuração do MediaPipe e PyAutoGUI**:
    ```python
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = py.size()
    ```
    - `mp_hands.Hands`: Configura o modelo para detectar as mãos.
    - `cap = cv2.VideoCapture(0)`: Inicializa a captura de vídeo a partir da webcam.
    - `screen_width, screen_height`: Obtém as dimensões da tela para mapear as coordenadas da câmera para a tela.

3. **Função para Calcular Distância**:
    ```python
    def calculate_distance(p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)
    ```
    - Calcula a distância euclidiana entre dois pontos tridimensionais.

4. **Processamento de Frames e Detecção de Mãos**:
    ```python
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Câmera não encontrada!")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)
        frame_height, frame_width, _ = frame.shape

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]
                distance = calculate_distance(index_finger_tip, thumb_tip)
                x = int(index_finger_tip.x * frame_width)
                y = int(index_finger_tip.y * frame_height)
                screen_x = screen_width * (x / frame_width)
                screen_y = screen_height * (y / frame_height)

                py.moveTo(screen_x, screen_y)
                if distance < 0.05:
                    py.click()

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        cv2.imshow("Hand tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    ```
    - Captura o vídeo da webcam e processa cada frame para detectar as mãos.
    - Calcula a posição do dedo indicador e do polegar para determinar a distância entre eles.
    - Mapeia as coordenadas do dedo indicador para a tela e move o cursor.
    - Se a distância entre o dedo indicador e o polegar for menor que um limite especificado (0.05), simula um clique do mouse.

## 🔧 Contribuição

Contribuições são bem-vindas! Se você encontrar bugs ou tiver sugestões para melhorar o projeto, sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

1. Faça um _fork_ do repositório.
2. Crie uma nova branch (`git checkout -b feature/nova-funcionalidade`).
3. Faça suas alterações e teste-as.
4. Envie suas alterações (`git commit -am 'Adiciona nova funcionalidade'`).
5. Envie a branch para o repositório (`git push origin feature/nova-funcionalidade`).
6. Crie um novo _pull request_.

---

Aproveite para testar e se divertir com o controlador de mouse por gestos!🖱️📸
