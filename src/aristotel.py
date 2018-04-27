#!/usr/bin/env python


class motion:

    _parameters_default = {
        "m": 10,
        "b": 1,
        "h": 10,
        "l": 10,
        "dt": 1e-3,
        "t": 10
    }

    def __init__(self, **kwargs):
        """
        aristotel.equations contains

            change_params method:
                is to change any of the parameters, see it for more info

            free_fall_time:
                find the time for a body with given mass <m> to fall through
                height <h> and medium with resistance characterized by <b>
                using aristotel mechanics

            free_fall_HvsT:
                find the time for a body with given mass <m> to fall through
                height <h> and medium with resistance characterized by <b>
                using aristotel mechanics and return data to plot it
        """

        self.m = None
        self.b = None
        self.h = None
        self.l = None
        self.dt = None
        self.t = None

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
    def _eq_free_fall(t, y, m, b):

        return -m/b

    def free_fall_time(self, **kwargs):
        """
        find the time for a body with given mass <m> to fall through height <h>
        and medium with resistance characterized by <b> using aristotel
        mechanics, the smaller the <dt> the better the result

        Parameters
        ----------
        m: double
            mass the falling body

        h: double
            height to be fallen

        b: double
            drag coefficient of the medium

        dt: double
            step size of the time interval

        Returns
        -------
        :double
            the time for which the body falls distance <h>
        """

        self.change_params(**kwargs)

        from scipy.integrate import ode

        r = ode(self._eq_free_fall).set_integrator("dopri5")

        r.set_f_params(self.m, self.b)

        r.set_initial_value(y=self.h, t=0)

        while r.integrate(r.t+self.dt)[0] >= 0:
            continue

        return r.t - self.dt

    def free_fall_HvsT(self, **kwargs):
        """
        find the time for a body with given mass <m> to fall through height <h>
        and medium with resistance characterized by <b> using aristotel
        mechanics, the smaller the <dt> the better the result it will return
        list of time and corresponding height

        Parameters
        ----------
        m: double
            mass the falling body

        h: double
            height to be fallen

        b: double
            drag coefficient of the medium

        dt: double
            step size of the time interval


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

        r.set_f_params(self.m, self.b)

        r.set_initial_value(y=self.h, t=0)

        t_list = [ 0 ]
        y_nested_list = [ [ self.h ] ]

        while r.integrate(r.t+self.dt)[0] >= 0:

            t_list.append(r.t)
            y_nested_list[0].append(r.y[0])

        return t_list, y_nested_list

if __name__ == "__main__":

    print("\n Hello world \n")
