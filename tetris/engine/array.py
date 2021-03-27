import hashlib

class TwoDArray(object):
    """
    A two-dimensional array data structure.
    """

    def __init__(self, sx, sy, v=0, data=False):
        """
        Setup a 2d array with the size (sx,sy), and the optional
        initial value v.
        """

        self.sx, self.sy = sx, sy
        self.data = [v] * sx * sy
        if data:
            self.data = data

    def __str__(self):
        """
        Return a nice representation of the array.
        """
        s = ""
        for i, data in enumerate(self.data):
            if i % self.sx == 0: s += "\n"
            s += f"{data} "
        return s

    def hash(self):
        """
        Returns a hash of the array. Useful for quickly comparing states without
        needing to output and inspect the full array.
        """
        return hashlib.md5(str(self).encode("ascii")).hexdigest()

    def combine(self, n, x=0, y=0):
        """
        Inserts a given array at a given x,y in the current
        array, and combines the values.
        """

        if type(n) != type(self):
            raise TypeError("Can't combine with non-TwoDArray")

        nx, ny = 0, 0
        for i, data in enumerate(n.data):
            if i % n.sx == 0 and i > 0: ny += 1; nx = 0

            lx = nx + x
            ly = ny + y

            if lx >= self.sx or ly >= self.sy:
                raise IndexError("Can't combine outside bounds of array.")

            if type(data) != type(self.get(lx, ly)):
                raise TypeError("Can't combine different data types in array.")

            self.set(lx, ly, data + self.get(lx, ly))
            nx+=1

    def replace(self, v, nv):
        """
        Replaces a given value in the array with a new value.
        Returns True or False based on whether a replacement occurred.
        """

        replaced = False
        for i, x in enumerate(self.data):
            if x == v:
                replaced = True 
                self.data[i] = nv
        return replaced

    def fill(self, v):
        """
        Fills the array with a given value.
        """
        self.data = [v] * self.sx * self.sy

    def get(self, x, y):
        """
        Returns the value at a given x,y position.
        """
        return self.data[(y * self.sx) + x]

    def set(self, x, y, v):
        """
        Sets the value at a given x,y position.
        """
        self.data[(y * self.sx) + x] = v


a = TwoDArray(10, 10, 1)
b = TwoDArray(8, 8, -1)

a.combine(b, 1, 1)

print(a)

