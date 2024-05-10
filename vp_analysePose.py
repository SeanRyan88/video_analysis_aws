# Identify the first repition 
# Is done by identifying when the wrist is first identified above the shoulders
def IdentifyFirstRep(AnalysisArray):
    for x in range(0,len(AnalysisArray)):
        wrist_y = AnalysisArray[x][4][1]
        shoulder_y = AnalysisArray[x][2][1]
        if wrist_y < shoulder_y:
            # Return the frame (image) and the index
            return AnalysisArray[x][0], x
    
# Identify the max height of the reptition
# Is done by identifying when the wrist is at the highest point
def IdentifyMaxofRep(AnalysisArray):
    print("Start IdentifyMaxofRep")
    max_height = float('inf')  
    max_frame = None
    max_index = -1

    # print("Test Now")
    for x in range(0,len(AnalysisArray) - 11, 5): 
        print("Test Begins")
        print("Max Test ", x, " / ", len(AnalysisArray)) 
        # SaveImage(AnalysisArray[x][0], "max Compare 1 " + "wrist_1 x=" + str(x) + ".jpg")
        wrist_1 = AnalysisArray[x][4][1]
        # SaveImage(AnalysisArray[x+5][0], "max Compare 2 " + "wrist_1 x=" + str(x+5) + ".jpg")
        wrist_2 = AnalysisArray[x + 5][4][1]
        print("wrist 1 = ", wrist_1)
        print("wrist 2 = ", wrist_2)

        if wrist_1 < wrist_2:
            print("wrist Test = True")
            max_height = wrist_1
            max_frame = AnalysisArray[x][0]
            max_index = x
            # print(x) 
            return max_frame, x+5
        # else:
            # print("wrist Test = True")
    
    # print("This finished")
    

    return 0, len(AnalysisArray) -1
    

# Identify the max height of the reptition
# Is done by identifying when the wrist is at the highest point
def IdentifyMinofRep(AnalysisArray):
    print("Start IdentifyMinofRep")
    max_height = float('inf')  
    max_frame = None
    max_index = -1

    # print("Test Now")
    for x in range(0,len(AnalysisArray) - 11, 5): 
        print("Test Begins")
        print("Min Test ", x, " / ", len(AnalysisArray)) 
        # SaveImage(AnalysisArray[x][0], "Min Compare 1 " + "wrist_1 x=" + str(x) + ".jpg")
        wrist_1 = AnalysisArray[x][4][1]
        # SaveImage(AnalysisArray[x+5][0], "Min Compare 2 " + "wrist_1 x=" + str(x+5) + ".jpg")
        wrist_2 = AnalysisArray[x + 5][4][1]
        # print("wrist 1 = ", wrist_1)
        # print("wrist 2 = ", wrist_2)

        if wrist_1 > wrist_2: # or wrist_1 < AnalysisArray[x][2][1]: #Shoulder
            print("wrist Test = True")
            max_height = wrist_1
            max_frame = AnalysisArray[x][0]
            max_index = x
            # print(x) 
            return max_frame, x+5
        # else:
            # print("wrist Test = True")
    
    # print("This finished")
    return 0, len(AnalysisArray) -1
    
    



def AnalysePose(video_path):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    AnalysisArray = []

    cap = cv2.VideoCapture(video_path)
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame or end of video.")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                shoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * image.shape[1],
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image.shape[0])
                elbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * image.shape[1],
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * image.shape[0])
                wrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * image.shape[1],
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * image.shape[0])
                
                angle = calculate_angle(shoulder, wrist, elbow)
                # print(image.shape)
                # print("Angle = ", angle)
                # print("Shoulder = ",shoulder )
                # print("Shoulder X = ", landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x)
                # print("Shoulder Y = ", landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)

                # print("Elbow = ",elbow )
                # print("Elbow X = ",landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y )
                # print("Elbow Y = ",elbow )
                # print("Wrist = ",wrist )
                # print("Wrist X = ",landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x )
                # print("Wrist Y = ",landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y )

                cv2.putText(image, str(round(angle, 2)), 
                            [500,500],
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
                
                AnalysisArray.append([image, angle, shoulder, elbow, wrist])

            except Exception as e:
                print(e)
                pass

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

            cv2.imshow('Mediapipe Feed', image)
            # time.sleep(1)  # Wait for 1 second between each frame

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return AnalysisArray



    UpdatedArray = AnalysisArray



