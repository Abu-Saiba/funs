import cv2
import numpy as np
from deepface import DeepFace
#tiredness testing
def get_tiredness_percentage(emotions):
    """
    Calculate tiredness percentage based on facial emotions.
    """
    tiredness_factors = {"sad": 0.5, "angry": 0.4, "neutral": 0.3, "happy": 0.1, "surprise": 0.2, "fear": 0.6, "disgust": 0.3}
    tiredness_score = sum(emotions[emotion] * tiredness_factors.get(emotion, 0) for emotion in emotions)
    return min(100, max(0, tiredness_score * 100))

def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Analyze emotion
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotions = result[0]['emotion']
            tiredness_percentage = get_tiredness_percentage(emotions)
            
            # Display results
            text = f"Tiredness: {tiredness_percentage:.2f}%"
            cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        except Exception as e:
            print("Error in analysis:", e)
        
        cv2.imshow('Tiredness Detector', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
