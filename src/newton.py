#!/usr/bin/env python


class motion:

    _parameters_default = {
        "m": 10,
        "b": 1,
        "h": 10,
        "l": 10,
        "dt": 1e-3,
        "t": 10,
        "g": 9.81,
        "v0": 0
    }

    def __init__(self, **kwargs):
        """
        newton.equations contains following methods

            change_params:
                is to change any of the parameters, see it for more info

            free_fall_time:
                find the time for a body with given mass <m> to fall through
                height <h> and on planet with gravitational acceleration <g>
                and considering air resistance using newtonian mechanics

            free_fall_Air_HvsT:
                find the time for a body with given mass <m> to fall through
                height <h> and on planet with gravitational acceleration <g>
                and considering air resistance using newtonian mechanics
        """

        self.m = None
        self.b = None
        self.h = None
        self.l = None
        self.dt = None
        self.t = None
        self.g = None
        self.v0 = None

        self.change_params(**kwargs)

        return

    def change_params(self, **kwargs):
        """
        change the any value of any attribute of the class

        Parameters
        ----------
        m: double
            mass of the body in motion

        b: double
            drag coefficient of the medium in which it is moving

        h: double
            horizontal distance

        l: double
            vertical distance

        dt: double
            time stepsize

        t: double
            time interval

        g: double
            gravitational acceleration

        v0: double
            initial velocity

        Returns
        -------
        """

        for key in kwargs.keys():
            if key.lower() not in list(self.__dict__.keys()):
                print("\n\n {} NOT KNOWN, skipping \n\n".format(key))
            else:
                self.__dict__[key] = kwargs[key]

        for _key in self.__dict__.keys():
            if not self.__dict__[_key]:
                self.__dict__[_key] = self._parameters_default[_key]

        return

    @staticmethod
    def _eq_free_fall(t, y, g, b):

        h, v = y

        return [ v, -g - (-1 if v < 0 else +1 )*b*v**2 ]

    def free_fall_time(self, **kwargs):
        """
        find the time for a body with given mass <m> to fall through height <h>
        and on planet with gravitational acceleration <g> with considering
        air resistance, characterized by parameter <b> using newtonian mechanics,
        the result as good as small the stepsize <dt> is

        Parameters
        ----------
        m: double
            mass of the object

        h: double
            height to be fallen

        dt: double
            step size of the time interval

        g: double
            gravitational acceleration

        v0: double
            initial velocity, if positive value means the body is thrown up, if
            negative it is thrown towards the earth surface

        b: double
            air resistance parameter

        Returns
        -------
        :double
            the time for which the body falls distance <H>
        """

        self.change_params(**kwargs)

        from scipy.integrate import ode

        r = ode(self._eq_free_fall).set_integrator("dopri5")

        r.set_f_params(self.g, self.b)

        r.set_initial_value(y=[self.h, self.v0], t=0)

        while r.integrate(r.t+self.dt)[0] >= 0:
            continue

        return r.t - self.dt

    def free_fall_HvsT(self, **kwargs):
        """
        find the time for a body with given mass <m> to fall through height <h>
        and on planet with gravitational acceleration <g> with considering
        air resistance, characterized by parameter <b> using newtonian mechanics,
        the result as good as small the stepsize <dt> is

        Parameters
        ----------
        m: double
            mass of the object

        h: double
            height to be fallen

        dt: double
            step size of the time interval

        g: double
            gravitational acceleration

        v0: double
            initial velocity, if positive value means the body is thrown up, if
            negative it is thrown towards the earth surface

        b: double
            air resistance parameter

        Returns
        -------
        : tuple
            [0] is the time
            [1]: nested list
                [0]: list
                    the height position for the corresponding time
        """

        self.change_params(**kwargs)

        from scipy.integrate import ode

        r = ode(self._eq_free_fall).set_integrator("dopri5")

        r.set_f_params(self.g, self.b)

        r.set_initial_value(y=[self.h, self.v0], t=0)

        t_list = [ 0 ]
        y_nested_list = [ [ self.h ] ]

        while r.integrate(r.t+self.dt)[0] >= 0:

            t_list.append(r.t)
            y_nested_list[0].append(r.y[0])

        return t_list, y_nested_list

class orbit:

    def __init__(self):
        pass

    @staticmethod
    def _eq_orbit(t, y, l, M, G):

        r, v = y

        return [ v, (2*v**2)/r + r - (G*M*r**2)/l**2 ]

    def solve_orbit(self):

        from scipy.integrate import ode
        from math import sqrt
        from math import cos

        r = ode(self._eq_orbit).set_integrator("dopri5")

        dt = 1e-3
        r_init = 1
        drdphi_init = 0.1

        M = 1
        G = 1
        l = 1

        r.set_f_params(l, M, G)
        r.set_initial_value(y=[r_init, drdphi_init], t=0)

        t_list = [ 0 ]
        y_nested_list = [ [ r_init ], [ drdphi_init ] ]

        k = 4

        while r.t < k*3.14:

            r.integrate(r.t+dt)

            #~ print(r.t, r.y[0], r.y[1] )

            t_list.append(r.t)
            y_nested_list[0].append(r.y[0])
            y_nested_list[1].append(r.y[1])

        import matplotlib.pyplot as plt
        ax = plt.subplot(111, projection='polar')
        ax.plot(t_list, y_nested_list[0])

        fig2, ax2 = plt.subplots()

        ax2.plot(t_list, y_nested_list[0])

        #~ fig3, ax3 = plt.subplots()

        #~ ax3.plot(t_list, y_nested_list[1])

        plt.show()

        return t_list, y_nested_list

if __name__ == "__main__":

    print("\n Hello world \n")
