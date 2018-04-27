#!/usr/bin/env python


class motion:

    _parameters_default = {
        "m": [1,5,10],
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
        class to make the graphs, aristotel, galilee and newton should be inside
        the same folder !!!
        """

        import aristotel
        import galilee
        import newton

        self.A = aristotel.motion()
        self.G = galilee.motion()
        self.N = newton.motion()

        self.m = None
        self.b = None
        self.h = None
        self.l = None
        self.dt = None
        self.t = None
        self.g = None
        self.v0 = None

        self.data_aristotel = {}
        self.data_galilee_NoAir = {}
        self.data_galilee_Air = {}
        self.data_newton = {}

        self.change_params(**kwargs)

        return

    @staticmethod
    def _get_iter_all_ls_ms():

        from itertools import product
        from random import shuffle

        list_ls = [ "-", "--", "-." ]
        list_ms = [ "o", "d", "x", "" ]

        all_combinations = [ _ for _ in product(list_ls, list_ms) ]

        shuffle(all_combinations)

        return iter(all_combinations)

    @staticmethod
    def _get_N_random_colors(N=4):

        from random import shuffle

        styles_colours = ["b", "g", "r", "c", "m", "y", "k"]
        shuffle(styles_colours)

        return styles_colours[:N]

    def change_params(self, **kwargs):
        """
        change the any value of any attribute of the class

        Parameters
        ----------
        m: list
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

        for _key in self._parameters_default.keys():
            if not self.__dict__[_key]:
                self.__dict__[_key] = self._parameters_default[_key]

        return

    def _generate_free_fall_data(self):

        self.data_aristotel.clear()
        self.data_galilee_NoAir.clear()
        self.data_galilee_Air.clear()
        self.data_newton.clear()

        for _ in self.m:

            self.data_aristotel[str(_)] = {"t": [], "h": []}

            self.data_aristotel[str(_)]["t"], \
            self.data_aristotel[str(_)]["h"] = self.A.free_fall_HvsT(
                m = _, h = self.h, b = self.b, dt = self.dt
            )

            self.data_galilee_NoAir[str(_)] = {"t": [], "h": []}

            self.data_galilee_NoAir[str(_)]["t"], \
            self.data_galilee_NoAir[str(_)]["h"] = self.G.free_fall_NoAir_HvsT(
                m = _, h = self.h, b = self.b, dt = self.dt, v0 = self.v0
            )

            self.data_galilee_Air[str(_)] = {"t": [], "h": []}

            self.data_galilee_Air[str(_)]["t"], \
            self.data_galilee_Air[str(_)]["h"] = self.G.free_fall_Air_HvsT(
                m = _, h = self.h, b = self.b, dt = self.dt, v0 = self.v0
            )

            self.data_newton[str(_)] = {"t": [], "h": []}

            self.data_newton[str(_)]["t"], \
            self.data_newton[str(_)]["h"] = self.N.free_fall_HvsT(
                m = _, h = self.h, b = self.b, dt = self.dt, v0 = self.v0
            )

        return

    @staticmethod
    def _set_plot_parms(ax, label_x, label_y):

        from matplotlib.ticker import FormatStrFormatter

        fontsize = 12
        ticksize = 10

        ax.clear()

        ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax.set_xlabel(label_x, fontsize=fontsize)
        ax.xaxis.set_tick_params(labelsize=ticksize)

        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax.set_ylabel(label_y, fontsize=fontsize)
        ax.yaxis.set_tick_params(labelsize=ticksize)

        ax.set_xlim(0,11)
        ax.set_ylim(0,10)

        return

    def plot_all_free_fall_data(self):

        from matplotlib import pyplot as plt

        fig, ax = plt.subplots()
        fig.set_tight_layout(True)

        self._set_plot_parms(ax, "t", "h")

        self._generate_free_fall_data()

        iter_ls_ms = self._get_iter_all_ls_ms()

        c_A, c_G_NoAir, c_G_Air, c_N = self._get_N_random_colors()

        linewidth = 1.2
        markersize = 5

        N_markers = 10

        for mass in self.m:

            ls, ms = next(iter_ls_ms)

            markevery = int(len(self.data_aristotel[str(mass)]["t"])/N_markers)
            ax.plot(
                self.data_aristotel[str(mass)]["t"],
                self.data_aristotel[str(mass)]["h"][0],
                linewidth=linewidth,
                linestyle=ls,
                marker=ms,
                markersize=markersize,
                markevery=markevery,
                color=c_A,
                label="Aristotel, m = {}".format(mass)
            )

            markevery = int(len(self.data_galilee_NoAir[str(mass)]["t"])/N_markers)
            ax.plot(
                self.data_galilee_NoAir[str(mass)]["t"],
                self.data_galilee_NoAir[str(mass)]["h"][0],
                linewidth=linewidth,
                linestyle=ls,
                marker=ms,
                markersize=markersize,
                markevery=markevery,
                color=c_G_NoAir,
                label="Galilee_NoAir, m = {}".format(mass)
            )

            markevery = int(len(self.data_galilee_Air[str(mass)]["t"])/N_markers)
            ax.plot(
                self.data_galilee_Air[str(mass)]["t"],
                self.data_galilee_Air[str(mass)]["h"][0],
                linewidth=linewidth,
                linestyle=ls,
                marker=ms,
                markersize=markersize,
                markevery=markevery,
                color=c_G_Air,
                label="Galilee_Air, m = {}".format(mass)
            )

            markevery = int(len(self.data_newton[str(mass)]["t"])/N_markers)
            ax.plot(
                self.data_newton[str(mass)]["t"],
                self.data_newton[str(mass)]["h"][0],
                linewidth=linewidth,
                linestyle=ls,
                marker=ms,
                markersize=markersize,
                markevery=markevery,
                color=c_N,
                label="Newton, m = {}".format(mass)
            )

        ax.legend(loc="best",fontsize=8)

        plt.show()

        return

    @staticmethod
    def _reducing_list_func(lreduce, N):

        mevery = int(len(lreduce)/N)
        last = lreduce[-1]

        lreduce = lreduce[::mevery]

        lreduce.append(last)

        return lreduce

    def _reduce_free_fall_data(self,N=10):
        """
        reduce all the data up to 20 points, including the start and end

        """

        for mass in self.m:

            self.data_aristotel[str(mass)]["t"] = \
                self._reducing_list_func(
                    self.data_aristotel[str(mass)]["t"],
                    N
                )
            self.data_aristotel[str(mass)]["h"][0] = \
                self._reducing_list_func(
                    self.data_aristotel[str(mass)]["h"][0],
                    N
                )

            self.data_galilee_NoAir[str(mass)]["t"] = \
                self._reducing_list_func(
                    self.data_galilee_NoAir[str(mass)]["t"],
                    N
                )
            self.data_galilee_NoAir[str(mass)]["h"][0] = \
                self._reducing_list_func(
                    self.data_galilee_NoAir[str(mass)]["h"][0],
                    N
                )

            self.data_galilee_Air[str(mass)]["t"] = \
                self._reducing_list_func(
                    self.data_galilee_Air[str(mass)]["t"],
                    N
                )
            self.data_galilee_Air[str(mass)]["h"][0] = \
                self._reducing_list_func(
                    self.data_galilee_Air[str(mass)]["h"][0],
                    N
                )

            self.data_newton[str(mass)]["t"] = \
                self._reducing_list_func(
                    self.data_newton[str(mass)]["t"],
                    N
                )
            self.data_newton[str(mass)]["h"][0] = \
                self._reducing_list_func(
                    self.data_newton[str(mass)]["h"][0],
                    N
                )

    def get_data_aristotel(self):

        t_all = [ [] for _ in self.m ]
        h_all = [ [] for _ in self.m ]

        for tm1, hm1, tm2, hm2, tm3, hm3 in zip(
            self.data_aristotel[str(self.m[0])]["t"],
            self.data_aristotel[str(self.m[0])]["h"][0],
            self.data_aristotel[str(self.m[1])]["t"],
            self.data_aristotel[str(self.m[1])]["h"][0],
            self.data_aristotel[str(self.m[2])]["t"],
            self.data_aristotel[str(self.m[2])]["h"][0],
        ):

            t_all[0].append(tm1)
            h_all[0].append(hm1)

            t_all[1].append(tm2)
            h_all[1].append(hm2)

            t_all[2].append(tm3)
            h_all[2].append(hm3)

            yield t_all[0], h_all[0], t_all[1], h_all[1], t_all[2], h_all[2]

    def update_aristotel(self,frame):

        self._set_plot_parms(self.ax, "t", "h")

        self.ax.plot(
            frame[0],
            frame[1],
            linewidth=1.5,
            linestyle="-",
            marker="o",
            markersize=8,
            color="k",
            label=" m = {} ".format(str(self.m[0]))
        )

        self.ax.plot(
            frame[2],
            frame[3],
            linewidth=1.5,
            linestyle="-",
            marker="o",
            markersize=8,
            color="k",
            label=" m = {}".format(str(self.m[1]))
        )
        self.ax.plot(
            frame[4],
            frame[5],
            linewidth=1.5,
            linestyle="-",
            marker="o",
            markersize=8,
            color="k",
            label=" m = {} ".format(str(self.m[2]))
        )

        self.ax.legend(loc="best",fontsize=8)

        return

    def animate_all_aristotel(self):

        import matplotlib.pyplot as plt
        import matplotlib.animation as animation

        self._generate_free_fall_data()
        self._reduce_free_fall_data()

        fig, self.ax = plt.subplots()
        fig.set_tight_layout(True)

        ani = animation.FuncAnimation(
            fig = fig,
            func = self.update_aristotel,
            frames = self.get_data_aristotel,
            interval = 500,
            repeat = False
        )

        plt.show()

    def _set_plot_parms_galilee_NoAir(self,ax, label_x, label_y):

        self._set_plot_parms(ax, "t", "h")

        for mass in self.m:
            ax.plot(
                self.data_aristotel[str(mass)]["t"],
                self.data_aristotel[str(mass)]["h"][0],
                linewidth=1.5,
                linestyle="-",
                marker="o",
                markersize=8,
                color="k",
                label="Aristotel m = {}".format(mass)
            )

    def get_data_galilee_NoAir(self):

        t_all = [ [] for _ in self.m ]
        h_all = [ [] for _ in self.m ]

        for tm1, hm1, tm2, hm2, tm3, hm3 in zip(
            self.data_galilee_NoAir[str(self.m[0])]["t"],
            self.data_galilee_NoAir[str(self.m[0])]["h"][0],
            self.data_galilee_NoAir[str(self.m[1])]["t"],
            self.data_galilee_NoAir[str(self.m[1])]["h"][0],
            self.data_galilee_NoAir[str(self.m[2])]["t"],
            self.data_galilee_NoAir[str(self.m[2])]["h"][0],
        ):

            t_all[0].append(tm1)
            h_all[0].append(hm1)

            t_all[1].append(tm2)
            h_all[1].append(hm2)

            t_all[2].append(tm3)
            h_all[2].append(hm3)

            yield t_all[0], h_all[0], t_all[1], h_all[1], t_all[2], h_all[2]

    def update_galilee_NoAir(self,frame):

        self._set_plot_parms_galilee_NoAir(self.ax, "t", "h")

        self.ax.plot(
            frame[0],
            frame[1],
            linewidth=1.5,
            linestyle="--",
            marker="X",
            markersize=8,
            color="b",
            label=" m = {} ".format(str(self.m[0]))
        )

        self.ax.plot(
            frame[2],
            frame[3],
            linewidth=1.5,
            linestyle="--",
            marker="X",
            markersize=8,
            color="b",
            label=" m = {}".format(str(self.m[1]))
        )

        self.ax.plot(
            frame[4],
            frame[5],
            linewidth=1.5,
            linestyle="--",
            marker="X",
            markersize=8,
            color="b",
            label=" m = {} ".format(str(self.m[2]))
        )

        self.ax.legend(loc="best",fontsize=8)

        return

    def animate_all_galilee_NoAir(self):

        import matplotlib.pyplot as plt
        import matplotlib.animation as animation

        self._generate_free_fall_data()
        self._reduce_free_fall_data()

        fig, self.ax = plt.subplots()
        fig.set_tight_layout(True)

        ani = animation.FuncAnimation(
            fig = fig,
            func = self.update_galilee_NoAir,
            frames = self.get_data_galilee_NoAir,
            interval = 500,
            repeat = False
        )

        plt.show()

    def _set_plot_parms_galilee_Air(self,ax, label_x, label_y):

        self._set_plot_parms_galilee_NoAir(ax, "t", "h")

        for mass in self.m:
            ax.plot(
                self.data_galilee_NoAir[str(mass)]["t"],
                self.data_galilee_NoAir[str(mass)]["h"][0],
                linewidth=1.5,
                linestyle="--",
                marker="X",
                markersize=8,
                color="b",
                label="Galilee No Air m = {}".format(mass)
            )

    def get_data_galilee_Air(self):

        t_all = [ [] for _ in self.m ]
        h_all = [ [] for _ in self.m ]

        for tm1, hm1, tm2, hm2, tm3, hm3 in zip(
            self.data_galilee_Air[str(self.m[0])]["t"],
            self.data_galilee_Air[str(self.m[0])]["h"][0],
            self.data_galilee_Air[str(self.m[1])]["t"],
            self.data_galilee_Air[str(self.m[1])]["h"][0],
            self.data_galilee_Air[str(self.m[2])]["t"],
            self.data_galilee_Air[str(self.m[2])]["h"][0],
        ):

            t_all[0].append(tm1)
            h_all[0].append(hm1)

            t_all[1].append(tm2)
            h_all[1].append(hm2)

            t_all[2].append(tm3)
            h_all[2].append(hm3)

            yield t_all[0], h_all[0], t_all[1], h_all[1], t_all[2], h_all[2]

    def update_galilee_Air(self,frame):

        self._set_plot_parms_galilee_Air(self.ax, "t", "h")

        self.ax.plot(
            frame[0],
            frame[1],
            linewidth=1.5,
            linestyle="--",
            marker="x",
            markersize=8,
            color="b",
            label=" m = {} ".format(str(self.m[0]))
        )

        self.ax.plot(
            frame[2],
            frame[3],
            linewidth=1.5,
            linestyle="--",
            marker="x",
            markersize=8,
            color="b",
            label=" m = {}".format(str(self.m[1]))
        )

        self.ax.plot(
            frame[4],
            frame[5],
            linewidth=1.5,
            linestyle="--",
            marker="x",
            markersize=8,
            color="b",
            label=" m = {} ".format(str(self.m[2]))
        )

        self.ax.legend(loc="best",fontsize=8)

        return

    def animate_all_galilee_Air(self):

        import matplotlib.pyplot as plt
        import matplotlib.animation as animation

        self._generate_free_fall_data()
        self._reduce_free_fall_data()

        fig, self.ax = plt.subplots()
        fig.set_tight_layout(True)

        ani = animation.FuncAnimation(
            fig = fig,
            func = self.update_galilee_Air,
            frames = self.get_data_galilee_Air,
            interval = 500,
            repeat = False
        )

        plt.show()

    def _set_plot_parms_newton(self,ax, label_x, label_y):

        self._set_plot_parms_galilee_Air(ax, "t", "h")

        for mass in self.m:
            ax.plot(
                self.data_galilee_Air[str(mass)]["t"],
                self.data_galilee_Air[str(mass)]["h"][0],
                linewidth=1.5,
                linestyle="--",
                marker="x",
                markersize=8,
                color="b",
                label="Galilee Air m = {}".format(mass)
            )

    def get_data_newton(self):

        t_all = [ [] for _ in self.m ]
        h_all = [ [] for _ in self.m ]

        for tm1, hm1, tm2, hm2, tm3, hm3 in zip(
            self.data_newton[str(self.m[0])]["t"],
            self.data_newton[str(self.m[0])]["h"][0],
            self.data_newton[str(self.m[1])]["t"],
            self.data_newton[str(self.m[1])]["h"][0],
            self.data_newton[str(self.m[2])]["t"],
            self.data_newton[str(self.m[2])]["h"][0],
        ):

            t_all[0].append(tm1)
            h_all[0].append(hm1)

            t_all[1].append(tm2)
            h_all[1].append(hm2)

            t_all[2].append(tm3)
            h_all[2].append(hm3)

            yield t_all[0], h_all[0], t_all[1], h_all[1], t_all[2], h_all[2]

    def update_newton(self,frame):

        self._set_plot_parms_newton(self.ax, "t", "h")

        self.ax.plot(
            frame[0],
            frame[1],
            linewidth=1.5,
            linestyle="-.",
            marker="*",
            markersize=8,
            color="m",
            label=" m = {} ".format(str(self.m[0]))
        )

        self.ax.plot(
            frame[2],
            frame[3],
            linewidth=1.5,
            linestyle="-.",
            marker="*",
            markersize=8,
            color="m",
            label=" m = {}".format(str(self.m[1]))
        )

        self.ax.plot(
            frame[4],
            frame[5],
            linewidth=1.5,
            linestyle="-.",
            marker="*",
            markersize=8,
            color="m",
            label=" m = {} ".format(str(self.m[2]))
        )

        self.ax.legend(loc="best",fontsize=8)

        return

    def animate_all_newton(self):

        import matplotlib.pyplot as plt
        import matplotlib.animation as animation

        self._generate_free_fall_data()
        self._reduce_free_fall_data()

        fig, self.ax = plt.subplots()
        fig.set_tight_layout(True)

        ani = animation.FuncAnimation(
            fig = fig,
            func = self.update_newton,
            frames = self.get_data_newton,
            interval = 500,
            repeat = False
        )

        plt.show()

if __name__ == "__main__":

    print("\n Hello world \n")

