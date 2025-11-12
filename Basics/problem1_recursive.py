def solution(digits = int, change = int):
    if digits == 2 and change == 2:
        answer = 10
    elif change == 1:
        answer = 10 ** digits

    else:
        answer = solution(digits - 1, change) + solution(digits - 1, change - 1)



    return answer

print (solution(6, 2))

# this is not the real answer btw.