# intervals are [a..b) where a <= b
# for now they are just tuples

class ITNode:
    def __init__(self, center, intervals):
        self.center = center
        self.intervals = intervals # might be empty or none
        self.left = None
        self.right = None

    def __str__(self):

        if self.intervals is None:
            s = "center = %s, NO INTERVALS" % self.center
        else:
            s = "center = %s, intervals = [%s]" % (
                self.center,
                ','.join([str(x) for x in self.intervals]))
        return s

class ITree:

    def __init__(self):
        self.root = None

    def insert(self, intervals, left_bound, right_bound):
        middle = (left_bound + right_bound) / 2.0

        straddle = []
        left_intervals = []
        right_intervals = []

        for i in intervals:
            if i[1] <= middle:
                left_intervals.append(i)
            elif i[0] > middle:
                right_intervals.append(i)
            else:
                # i[1] > middle and i[0] <= middle
                straddle.append(i)

        left_child = None
        if len(left_intervals) > 0:
            left_child = self.insert(left_intervals, left_bound, middle)

        right_child = None
        if len(right_intervals) > 0:
            right_child = self.insert(right_intervals, middle, right_bound)
        
        if left_child or right_child or straddle:
            node = ITNode(middle, straddle)
            node.left = left_child
            node.right = right_child
            return node

    def construct(self, intervals):
        # find range of entire interval set
        imax = None
        imin = None
        for i in intervals:
            if not imin:
                imin = i[0]
            if not imax:
                imax = i[1]

            if i[0] < imin:
                imin = i[0]

            if i[1] > imax:
                imax = i[1]

        self.root = self.insert(intervals, imin, imax)

    def ptree(self, node, level):
        if not node:
            print "%s%s" % ('    ' * level, "NUTHIN")
            return

        print "%s%s" % ('    ' * level, str(node))
        if not node.left and not node.right:
            return

        self.ptree(node.left, level+1)
        self.ptree(node.right, level+1)

    def dump(self):
        self.ptree(self.root, 0)

    def find_at_node(self, node, findme):
        # check whether findme straddles
        # whether any left endpoint of a straddler is in findme
        # whether any right endpoint of a straddler is in findme
        pass

    def find_interval(self, findme):
        '''
        give me the intervals in this collection that findme touches.
        '''
        return self.find_at_node(self.root, findme)

# merging overlapping intervals
# 
# 1. Sort the intervals based on increasing order of 
#     starting time.
# 2. Push the first interval on to a stack.
# 3. For each interval do the following
#    a. If the current interval does not overlap with the stack 
#        top, push it.
#    b. If the current interval overlaps with stack top and ending
#        time of current interval is more than that of stack top, 
#        update stack top with the ending  time of current interval.
# 4. At the end stack contains the merged intervals. 
