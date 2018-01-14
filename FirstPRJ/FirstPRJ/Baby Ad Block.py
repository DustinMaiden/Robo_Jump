def solution(A):
    # left bound and right bound problem, i think
    size = len(A)
    y = size
    x = 0

    for x in range(0, size - 1):
        if A[x] < A[x + 1]:
            leftbound = x

    for y in range(size, 0):
        if A[y] < A[y - 1]:
            rightbound = y
        y -= 1

    answer = int(rightbound) - int(leftbound)
    return answer
