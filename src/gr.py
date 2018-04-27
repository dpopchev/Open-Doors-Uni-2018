#!/usr/bin/env python


class orbit:

    def __init__(self):
        pass

    @staticmethod
    def _eq_orbit(t, y, l, M, G, c):

        r, v = y

        return [ v, (2*v**2)/r + r - (G*M*r**2)/l**2 - (3*G*M)/c**2]

    def solve_orbit(self):

        from scipy.integrate import ode
        from math import sqrt

        r = ode(self._eq_orbit).set_integrator("dopri5")

        dt = 1e-3
        r_init = 1
        drdphi_init = 0.1

        M = 1
        G = 1
        c = 3
        l = 1.21

        r.set_f_params(l, M, G, c)
        r.set_initial_value(y=[r_init, drdphi_init], t=0)

        t_list = [ 0 ]
        y_nested_list = [ [ r_init ], [ drdphi_init ] ]

        k = 4

        while r.t < k*3.14:

            r.integrate(r.t+dt)

            print(r.t, r.y[0], r.y[1] )

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
