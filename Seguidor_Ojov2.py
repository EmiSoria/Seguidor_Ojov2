import cv2
import mediapipe as mp
import pyautogui

# Abrir la webcam
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# Obtener el tamaño de la pantalla
screen_w, screen_h = pyautogui.size()
left_click_active = False

while True:
    _, frame = cam.read()
    # Invertir la webcam en el eje y
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):  # Puntos del ojo derecho
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            # Dibujar círculos verdes en el ojo derecho
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w / frame_w * (x * 1.4)  # Obtener la proporción
                screen_y = screen_h / frame_h * (y * 1.4)
                # Mover el cursor
                pyautogui.moveTo(screen_x, screen_y)

        # Puntos para detectar el parpadeo del ojo izquierdo
        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            # Dibujar círculos amarillos en el ojo izquierdo
            cv2.circle(frame, (x, y), 3, (0, 255, 255))

        # Puntos para detectar el parpadeo del ojo derecho
        right_eye = [landmarks[374], landmarks[386]]
        for landmark in right_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            # Dibujar círculos rojos en el ojo derecho
            cv2.circle(frame, (x, y), 3, (0, 0, 255))

        # Verificar si los puntos del ojo izquierdo están cerca (parpadeo)
        left_blink = abs(left_eye[0].y - left_eye[1].y) < 0.005
        # Verificar si los puntos del ojo derecho están cerca (parpadeo)
        right_blink = abs(right_eye[0].y - right_eye[1].y) < 0.005

        # Ejecutar clics solo si no se están parpadeando ambos ojos al mismo tiempo
        if left_blink and right_blink:
            print("No click (both eyes blinking)")
        elif left_blink:
            if not left_click_active:
                print('Left mouse down')
                pyautogui.mouseDown()  # Mantener clic izquierdo presionado
                left_click_active = True
        else:
            if left_click_active:
                print('Left mouse up')
                pyautogui.mouseUp()  # Soltar clic izquierdo
                left_click_active = False

        if right_blink:
            print('Right click')
            pyautogui.click(button='right')  # Hacer clic derecho
            pyautogui.sleep(1)

    # Mostrar el fotograma en una ventana
    cv2.imshow('Eyes Mouse AI', frame)
    cv2.waitKey(1)
