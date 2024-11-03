   def f(x):
      return x % 2 != 0 and x % 3 != 0
   >>> filter(f, range(2, 25))
   [5, 7, 11, 13, 17, 19, 23]
   >>> [x for x in range(2, 25) if f(x)]
   [5, 7, 11, 13, 17, 19, 23]

