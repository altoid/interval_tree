# intervals are [a..b) where a <= b
# for now they are just tuples


class ITNode:
    def __init__(self, center, intervals):
        self.center = center
        self.intervals = intervals  # might be empty or none
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
    # note:  to construct the tree you have to have all of your intervals available up front.  if you add or remove
    # intervals you have to rebalance the tree.

    def __init__(self):
        self.root = None

        # this consists of tuples that look like this:
        #
        # (x (y z))
        #
        # (y z) is an interval and x is either y or z.  we use this to sort all the x coordinates,
        # and with each coordinate we maintain a reference to the interval it's in.

        self.sorted_coordinates = []


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
        if left_intervals:
            left_child = self.insert(left_intervals, left_bound, middle)

        right_child = None
        if right_intervals:
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

            self.sorted_coordinates.append((i[0], i))
            self.sorted_coordinates.append((i[1], i))

        self.root = self.insert(intervals, imin, imax)
        self.sorted_coordinates = sorted(self.sorted_coordinates, key=lambda x: x[0])

    def ptree(self, node, level):
        if not node:
            print "%s%s" % ('    ' * level, "NUTHIN")
            return

        print "%s%s" % ('    ' * level, str(node))
        if not node.left and not node.right:
            return

        self.ptree(node.left, level + 1)
        self.ptree(node.right, level + 1)

    def dump(self):
        self.ptree(self.root, 0)

    def find_intervals_for_point_helper(self, x, node):
        if not node:
            return

        for i in node.intervals:
            if i[0] <= x < i[1]:
                yield i

        if x <= node.center:
            for i in self.find_intervals_for_point_helper(x, node.left):
                yield i
        elif x > node.center:
            for i in self.find_intervals_for_point_helper(x, node.right):
                yield i

    def find_intervals_for_point(self, x):
        for i in self.find_intervals_for_point_helper(x, self.root):
            yield i

    def find_leftmost_coordinate(self, x, left, right):
        if right < left:
            return None

        if right == left:
            return self.sorted_coordinates[left][0]

        m = (right + left) / 2
        if x <= self.sorted_coordinates[m][0]:
            return self.find_leftmost_coordinate(x, left, m)
        return self.find_leftmost_coordinate(x, m + 1, right)

    def find_intervals_for_interval(self, r):
        # find the leftmost coordinate that is >= r[0]

        i = self.find_leftmost_coordinate(r[0], 0, len(self.sorted_coordinates) - 1)
        if not i:
            return

        # coords[i] will be <= r[0].  we want the leftmost coord that is <= r[0].  so iterate.
        # if any coord is == r[0], wind back to the left to find them all.
        while i >= 0 and self.sorted_coordinates[i][0] == r[0]:
            i -= 1

        while i < len(self.sorted_coordinates):
            if self.sorted_coordinates[i][0] >= r[0]:
                break
            i += 1

        if i > len(self.sorted_coordinates):
            return

        result = set()
        while i < len(self.sorted_coordinates):

            test_interval = self.sorted_coordinates[i][1]

            if test_interval[0] <= r[0] < test_interval[1]:
                result.add(test_interval)

            if test_interval[0] < r[1] < test_interval[1]:
                result.add(test_interval)

            i += 1

        # now look for any intervals that enclose r.
        for i in self.find_intervals_for_point((r[0] + r[1]) / 2.0):
            result.add(i)

        for e in result:
            yield e



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
