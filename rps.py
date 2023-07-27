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
    
    
clock = 0 
p1_move = p2_move = None
gameText = ""
success = True
P1score = 0
P2score = 0

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
        
        
        if 0 <= clock < 20:
            success = True
            gameText= "Ready?"
            
        elif clock < 30:
            gameText="rock, ..."
        elif clock < 40:
            gameText="paper, ..."
        elif clock < 50:
            gameText="scissors, ..."
        elif clock < 60:
            gameText="SHOOT!"
        elif clock == 60:
            hls = results.multi_hand_landmarks 
            if hls and len(hls) == 2:
                p1_move = getHandMove(hls[0])
                p2_move = getHandMove(hls[1])
            else:
                success = False
        
        
        elif clock < 100:
            if success:
                gameText = f"Played 1 played {p1_move}. Player 2 played {p2_move}."
                if p1_move == p2_move: gameText = f"{gameText} Tie!"
                elif (p1_move == "paper" and p2_move == "rock"):
                    gameText = f"{gameText} Player 1 wins!"
                elif (p1_move == "scissors" and p2_move == "paper"):
                    gameText = f"{gameText} Player 1 wins!"
                elif (p1_move == "rock" and p2_move == "scissiors"):
                    gameText = f"{gameText} Player 1 wins!"
                else:
                    gameText= f"{gameText} Player 2 wins!"
            else:
                gameText = "Didn't play"
            
        
        cv.putText(image, f"Clock: {clock}", (50,50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv.LINE_AA)
        cv.putText(image, gameText, (50,80), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv.LINE_AA)
        clock = (clock + 1) % 100
        
        cv.imshow('image', image)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
        
vid.release()
cv.destroyAllWindows()
    


