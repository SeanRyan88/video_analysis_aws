def process_video(videoPath):
    print("Run Process process_video")
    # AnalysisArray[image, angle, shoulder[x,y], elbow[x,y], wrist[x,y]]
    # Wrist Y = AnalysisArray[4[1]
    # print(AnalysisArray)
    ResultsArray = []

    # Identify all start, max and end frames of each repition.

    # Identify first repetition (wrist is above shoulder)
    SaveFrame, CheckPoint = vp_analysePose.IdentifyFirstRep(AnalysisArray)

    if SaveFrame is None:
        print("FAIL")
        # Return error message "Please ensure you complete reps, we were unable to identify you putting your arms above your head"
    else:
        # Save the starting frame if it's not None
        SaveImage(SaveFrame, filename="first_frame.jpg")
        ResultsArray.append(SaveFrame)

    if ResultsArray == "":
        print("FAIL") #XXXXX
        #### Return error message "Please ensure you complete reps, we were unable to identify you putting your arms above your head"

    print("Begin Analysis")
    print(AnalyseRepetitions(AnalysisArray[CheckPoint:len(AnalysisArray) -1 ]))


    # Return GIF
