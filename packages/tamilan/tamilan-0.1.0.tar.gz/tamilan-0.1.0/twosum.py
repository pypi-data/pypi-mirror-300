def twoSumK( numbers: [int], target: int) -> [int]:
    start,end  = 0, len(numbers)-1  # left, right
    while start<end:
        if numbers[start]+numbers[end]==target: return [start+1,end+1]
        elif numbers[start]+numbers[end]<target: start+=1
        else: end-=1
    return []
def twoSum( numbers: [int], target: int) -> [int]:
    start,end  = 0, len(numbers)-1  # left, right
    while start<end:
        if numbers[start]+numbers[end]==target: return [start,end]
        elif numbers[start]+numbers[end]<target: start+=1
        else: end-=1
    return []
def is_subsequence(s: str, t: str) -> bool:
    t_iter = iter(t)  # Create an iterator for 't'
    return all(char in t_iter for char in s)

def helper():
    print("* => twoSumK( numbers: [int], target: int) -> [int]:  <== 1")
    print("* => twoSum( numbers: [int], target: int) -> [int]:  <== 2")
    print("* => is_subsequence(s: str, t: str) -> bool:  <== 3")
