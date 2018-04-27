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


class orbit:

    _parameters_default = {
        "M": 1,
        "G": 1,
        "L": 1.21,
        "c": 3,
        "r0": 1,
        "drdphi0": 0,
        "phi0": 0,
        "dt": 1e-3,
        "k": 1
    }

    def __init__(self, **kwargs):

        self.M = None
        self.G = None
        self.L = None
        self.c = None
        self.r0 = None
        self.drdphi0 = None
        self.phi0 = None
        self.dt = None
        self.k = None

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
    def _eq_motion(t, ode, L, M, G):

        r, v = ode

        return [
            v,
            2*v**2/r + r - G*M*r**2/L**2
        ]

    def plot_k_period(self, **kwargs):

        from scipy.integrate import ode
        from matplotlib import pyplot as plt
        from matplotlib import style
        from matplotlib.gridspec import GridSpec

        self.change_params(**kwargs)

        r = ode(self._eq_motion).set_integrator("dopri5")

        r.set_f_params(self.L, self.M, self.G)

        r.set_initial_value(
            y=[ self.r0, self.drdphi0 ],
            t=self.phi0
        )

        phi= [ r.t ]
        ode = [ [ _ ] for _ in r.y ]

        while r.t <= self.k*2*3.14:

            r.integrate(r.t+self.dt)

            phi.append(r.t)

            for i,j in zip(ode, r.y):
                i.append(j)

        style.use("seaborn-poster")

        gs = GridSpec(nrows=1, ncols=2)

        fig = plt.figure()
        fig.set_tight_layout(True)

        ax_r = fig.add_subplot(gs[0,0], polar=True)
        ax_drdphi = fig.add_subplot(gs[0,1], polar=True)

        ax_r.plot(phi, ode[0], label="r(phi)")
        ax_drdphi.plot(phi, ode[1], label="drdphi")

        ax_r.legend(loc="best", fontsize=10)
        ax_drdphi.legend(loc="best", fontsize=10)

        plt.show()

        return

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
