import cv2 as cv 
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y < landmarks[i+3].y for i in range (9,20,4)]):
        return "rock"
    elif landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks[20].y:
        return "scissors"
    else:
        return "paper"

vid = cv.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    while True:
        ret, image = vid.read()
        if not ret or image is None:
            break
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        
        results = hands.process(image)
        
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
                
        image = cv.flip(image, 1)
        
        
        cv.imshow('image', image)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
        
vid.release()
cv.destroyAllWindows()
    


