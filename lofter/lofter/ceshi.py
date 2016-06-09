

class Solution1(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """

        for i in range(len(nums)):
            a=target-nums[i]
            if a in nums and i!=nums.index(a):
                return [i,nums.index(a)]

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        return map(sum,zip(l1,l2))
print Solution().addTwoNumbers([3,2,4],[1,2,3])
print zip([3,2,4],[1,2,3])



