class BrentDekkerError(Exception):
    __module__ = "builtins"

class BrentDekker:

    def __init__(self, func, ab_range, epsilon=1e-5):

        self.f = func
        self.a = ab_range[0]
        self.b = ab_range[1]
        self.epsilon = epsilon

        if self.f(self.a) * self.f(self.b) > 0:
            err = "f(a) and f(b) share the same sign!\n"
            err += f"f({self.a}) = {self.f(self.a)}\n"
            err += f"f({self.b}) = {self.f(self.b)}"
            raise BrentDekkerError(err)

    def interpolate(self):

        def inverse_quadratic(f, x1, x2, x3):
            x = x1 * (f(x2) * f(x3)) / ((f(x1) - f(x2)) * (f(x1) - f(x3)))
            x += x2 * (f(x1) * f(x3)) / ((f(x2) - f(x1)) * (f(x2) - f(x3)))
            x += x3 * (f(x1) * f(x2)) / ((f(x3) - f(x1)) * (f(x3) - f(x2)))
            return x

        def secant(f, x, y):
            return y - f(y) * ((y - x) / (f(y) - f(x)))
        
        def bisection(f, a, b):
        
            error = 10
            while error > 1e-5:
                m = (a + b) / 2
                fm = f(m)
                
                if f(a) * fm > 0:
                    a = m
                elif f(b) * fm > 0:
                    b = m        

                error = abs(fm)

            return m
        
        a = self.a
        b = self.b
        c = a

        bisection_last = False
        iqi_secant_last = False

        while abs(b-a) > self.epsilon:
            
            if abs(self.f(a)) < abs(self.f(b)):
                b_temp = b
                b = a
                a = b_temp

            if bisection_last and abs(s - b) >= 0.5 * abs(b - c):
                s = bisection(self.f, a, b)
            elif iqi_secant_last and abs(s - b) >= 0.5 * abs(c - d):
                s = bisection(self.f, a, b)
                iqi_secant_last = False
                bisection_last = True
            elif not (self.f(a) == self.f(b) or self.f(b) == self.f(c) or self.f(a) == self.f(c)):
                s = inverse_quadratic(self.f, a, c, b)
                iqi_secant_last = True
                bisection_last = False
            elif self.f(b) != self.f(c):
                s = secant(self.f, b, c)
                iqi_secant_last = True
                bisection_last = False
            else:
                s = bisection(self.f, a, b)
                iqi_secant_last = False
                bisection_last = True
            
            m = (a + b) / 2
            d = c
            c = b

            if b <= s <= (3 * a + b) / 4 or (3 * a + b) / 4 <= s <= b:
                b = s
            else:
                b = m

            if  self.f(b) * self.f(a) > 0:
                a = c

        return b
