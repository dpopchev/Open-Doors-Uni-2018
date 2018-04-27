#!/usr/bin/env python


class motion:

    _parameters_default = {
        "m": 10,
        "b": 1,
        "g": 9.81,
        "x0": 0,
        "y0": 20,
        "vx0": 0,
        "vy0": 0,
        "t0": 0,
        "dt": 1e-3
    }

    def __init__(self, **kwargs):

        self.m = None
        self.b = None
        self.g = None
        self.x0 = None
        self.y0 = None
        self.vx0 = None
        self.vy0 = None
        self.t0 = None
        self.dt = None

        self.change_params(**kwargs)

        return

    def change_params(self, **kwargs):

        for _ in kwargs.keys():
            if _.lower() not in list(self._parameters_default.keys()):
                print("\n\n {} NOT KNOWN, skipping \n\n".format(_))
            else:
                self.__dict__[_] = kwargs[_]

        for _ in self._parameters_default.keys():
            if not self.__dict__[_]:
                self.__dict__[_] = self._parameters_default[_]

        return

    @staticmethod
    def _eq_motion(t, ode, g, m, b):

        x, y, vx, vy = ode

        return [
            vx,
            vy,
            ( (-1) if vx > 0 else (+1) )*(b/m)*vx,
            -g + ( (1) if vy > 0 else (-1) )*(b/m)*vy
        ]

    def time_it(self, **kwargs):

        self.change_params(**kwargs)

        from scipy.integrate import ode

        r = ode(self._eq_motion).set_integrator("dopri5")

        r.set_f_params(self.g, self.m, self.b)

        r.set_initial_value(
            y=[ self.x0, self.y0, self.vx0, self.vy0 ],
            t=self.t0
        )

        while r.integrate(r.t+self.dt)[1] >= 0:
            continue

        return r.t - self.dt

    def get_data(self, **kwargs):

        self.change_params(**kwargs)

        from scipy.integrate import ode

        r = ode(self._eq_motion).set_integrator("dopri5")

        r.set_f_params(self.g, self.m, self.b)

        r.set_initial_value(
            y=[ self.x0, self.y0, self.vx0, self.vy0 ],
            t=self.t0
        )

        t = [ r.t ]
        ode = [ [ _ ] for _ in r.y ]

        while r.integrate(r.t+self.dt)[1] >= 0:

            t.append(r.t)

            for i,j in zip(ode, r.y):
                i.append(j)

        return [ t, ode ]

if __name__ == "__main__":

    print("\n Hello world \n")
