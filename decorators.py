from misc import Failure

class profiled(object):
    def __init__(self,f):
        self.__count=0
        self.__f=f
        self.__name__=f.__name__
    def __call__(self,*args,**dargs):
        self.__count+=1
        return self.__f(*args,**dargs)
    def count(self):
        return self.__count
    def reset(self):
        self.__count=0

#Okay look this decorator is pretty sick. Have you been suuuper feelin urself
#after writing a beautiful recursive function, only to have it return
#absolute garbage when you run it? Every wonder why your code is garbage?
#Yes, you've failed, and yes, you have no one to blame but yourself...but
#now you can learn the exact manner in which you ruined everything by
#having your mediocre-grade function print out every step of its recursive
#process! Yes, this is absolutely legal!
class traced(object):
    #To keep track of nesting levels across function calls, we declare
    #the nest_count variable to be global
    nest_count = 0
    def __init__(self,f):
        #Preserve some info about our function using the traced decorator
        self.__f = f
        self.__name__ = f.__name__
    #So here's where the magic happens. The approach to tracing the function
    #is to understand its state before its next recursive call and after it.
    def __call__(self,*args,**dargs):
        #So we first make the indentation to reflect the nesting level,
        #then determine the arguments the function is using at this stage
        #of its call
        pipes = "| " * traced.nest_count
        argsL = ", ".join([repr(x) for x in args])
        keys = ", ".join([key + "=" + repr(val) for key,val in dargs.items()])
        print pipes + ",- " + self.__name__ + "(" + argsL + keys + ")"

        #We have all the info about the function at this moment, so prepare
        #for our next request for function info
        traced.nest_count += 1
        #Now we make our function call. Sometimes your function is especially
        #poorly-written and will throw exceptions left and right. We want
        #the trace to keep track of this as well!
        try:
            #Grab the result of calling the function, mind you this line
            #calls this very __call__ function again!
            result = self.__f(*args, **dargs)

            #Prepares formatting for the return
            traced.nest_count -= 1
            out_pipes = "| " * traced.nest_count
            print out_pipes + "`- " + repr(result)
            return result
        except Exception, e:
            #Now if we actually did encounter an exception we need to let
            #the rest of the recursive calls finish properly, so just
            #raise the exception and maintain the tracing sturcture
            traced.nest_count -= 1
            raise e

#So I was back in pa5 making coffee while waiting for my crack-password
#function to run. Wouldn't it be great if crack-password just remembered
#what each input resulted in so I don't have to regrow my beard while it
#recomputes it? This amazeballs decorator solves this exact problem.
class memoized(object):
    def __init__(self,f):
        #Every function (that is, every instance of this class) will have its
        #own unique table linking inputs as keys to outputs.
        self.history = {}
        self.__f = f
        self.__name__ = f.__name__
    def __call__(self, *args, **dargs):
        #The "key" we use to access self.history is a giant string holding
        #all key/value pairs from dargs appended to all args.
        dictElems = []
        #This loop puts all key/value pairs from dargs into a list
        for dkey in dargs:
            dictElems.append((dkey,dargs[dkey]))
        key = str(args)
        #This loop smushes all regular args into one string
        for a in args:
            key += str(a)
        #This loop appends every string in dictElems list to key
        for de in dictElems:
            key += str(de[0]) + str(de[1])
        #Our key is finally built, we can see if it's in self.history
        if key in self.history :
            if isinstance(self.history[key], Exception):
                #If we discover this key reuslted in an exception, throw it!
                raise self.history[key]
            return  self.history[key]
        else:
            #Ah, we've got a key not in our self.history, time to add it!
            try:
                #Figure out what this key's value will be
                res = self.__f(*args, **dargs)
                self.history[key] = res
                return res
            except Exception, e:
                #If we encounter an exception, we keep track of that too!
                self.history[key] = e
            if isinstance(self.history[key], Exception):
                raise self.history[key]
            #Exception or not, you still return whatever you end up adding
            #To the function's history!
            return self.history[key]

# run some examples.  The output from this is in decorators.out
def run_examples():
    for f,a in [(fib_t,(7,)),
                (fib_mt,(7,)),
                (fib_tm,(7,)),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (fib_mp.reset,()),
                (fib_mp,(7,)),
                (fib_mp.count,()),
                (even_t,(6,)),
                (quicksort_t,([5,8,100,45,3,89,22,78,121,2,78],)),
                (quicksort_mt,([5,8,100,45,3,89,22,78,121,2,78],)),
                (quicksort_mt,([5,8,100,45,3,89,22,78,121,2,78],)),
                (change_t,([9,7,5],44)),
                (change_mt,([9,7,5],44)),
                (change_mt,([9,7,5],44)),
                ]:
        print "RUNNING %s(%s):" % (f.__name__,", ".join([repr(x) for x in a]))
        rv=f(*a)
        print "RETURNED %s" % repr(rv)

@traced
def fib_t(x):
    if x<=1:
        return 1
    else:
        return fib_t(x-1)+fib_t(x-2)

@traced
@memoized
def fib_mt(x):
    if x<=1:
        return 1
    else:
        return fib_mt(x-1)+fib_mt(x-2)

@memoized
@traced
def fib_tm(x):
    if x<=1:
        return 1
    else:
        return fib_tm(x-1)+fib_tm(x-2)

@profiled
@memoized
def fib_mp(x):
    if x<=1:
        return 1
    else:
        return fib_mp(x-1)+fib_mp(x-2)

@traced
def even_t(x):
    if x==0:
        return True
    else:
        return odd_t(x-1)

@traced
def odd_t(x):
    if x==0:
        return False
    else:
        return even_t(x-1)

@traced
def quicksort_t(l):
    if len(l)<=1:
        return l
    pivot=l[0]
    left=quicksort_t([x for x in l[1:] if x<pivot])
    right=quicksort_t([x for x in l[1:] if x>=pivot])
    return left+l[0:1]+right

@traced
@memoized
def quicksort_mt(l):
    if len(l)<=1:
        return l
    pivot=l[0]
    left=quicksort_mt([x for x in l[1:] if x<pivot])
    right=quicksort_mt([x for x in l[1:] if x>=pivot])
    return left+l[0:1]+right

class ChangeException(Exception):
    pass

@traced
def change_t(l,a):
    if a==0:
        return []
    elif len(l)==0:
        raise ChangeException()
    elif l[0]>a:
        return change_t(l[1:],a)
    else:
        try:
            return [l[0]]+change_t(l,a-l[0])
        except ChangeException:
            return change_t(l[1:],a)

@traced
@memoized
def change_mt(l,a):
    if a==0:
        return []
    elif len(l)==0:
        raise ChangeException()
    elif l[0]>a:
        return change_mt(l[1:],a)
    else:
        try:
            return [l[0]]+change_mt(l,a-l[0])
        except ChangeException:
            return change_mt(l[1:],a)


