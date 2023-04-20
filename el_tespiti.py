import cv2
import mediapipe as mp
import numpy as  np

    
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


finger_x =np.arange(0.1,0.9,0.00140625)
finger_x = finger_x.tolist()
screen_x = np.arange(1,640,1)                  # el tespitinden gelen kordinat bilgisi 0 - 9 arasında bir değere dönüştürülmesi sağlandı
                                               # böylece istenilen 2 parmak eklemi arasındaki mesafe ölçülmesi ve çizgi çizilmesi sağlandı
finger_y =np.arange(0.1,0.9,0.001875)
finger_y = finger_y.tolist()
screen_y = np.arange(1,480,1)

x1 = [1]
y1 = [1]
x2 = [1]
y2 = [1]

a = [0.1] # y1
b = [0.1] # y2

c = [0.1] # x1
d = [0.1] # x2

# converted item

x11 = [1]
y11 = [1]
x22 = [1]
y22 = [1]


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    
    
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      #print("sonuç")
      for hand_landmarks in results.multi_hand_landmarks:
        #print(results.multi_hand_landmarks[0].landmark[20])
        try:
          x1[0] = (results.multi_hand_landmarks[0].landmark[4].x)
          y1[0] = (results.multi_hand_landmarks[0].landmark[4].y)

          x2[0] = (results.multi_hand_landmarks[0].landmark[8].x)
          y2[0] = (results.multi_hand_landmarks[0].landmark[8].y)

          y16 = (results.multi_hand_landmarks[0].landmark[16].y)
          y0 = (results.multi_hand_landmarks[0].landmark[0].y)
        except:
          x1[0] = 5
          y1[0] = 5

          x2[0] = 20
          y2[0] = 20
          print("hata")
        #print(results.multi_hand_landmarks[0].landmark[8].x)
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
      

    
        # y1
        for i in finger_y:
          if y1[0] >= i:
            a.clear()
            a.append(i)
            
          else:
            break
        index = finger_y.index(a[0])
        y11.clear()
        y11.append(screen_y[index])

        #y2
        for i in finger_y:
          if y2[0] >= i:
            b.clear()
            b.append(i)
            
          else:
            break
        index = finger_y.index(b[0])
        
        y22.clear()
        y22.append(screen_y[index])

        #x1
        for i in finger_y:
          if x1[0] >= i:
            c.clear()
            c.append(i)
            
          else:
            break
        index = finger_y.index(c[0])
        x11.clear()
        x11.append(screen_y[index])

        #x2
        for i in finger_y:
          if x2[0] >= i:
            d.clear()
            d.append(i)
            
          else:
            break
        index = finger_y.index(d[0])
        x22.clear()
        x22.append(screen_y[index])       
        
    else:
        x11 = [1]
        y11 = [1]
        x22 = [1]
        y22 = [1]
        pass  
    

    image = cv2.line(image, (x11[0]+100 ,y11[0]), (x22[0]+100 ,y22[0]+50), (0, 0, 255), thickness=2)

    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    cv2.resizeWindow("MediaPipe Hands", 640, 480)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
