nums = [1,2,3,4]
is_bool = False
for i in range(len(nums)-1):
    for j in range(i+1,len(nums)):
        if nums[i] == nums[j]:
            is_bool = True

print(is_bool)