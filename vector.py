from misc import Failure

#Class implementing a fixed-length vector
class Vector(object):
    #Constructor for a vector. Size can either describe the size of the
    #vector object, or the elements you wish to see in the Vector.
    def __init__(self,size):
        if isinstance(size, list):
            self.vec = size[:]
        elif isinstance(size, int) or isinstance(size, long):
            if int(size) < 0:
                raise ValueError("Vector length argument is negative")
            else:
                self.vec = int(size) * [0.0]
        else:
            raise TypeError("Could not use as list or length")

    #Returns a string concatinating the type of the Vector
    #with the string representation of the object's internal list
    def __repr__(self):
        res = "Vector(" + repr(self.vec) + ")"
        return res

    #Returns the length of the calling object's internal list
    def __len__(self):
        return len(self.vec)

    #Uses the yield call to obtain the next value in a Vector object's
    #internal list. Overrides the __iter__ function to extend functionality
    #to Vectors
    def __iter__(self):
        for i in self.vec:
            yield i

    #Defines how python should understand Vector Addition
    def __add__(self,other):
        t = []
        #If the other is a vector, we must specify its internal list
        if type(other).__name__ == "Vector":
            for m in range(0, len(self.vec)):
                t.append(self.vec[m] + other.vec[m])
        #If other is some other iterable object, we specify behavior also
        else:
            for m in range(0, len(self.vec)):
                t.append(self.vec[m] + other[m])
        return Vector(t)

    #If the caller is not a Vector, but a vector is still being added,
    #We swap "other" and "self" and add as specified in "__add__"
    def __radd__(self,other):
        t = []
        if type(other).__name__ == "Vector":
            for m in range(0, len(self.vec)):
                t.append(self.vec[m] + other.vec[m])
        else:
            for m in range(0, len(self.vec)):
                t.append(self.vec[m] + other[m])
        return Vector(t)

    #How to perform incremented addition, we insure that information about
    #the caller's previous value isn't lost when returning the new vector
    def __iadd__(self,other):
        if type(other).__name__ == "Vector":
            for m in range(0, len(self.vec)):
                self.vec[m] += other.vec[m]
        else:
            for m in range(0, len(self.vec)):
                self.vec[m] += other[m]
        return self

    #This function returns the key'th item in a vector object's internal
    #list. Throws an exception if the key is out of bounds, and accomodates
    #for negative output as well.
    def __getitem__(self,key):
        if abs(key) >= len(self):
            raise IndexError("Index out of bounds")
        if key < 0:
            key = len(self) + key
        return self.vec[key]

    #This function takes the key'th item in a vector object's internal
    #list and sets it equal to the value argument. If the key is out of
    #bounds, raises the appropriate exception
    def __setitem__(self,key,value):
        if key >= len(self):
            raise IndexError("Index out of bounds")
        if key < 0:
            key = len(self) + key
        self.vec[key] = value

    #Describes how to check for equality between vector objects.
    def __eq__(self,other):
        #If both arguments are vectors, check their internal lists
        if type(other).__name__ == "Vector":
            return self.vec == other.vec
        #Different objects are never the same
        else:
            return False

    #Describes how to check for inequality operating off of the assumption
    #that objects that are equal are never inequal at the same time, and
    #vice verse
    def __ne__(self,other):
        return not self == other

    #Describes how to check for a "greater than" relationship between two
    #vectors.
    def __gt__(self,other):
        if type(other).__name__ == "Vector":
            #We define two temporary lists
            oL = other.vec
            sL = self.vec
            while sL != []:
                #If their largest values match, remove them from both
                if max(sL) > max(oL): return True
                else:
                    sL.remove(max(sL))
                    oL.remove(max(oL))
        #At this point either self <= other, or other is not a vector
        return False

    #Describes how to check for a "greather than or equal to" relationship
    #between two vectors
    def __ge__(self,other):
        if type(other).__name__ == "Vector":
            #Define two temporary lists representing self.vec and other.vec
            oL = other.vec
            sL = self.vec
            eq = True
            while sL != []:
                if max(sL) > max(oL): return True
                else:
                    #If their max values are not equal, then other/self
                    #will never be equal
                    if max(sL) != max(oL): eq = False
                    sL.remove(max(sL))
                    oL.remove(max(oL))
            return eq
        return False

    #Describes how to check for a "less than" relationship between two
    #vectors.
    def __lt__(self,other):
        if type(other).__name__ == "Vector":
            oL = other.vec
            sL = self.vec
            while sL != []:
                #We consider the largest value of each list, its the quickest
                #way to determine which list is "larger"
                if max(sL) < max(oL): return True
                else:
                    sL.remove(max(sL))
                    oL.remove(max(oL))
        return False

    #Describes how to check for a "less than or equal to" relationship
    #between two vectors.
    def __le__(self,other):
        if type(other).__name__ == "Vector":
            oL = other.vec
            sL = self.vec
            eq = True
            while sL != []:
                #First we try to figure out which list is "greater" than
                #the other
                if max(sL) < max(oL): return True
                else:
                    #If their max values are not equal, then other/self
                    #will never be equal
                    if max(sL) != max(oL): eq = False
                    sL.remove(max(sL))
                    oL.remove(max(oL))
            return eq
        return False

    #Takes at least one vector and a list-like object, and returns the
    #sum of multiplying their respective elements together. We maintain an
    #accumulator to hold the result of our product addition, fold-style.
    def dot(self,other):
        res = 0
        #If other is a vector, multiply the elements in their internal lists
        if type(other).__name__ == "Vector":
            for m in range(0, len(self.vec)):
                res += self.vec[m] * other.vec[m]
        else:
            #If other is somelist-like object, we multiply it with self's
            #corresponding internal list element
            for m in range(0, len(self.vec)):
                res += self.vec[m] * other[m]
        return res

