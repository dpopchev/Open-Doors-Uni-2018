#!/usr/bin/env python

import aristotel
import galilee
import imp
import matplotlib.animation as animation

from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.gridspec import GridSpec
from IPython import get_ipython

imp.reload(aristotel)
imp.reload(galilee)
#~ get_ipython().run_line_magic("matplotlib", "qt5")

class motion:

    _parameters_default = {
        "m": [ 1, 5, 10 ],
        "b": 1,
        "g": 9.81,
        "x0": 0,
        "y0": 10,
        "vx0": 0,
        "vy0": 0,
        "t0": 0,
        "dt": 1e-3
    }

    def __init__(self, **kwargs):

        self.A = aristotel.motion()
        self.G = galilee.motion()

        self.m = []
        self.b = None
        self.g = None
        self.x0 = None
        self.y0 = None
        self.vx0 = None
        self.vy0 = None
        self.t0 = None
        self.dt = None
        self.ls_ms = []
        self.max_x = 0
        self.max_y = 0
        self.max_vx = 0
        self.max_vy = 0
        self.max_t = 0

        self.data_aristotel = {}
        self.data_galilee = {}

        self.change_params(**kwargs)

        return

    def change_params(self, **kwargs):

        for _ in kwargs.keys():
            if _.lower() not in list(_parameters_default.keys()):
                print("\n\n {} NOT KNOWN, skipping \n\n".format(_))
            else:
                self.__dict__[_] = kwargs[_]

        for _ in self._parameters_default.keys():
            if not self.__dict__[_]:
                self.__dict__[_] = self._parameters_default[_]

        self.ls_ms.clear()
        it_ls_ms = self._get_iter_all_ls_ms()

        for m, ls_ms in zip(self.m, it_ls_ms):
            self.ls_ms.append(ls_ms)

        self.max_x = 0
        self.min_x = 0

        self.max_y = 0
        self.min_y = 0

        self.max_vx = 0
        self.min_vx = 0

        self.max_vy = 0
        self.min_vy = 0

        self.max_t = 0
        self.min_t = 0

        return

    @staticmethod
    def _get_y_vy_plot():

        style.use("seaborn-poster")

        gs = GridSpec(nrows=1, ncols=2)

        fig = plt.figure()
        fig.set_tight_layout(True)

        ax_y = fig.add_subplot(gs[0,0])
        ax_vy = fig.add_subplot(gs[0,1])

        return fig, ax_y, ax_vy

    @staticmethod
    def _get_iter_all_ls_ms():

        from itertools import product
        from random import shuffle

        list_ls = [ "-", "--" ]
        list_ms = [ "o", "d", "x", "" ]

        all_combinations = [ _ for _ in product(list_ls, list_ms) ]

        shuffle(all_combinations)

        return iter(all_combinations)

    @staticmethod
    def _reduce_points(data, N=20):

        mevery = int(len(data)/(N-1))
        last = data[-1]

        data = data[::mevery]
        data.append(last)

        return data

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

        return

    def _set_max_min_y_vy_t(self, data):

        self.max_t = \
            self.max_t if abs(self.max_t) >= abs(max(data[0],key=abs)) else max(data[0],key=abs)

        self.min_t = \
            self.min_t if abs(self.min_t) >= abs(min(data[0],key=abs)) else min(data[0],key=abs)

        self.max_y = \
            self.max_y if abs(self.max_y) >= abs(max(data[1][1],key=abs)) else max(data[1][1],key=abs)

        self.min_y = \
            self.min_y if abs(self.min_y) >= abs(min(data[1][1],key=abs)) else min(data[1][1],key=abs)

        self.max_vy = \
            self.max_vy if abs(self.max_vy) >= abs(max(data[1][3],key=abs)) else max(data[1][3],key=abs)

        self.min_vy = \
            self.min_vy if abs(self.min_vy) >= abs(min(data[1][3],key=abs)) else min(data[1][3],key=abs)

        return

    def _load_aristotel_all(self):

        self.data_aristotel.clear()

        for _ in self.m:

            self.data_aristotel["m={}".format(_)] = self.A.get_data(m=_)

            self.data_aristotel["m={}".format(_)][0] = \
                self._reduce_points( self.data_aristotel["m={}".format(_)][0] )

            for ind, ydata in enumerate(self.data_aristotel["m={}".format(_)][1]):
                self.data_aristotel["m={}".format(_)][1][ind] = self._reduce_points( ydata )


        self.data_aristotel["c"] = "g"

    def plot_y_vy_all_aristotel(self):

        fig, ax_y, ax_vy = self._get_y_vy_plot()

        self._load_aristotel_all()

        self._set_plot_parms(ax_y, "time", "height")
        self._set_plot_parms(ax_vy, "time", "velocity")

        for _, ls_ms in zip(self.data_aristotel.keys() - "c", self.ls_ms):

            self._set_max_min_y_vy_t(self.data_aristotel[_])

            ax_y.plot(
                self.data_aristotel[_][0],
                self.data_aristotel[_][1][1],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_aristotel["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

            ax_vy.plot(
                self.data_aristotel[_][0],
                self.data_aristotel[_][1][3],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_aristotel["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

        ax_y.set_xlim(0, self.max_t + 0.05*self.max_t)
        ax_y.set_ylim(0, self.max_y + 0.05*self.max_y)
        ax_y.legend(loc="best",fontsize=10)

        ax_vy.set_xlim(0, self.max_t + 0.05*self.max_t)
        ax_vy.set_ylim(0, self.max_vy + 0.05*self.max_vy)
        ax_vy.legend(loc="best",fontsize=10)

        plt.show()

    def update_A_data(self):

        lengths = []
        for _ in self.data_aristotel.keys() - "c":
            lengths.append(len(self.data_aristotel[_][0]) + 1)

        i = 1
        while i <= max(lengths):

            yield {
                mass: [
                    self.data_aristotel[mass][0][:i], [
                        ypoints[:i] for ypoints in self.data_aristotel[mass][1]
                    ]
                ] for mass in self.data_aristotel.keys() - "c"
            }

            i += 1

    def update_A_plot(self, frame, ax_y, ax_vy):

        self._set_plot_parms(ax_y, "time", "height")
        self._set_plot_parms(ax_vy, "time", "velocity")

        for _, ls_ms in zip(frame, self.ls_ms):

            self._set_max_min_y_vy_t(self.data_aristotel[_])

            ax_y.plot(
                frame[_][0],
                frame[_][1][1],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_aristotel["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

            ax_vy.plot(
                frame[_][0],
                frame[_][1][3],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_aristotel["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

        ax_y.set_xlim(0, self.max_t + 0.05*self.max_t)
        ax_y.set_ylim(0, self.max_y + 0.05*self.max_y)
        ax_y.legend(loc="best",fontsize=10)

        ax_vy.set_xlim(0, self.max_t + 0.05*self.max_t)
        ax_vy.set_ylim(0, self.max_vy + 0.05*self.max_vy)
        ax_vy.legend(loc="best",fontsize=10)

    def animate_all_aristotel(self):

        fig, ax_y, ax_vy = self._get_y_vy_plot()

        self._load_aristotel_all()

        ani = animation.FuncAnimation(
            fig=fig,
            func=self.update_A_plot,
            fargs=(ax_y, ax_vy),
            frames=self.update_A_data,
            interval=500,
            repeat=False
        )

        plt.show()

    def _load_galilee_all(self):

        self.data_galilee.clear()

        for _ in self.m:

            self.data_galilee["m={}".format(_)] = self.G.get_data(g=self.g)

            self.data_galilee["m={}".format(_)][0] = \
                self._reduce_points( self.data_galilee["m={}".format(_)][0] )

            for ind, ydata in enumerate(self.data_galilee["m={}".format(_)][1]):
                self.data_galilee["m={}".format(_)][1][ind] = self._reduce_points( ydata )


        self.data_galilee["c"] = "r"

    def plot_y_vy_all_galilee(self):

        fig, ax_y, ax_vy = self._get_y_vy_plot()

        self._load_galilee_all()

        self._set_plot_parms(ax_y, "time", "height")
        self._set_plot_parms(ax_vy, "time", "velocity")

        for _, ls_ms in zip(self.data_galilee.keys() - "c", self.ls_ms):

            self._set_max_min_y_vy_t(self.data_galilee[_])

            ax_y.plot(
                self.data_galilee[_][0],
                self.data_galilee[_][1][1],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_galilee["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

            ax_vy.plot(
                self.data_galilee[_][0],
                self.data_galilee[_][1][3],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_galilee["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

        ax_y.set_xlim(
            self.min_t - 0.05*self.min_t,
            self.max_t + 0.05*self.max_t
        )
        ax_y.set_ylim(
            self.min_y - 0.05*self.min_y,
            self.max_y + 0.05*self.max_y
        )
        ax_y.legend(loc="best",fontsize=10)

        ax_vy.set_xlim(
            self.min_t - 0.05*self.min_t,
            self.max_t + 0.05*self.max_t
        )

        ax_vy.set_ylim(
            self.min_vy - 0.05*self.min_vy,
            self.max_vy + 0.05*self.max_vy
        )
        ax_vy.legend(loc="best",fontsize=10)

        plt.show()

    def update_G_data(self):

        lengths = []
        for _ in self.data_galilee.keys() - "c":
            lengths.append(len(self.data_galilee[_][0]) + 1)

        i = 1
        while i <= max(lengths):

            yield {
                mass: [
                    self.data_galilee[mass][0][:i], [
                        ypoints[:i] for ypoints in self.data_galilee[mass][1]
                    ]
                ] for mass in self.data_galilee.keys() - "c"
            }

            i += 1

    def update_G_plot(self, frame, ax_y, ax_vy):

        self._set_plot_parms(ax_y, "time", "height")
        self._set_plot_parms(ax_vy, "time", "velocity")

        for _, ls_ms in zip(frame, self.ls_ms):

            self._set_max_min_y_vy_t(self.data_galilee[_])

            ax_y.plot(
                frame[_][0],
                frame[_][1][1],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_galilee["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

            ax_vy.plot(
                frame[_][0],
                frame[_][1][3],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_galilee["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

        ax_y.set_xlim(
            self.min_t - 0.05*self.min_t,
            self.max_t + 0.05*self.max_t
        )
        ax_y.set_ylim(
            self.min_y - 0.05*self.min_y,
            self.max_y + 0.05*self.max_y
        )
        ax_y.legend(loc="best",fontsize=10)

        ax_vy.set_xlim(
            self.min_t - 0.05*self.min_t,
            self.max_t + 0.05*self.max_t
        )

        ax_vy.set_ylim(
            self.min_vy - 0.05*self.min_vy,
            self.max_vy + 0.05*self.max_vy
        )
        ax_vy.legend(loc="best",fontsize=10)

    def animate_all_galilee(self):

        fig, ax_y, ax_vy = self._get_y_vy_plot()

        self._load_galilee_all()

        ani = animation.FuncAnimation(
            fig=fig,
            func=self.update_G_plot,
            fargs=(ax_y, ax_vy),
            frames=self.update_G_data,
            interval=500,
            repeat=False
        )

        plt.show()


    #@staticmethod
    #def _get_N_random_colors(N=4):

        #from random import shuffle

        #styles_colours = ["b", "g", "r", "c", "m", "y", "k"]
        #shuffle(styles_colours)

        #return styles_colours[:N]

    #def _generate_free_fall_data(self):

        #self.data_aristotel.clear()
        #self.data_galilee_NoAir.clear()
        #self.data_galilee_Air.clear()
        #self.data_newton.clear()

        #for _ in self.m:

            #self.data_aristotel[str(_)] = {"t": [], "h": []}

            #self.data_aristotel[str(_)]["t"], \
            #self.data_aristotel[str(_)]["h"] = self.A.free_fall_HvsT(
                #m = _, h = self.h, b = self.b, dt = self.dt
            #)

            #self.data_galilee_NoAir[str(_)] = {"t": [], "h": []}

            #self.data_galilee_NoAir[str(_)]["t"], \
            #self.data_galilee_NoAir[str(_)]["h"] = self.G.free_fall_NoAir_HvsT(
                #m = _, h = self.h, b = self.b, dt = self.dt, v0 = self.v0
            #)

            #self.data_galilee_Air[str(_)] = {"t": [], "h": []}

            #self.data_galilee_Air[str(_)]["t"], \
            #self.data_galilee_Air[str(_)]["h"] = self.G.free_fall_Air_HvsT(
                #m = _, h = self.h, b = self.b, dt = self.dt, v0 = self.v0
            #)

            #self.data_newton[str(_)] = {"t": [], "h": []}

            #self.data_newton[str(_)]["t"], \
            #self.data_newton[str(_)]["h"] = self.N.free_fall_HvsT(
                #m = _, h = self.h, b = self.b, dt = self.dt, v0 = self.v0
            #)

        #return



    #def plot_all_free_fall_data(self):

        #from matplotlib import pyplot as plt

        #fig, ax = plt.subplots()
        #fig.set_tight_layout(True)

        #self._set_plot_parms(ax, "t", "h")

        #self._generate_free_fall_data()

        #iter_ls_ms = self._get_iter_all_ls_ms()

        #c_A, c_G_NoAir, c_G_Air, c_N = self._get_N_random_colors()

        #linewidth = 1.2
        #markersize = 5

        #N_markers = 10

        #for mass in self.m:

            #ls, ms = next(iter_ls_ms)

            #markevery = int(len(self.data_aristotel[str(mass)]["t"])/N_markers)
            #ax.plot(
                #self.data_aristotel[str(mass)]["t"],
                #self.data_aristotel[str(mass)]["h"][0],
                #linewidth=linewidth,
                #linestyle=ls,
                #marker=ms,
                #markersize=markersize,
                #markevery=markevery,
                #color=c_A,
                #label="Aristotel, m = {}".format(mass)
            #)

            #markevery = int(len(self.data_galilee_NoAir[str(mass)]["t"])/N_markers)
            #ax.plot(
                #self.data_galilee_NoAir[str(mass)]["t"],
                #self.data_galilee_NoAir[str(mass)]["h"][0],
                #linewidth=linewidth,
                #linestyle=ls,
                #marker=ms,
                #markersize=markersize,
                #markevery=markevery,
                #color=c_G_NoAir,
                #label="Galilee_NoAir, m = {}".format(mass)
            #)

            #markevery = int(len(self.data_galilee_Air[str(mass)]["t"])/N_markers)
            #ax.plot(
                #self.data_galilee_Air[str(mass)]["t"],
                #self.data_galilee_Air[str(mass)]["h"][0],
                #linewidth=linewidth,
                #linestyle=ls,
                #marker=ms,
                #markersize=markersize,
                #markevery=markevery,
                #color=c_G_Air,
                #label="Galilee_Air, m = {}".format(mass)
            #)

            #markevery = int(len(self.data_newton[str(mass)]["t"])/N_markers)
            #ax.plot(
                #self.data_newton[str(mass)]["t"],
                #self.data_newton[str(mass)]["h"][0],
                #linewidth=linewidth,
                #linestyle=ls,
                #marker=ms,
                #markersize=markersize,
                #markevery=markevery,
                #color=c_N,
                #label="Newton, m = {}".format(mass)
            #)

        #ax.legend(loc="best",fontsize=8)

        #plt.show()

        #return

    #def _reduce_free_fall_data(self,N=10):
        #"""
        #reduce all the data up to 20 points, including the start and end

        #"""

        #for mass in self.m:

            #self.data_aristotel[str(mass)]["t"] = \
                #self._reducing_list_func(
                    #self.data_aristotel[str(mass)]["t"],
                    #N
                #)
            #self.data_aristotel[str(mass)]["h"][0] = \
                #self._reducing_list_func(
                    #self.data_aristotel[str(mass)]["h"][0],
                    #N
                #)

            #self.data_galilee_NoAir[str(mass)]["t"] = \
                #self._reducing_list_func(
                    #self.data_galilee_NoAir[str(mass)]["t"],
                    #N
                #)
            #self.data_galilee_NoAir[str(mass)]["h"][0] = \
                #self._reducing_list_func(
                    #self.data_galilee_NoAir[str(mass)]["h"][0],
                    #N
                #)

            #self.data_galilee_Air[str(mass)]["t"] = \
                #self._reducing_list_func(
                    #self.data_galilee_Air[str(mass)]["t"],
                    #N
                #)
            #self.data_galilee_Air[str(mass)]["h"][0] = \
                #self._reducing_list_func(
                    #self.data_galilee_Air[str(mass)]["h"][0],
                    #N
                #)

            #self.data_newton[str(mass)]["t"] = \
                #self._reducing_list_func(
                    #self.data_newton[str(mass)]["t"],
                    #N
                #)
            #self.data_newton[str(mass)]["h"][0] = \
                #self._reducing_list_func(
                    #self.data_newton[str(mass)]["h"][0],
                    #N
                #)

    #def get_data_aristotel(self):

        #t_all = [ [] for _ in self.m ]
        #h_all = [ [] for _ in self.m ]

        #for tm1, hm1, tm2, hm2, tm3, hm3 in zip(
            #self.data_aristotel[str(self.m[0])]["t"],
            #self.data_aristotel[str(self.m[0])]["h"][0],
            #self.data_aristotel[str(self.m[1])]["t"],
            #self.data_aristotel[str(self.m[1])]["h"][0],
            #self.data_aristotel[str(self.m[2])]["t"],
            #self.data_aristotel[str(self.m[2])]["h"][0],
        #):

            #t_all[0].append(tm1)
            #h_all[0].append(hm1)

            #t_all[1].append(tm2)
            #h_all[1].append(hm2)

            #t_all[2].append(tm3)
            #h_all[2].append(hm3)

            #yield t_all[0], h_all[0], t_all[1], h_all[1], t_all[2], h_all[2]

    #def update_aristotel(self,frame):

        #self._set_plot_parms(self.ax, "t", "h")

        #self.ax.plot(
            #frame[0],
            #frame[1],
            #linewidth=1.5,
            #linestyle="-",
            #marker="o",
            #markersize=8,
            #color="k",
            #label=" m = {} ".format(str(self.m[0]))
        #)

        #self.ax.plot(
            #frame[2],
            #frame[3],
            #linewidth=1.5,
            #linestyle="-",
            #marker="o",
            #markersize=8,
            #color="k",
            #label=" m = {}".format(str(self.m[1]))
        #)
        #self.ax.plot(
            #frame[4],
            #frame[5],
            #linewidth=1.5,
            #linestyle="-",
            #marker="o",
            #markersize=8,
            #color="k",
            #label=" m = {} ".format(str(self.m[2]))
        #)

        #self.ax.legend(loc="best",fontsize=8)

        #return

    #def animate_all_aristotel(self):

        #import matplotlib.pyplot as plt
        #import matplotlib.animation as animation

        #self._generate_free_fall_data()
        #self._reduce_free_fall_data()

        #fig, self.ax = plt.subplots()
        #fig.set_tight_layout(True)

        #ani = animation.FuncAnimation(
            #fig = fig,
            #func = self.update_aristotel,
            #frames = self.get_data_aristotel,
            #interval = 500,
            #repeat = False
        #)

        #plt.show()

    #def _set_plot_parms_galilee_NoAir(self,ax, label_x, label_y):

        #self._set_plot_parms(ax, "t", "h")

        #for mass in self.m:
            #ax.plot(
                #self.data_aristotel[str(mass)]["t"],
                #self.data_aristotel[str(mass)]["h"][0],
                #linewidth=1.5,
                #linestyle="-",
                #marker="o",
                #markersize=8,
                #color="k",
                #label="Aristotel m = {}".format(mass)
            #)

    #def get_data_galilee_NoAir(self):

        #t_all = [ [] for _ in self.m ]
        #h_all = [ [] for _ in self.m ]

        #for tm1, hm1, tm2, hm2, tm3, hm3 in zip(
            #self.data_galilee_NoAir[str(self.m[0])]["t"],
            #self.data_galilee_NoAir[str(self.m[0])]["h"][0],
            #self.data_galilee_NoAir[str(self.m[1])]["t"],
            #self.data_galilee_NoAir[str(self.m[1])]["h"][0],
            #self.data_galilee_NoAir[str(self.m[2])]["t"],
            #self.data_galilee_NoAir[str(self.m[2])]["h"][0],
        #):

            #t_all[0].append(tm1)
            #h_all[0].append(hm1)

            #t_all[1].append(tm2)
            #h_all[1].append(hm2)

            #t_all[2].append(tm3)
            #h_all[2].append(hm3)

            #yield t_all[0], h_all[0], t_all[1], h_all[1], t_all[2], h_all[2]

    #def update_galilee_NoAir(self,frame):

        #self._set_plot_parms_galilee_NoAir(self.ax, "t", "h")

        #self.ax.plot(
            #frame[0],
            #frame[1],
            #linewidth=1.5,
            #linestyle="--",
            #marker="X",
            #markersize=8,
            #color="b",
            #label=" m = {} ".format(str(self.m[0]))
        #)

        #self.ax.plot(
            #frame[2],
            #frame[3],
            #linewidth=1.5,
            #linestyle="--",
            #marker="X",
            #markersize=8,
            #color="b",
            #label=" m = {}".format(str(self.m[1]))
        #)

        #self.ax.plot(
            #frame[4],
            #frame[5],
            #linewidth=1.5,
            #linestyle="--",
            #marker="X",
            #markersize=8,
            #color="b",
            #label=" m = {} ".format(str(self.m[2]))
        #)

        #self.ax.legend(loc="best",fontsize=8)

        #return

    #def animate_all_galilee_NoAir(self):

        #import matplotlib.pyplot as plt
        #import matplotlib.animation as animation

        #self._generate_free_fall_data()
        #self._reduce_free_fall_data()

        #fig, self.ax = plt.subplots()
        #fig.set_tight_layout(True)

        #ani = animation.FuncAnimation(
            #fig = fig,
            #func = self.update_galilee_NoAir,
            #frames = self.get_data_galilee_NoAir,
            #interval = 500,
            #repeat = False
        #)

        #plt.show()

    #def _set_plot_parms_galilee_Air(self,ax, label_x, label_y):

        #self._set_plot_parms_galilee_NoAir(ax, "t", "h")

        #for mass in self.m:
            #ax.plot(
                #self.data_galilee_NoAir[str(mass)]["t"],
                #self.data_galilee_NoAir[str(mass)]["h"][0],
                #linewidth=1.5,
                #linestyle="--",
                #marker="X",
                #markersize=8,
                #color="b",
                #label="Galilee No Air m = {}".format(mass)
            #)

    #def get_data_galilee_Air(self):

        #t_all = [ [] for _ in self.m ]
        #h_all = [ [] for _ in self.m ]

        #for tm1, hm1, tm2, hm2, tm3, hm3 in zip(
            #self.data_galilee_Air[str(self.m[0])]["t"],
            #self.data_galilee_Air[str(self.m[0])]["h"][0],
            #self.data_galilee_Air[str(self.m[1])]["t"],
            #self.data_galilee_Air[str(self.m[1])]["h"][0],
            #self.data_galilee_Air[str(self.m[2])]["t"],
            #self.data_galilee_Air[str(self.m[2])]["h"][0],
        #):

            #t_all[0].append(tm1)
            #h_all[0].append(hm1)

            #t_all[1].append(tm2)
            #h_all[1].append(hm2)

            #t_all[2].append(tm3)
            #h_all[2].append(hm3)

            #yield t_all[0], h_all[0], t_all[1], h_all[1], t_all[2], h_all[2]

    #def update_galilee_Air(self,frame):

        #self._set_plot_parms_galilee_Air(self.ax, "t", "h")

        #self.ax.plot(
            #frame[0],
            #frame[1],
            #linewidth=1.5,
            #linestyle="--",
            #marker="x",
            #markersize=8,
            #color="b",
            #label=" m = {} ".format(str(self.m[0]))
        #)

        #self.ax.plot(
            #frame[2],
            #frame[3],
            #linewidth=1.5,
            #linestyle="--",
            #marker="x",
            #markersize=8,
            #color="b",
            #label=" m = {}".format(str(self.m[1]))
        #)

        #self.ax.plot(
            #frame[4],
            #frame[5],
            #linewidth=1.5,
            #linestyle="--",
            #marker="x",
            #markersize=8,
            #color="b",
            #label=" m = {} ".format(str(self.m[2]))
        #)

        #self.ax.legend(loc="best",fontsize=8)

        #return

    #def animate_all_galilee_Air(self):

        #import matplotlib.pyplot as plt
        #import matplotlib.animation as animation

        #self._generate_free_fall_data()
        #self._reduce_free_fall_data()

        #fig, self.ax = plt.subplots()
        #fig.set_tight_layout(True)

        #ani = animation.FuncAnimation(
            #fig = fig,
            #func = self.update_galilee_Air,
            #frames = self.get_data_galilee_Air,
            #interval = 500,
            #repeat = False
        #)

        #plt.show()

    #def _set_plot_parms_newton(self,ax, label_x, label_y):

        #self._set_plot_parms_galilee_Air(ax, "t", "h")

        #for mass in self.m:
            #ax.plot(
                #self.data_galilee_Air[str(mass)]["t"],
                #self.data_galilee_Air[str(mass)]["h"][0],
                #linewidth=1.5,
                #linestyle="--",
                #marker="x",
                #markersize=8,
                #color="b",
                #label="Galilee Air m = {}".format(mass)
            #)

    #def get_data_newton(self):

        #t_all = [ [] for _ in self.m ]
        #h_all = [ [] for _ in self.m ]

        #for tm1, hm1, tm2, hm2, tm3, hm3 in zip(
            #self.data_newton[str(self.m[0])]["t"],
            #self.data_newton[str(self.m[0])]["h"][0],
            #self.data_newton[str(self.m[1])]["t"],
            #self.data_newton[str(self.m[1])]["h"][0],
            #self.data_newton[str(self.m[2])]["t"],
            #self.data_newton[str(self.m[2])]["h"][0],
        #):

            #t_all[0].append(tm1)
            #h_all[0].append(hm1)

            #t_all[1].append(tm2)
            #h_all[1].append(hm2)

            #t_all[2].append(tm3)
            #h_all[2].append(hm3)

            #yield t_all[0], h_all[0], t_all[1], h_all[1], t_all[2], h_all[2]

    #def update_newton(self,frame):

        #self._set_plot_parms_newton(self.ax, "t", "h")

        #self.ax.plot(
            #frame[0],
            #frame[1],
            #linewidth=1.5,
            #linestyle="-.",
            #marker="*",
            #markersize=8,
            #color="m",
            #label=" m = {} ".format(str(self.m[0]))
        #)

        #self.ax.plot(
            #frame[2],
            #frame[3],
            #linewidth=1.5,
            #linestyle="-.",
            #marker="*",
            #markersize=8,
            #color="m",
            #label=" m = {}".format(str(self.m[1]))
        #)

        #self.ax.plot(
            #frame[4],
            #frame[5],
            #linewidth=1.5,
            #linestyle="-.",
            #marker="*",
            #markersize=8,
            #color="m",
            #label=" m = {} ".format(str(self.m[2]))
        #)

        #self.ax.legend(loc="best",fontsize=8)

        #return

    #def animate_all_newton(self):

        #import matplotlib.pyplot as plt
        #import matplotlib.animation as animation

        #self._generate_free_fall_data()
        #self._reduce_free_fall_data()

        #fig, self.ax = plt.subplots()
        #fig.set_tight_layout(True)

        #ani = animation.FuncAnimation(
            #fig = fig,
            #func = self.update_newton,
            #frames = self.get_data_newton,
            #interval = 500,
            #repeat = False
        #)

        #plt.show()

if __name__ == "__main__":

    print("\n Hello world \n")

