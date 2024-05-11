def textResults(results):
    # Results in format results[found, top = x, bottom = x, speed = x]

    if results[0] == 0:
        result = "Unable to identify... \n \n Try to do ..."
    else:
        total = results[1] + results[2] + results[3]
        if total == 1:
            result = "Score: 50/100 \n \n Good job! You're on your way to improve your shoulder mobility."
        elif total == 2:
            result = "Score: 75/100 \n \n Great job! You're showing strong adherence to the recommended shoulder exercises"
        else:
            result = "Score: 100/100 \n \n You're a Natural! You're showing strong adherence to the recommended shoulder exercises"

        #  \n \n You’re currently completing the exercise too quickly! Consider slowing down and counting 3 seconds as you go up, and 3 seconds as you go down."
        
        
        result += "\n To improve try to ..."
        if results[1] == 1:
            result += "\n- 11Keep your... "
        elif results[1] == 2:
            result += "\n- 12Keep your... "
        elif results[1] == 3:
            result += "\n- 13Keep your... "

        if results[2] == 1:
            result += "\n- 21Keep your... "
        elif results[2] == 2:
            result += "\n- 22Keep your... "
        elif results[2] == 3:
            result += "\n- 23Keep your... "

        if results[3] == 1:
            result += "\n- 31Keep your... "
        elif results[3] == 2:
            result += "\n- 32Keep your... "
        elif results[3] == 3:
            result += "\n- 33Keep your... "



        
    return result
        
