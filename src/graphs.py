#!/usr/bin/env python

import aristotel
import galilee
import newton
import imp
import matplotlib.animation as animation

from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.gridspec import GridSpec
from IPython import get_ipython

imp.reload(aristotel)
imp.reload(galilee)
imp.reload(newton)

#~ if you start it from jupyter qtconsole, this will create separated windows
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
        self.N = newton.motion()

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
        self.data_newton = {}

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

        list_ls = [ "-", "--", "-." ]
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
            abs(self.max_vy if abs(self.max_vy) >= abs(max(data[1][3],key=abs)) else max(data[1][3],key=abs))

        self.min_vy = \
            abs(self.min_vy if abs(self.min_vy) >= abs(min(data[1][3],key=abs)) else min(data[1][3],key=abs))

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
        self._set_plot_parms(ax_vy, "time", "speed")

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
                [abs(i) for i in self.data_aristotel[_][1][3]],
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

    def plot_y_vy_all_aristotel_v_G(self, ax_y, ax_vy):

        for _, ls_ms in zip(self.data_aristotel.keys() - "c", self.ls_ms):

            ax_y.plot(
                self.data_aristotel[_][0],
                self.data_aristotel[_][1][1],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_aristotel["c"],
                label="A, {}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

            ax_vy.plot(
                self.data_aristotel[_][0],
                [abs(i) for i in self.data_aristotel[_][1][3]],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_aristotel["c"],
                label="A, {}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

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
        self._set_plot_parms(ax_vy, "time", "speed")

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
                [abs(i) for i in frame[_][1][3]],
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
        self._set_plot_parms(ax_vy, "time", "speed")

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
                [abs(i) for i in self.data_galilee[_][1][3]],
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

    def plot_y_vy_all_galilee_v_N(self, ax_y, ax_vy):

        for _, ls_ms in zip(self.data_galilee.keys() - "c", self.ls_ms):

            ax_y.plot(
                self.data_galilee[_][0],
                self.data_galilee[_][1][1],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_galilee["c"],
                label="G, {}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

            ax_vy.plot(
                self.data_galilee[_][0],
                [abs(i) for i in self.data_galilee[_][1][3]],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_galilee["c"],
                label="G, {}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

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
        self._set_plot_parms(ax_vy, "time", "speed")

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
                [abs(i) for i in frame[_][1][3]],
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

    def update_G_vs_A_data(self):

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

    def update_G_vs_A_plot(self, frame, ax_y, ax_vy):

        self._set_plot_parms(ax_y, "time", "height")
        self._set_plot_parms(ax_vy, "time", "speed")

        self.plot_y_vy_all_aristotel_v_G(ax_y, ax_vy)

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
                [abs(i) for i in frame[_][1][3]],
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

    def animate_all_galilee_vs_A(self):

        fig, ax_y, ax_vy = self._get_y_vy_plot()

        self._load_aristotel_all()
        self._load_galilee_all()

        ani = animation.FuncAnimation(
            fig=fig,
            func=self.update_G_vs_A_plot,
            fargs=(ax_y, ax_vy),
            frames=self.update_G_vs_A_data,
            interval=500,
            repeat=False
        )

        plt.show()

    def _load_newton_all(self):

        self.data_newton.clear()

        for _ in self.m:

            self.data_newton["m={}".format(_)] = self.N.get_data(m=_)

            self.data_newton["m={}".format(_)][0] = \
                self._reduce_points( self.data_newton["m={}".format(_)][0] )

            for ind, ydata in enumerate(self.data_newton["m={}".format(_)][1]):
                self.data_newton["m={}".format(_)][1][ind] = self._reduce_points( ydata )


        self.data_newton["c"] = "b"

    def plot_y_vy_all_newton(self):

        fig, ax_y, ax_vy = self._get_y_vy_plot()

        self._load_newton_all()

        self._set_plot_parms(ax_y, "time", "height")
        self._set_plot_parms(ax_vy, "time", "speed")

        for _, ls_ms in zip(self.data_newton.keys() - "c", self.ls_ms):

            self._set_max_min_y_vy_t(self.data_newton[_])

            ax_y.plot(
                self.data_newton[_][0],
                self.data_newton[_][1][1],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_newton["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

            ax_vy.plot(
                self.data_newton[_][0],
                [abs(i) for i in self.data_newton[_][1][3]],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_newton["c"],
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

    def update_N_data(self):

        lengths = []
        for _ in self.data_newton.keys() - "c":
            lengths.append(len(self.data_newton[_][0]) + 1)

        i = 1
        while i <= max(lengths):

            yield {
                mass: [
                    self.data_newton[mass][0][:i], [
                        ypoints[:i] for ypoints in self.data_newton[mass][1]
                    ]
                ] for mass in self.data_newton.keys() - "c"
            }

            i += 1

    def update_N_plot(self, frame, ax_y, ax_vy):

        self._set_plot_parms(ax_y, "time", "height")
        self._set_plot_parms(ax_vy, "time", "speed")

        for _, ls_ms in zip(frame, self.ls_ms):

            self._set_max_min_y_vy_t(self.data_newton[_])

            ax_y.plot(
                frame[_][0],
                frame[_][1][1],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_newton["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

            ax_vy.plot(
                frame[_][0],
                [abs(i) for i in frame[_][1][3]],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_newton["c"],
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

    def animate_all_newton(self):

        fig, ax_y, ax_vy = self._get_y_vy_plot()

        self._load_newton_all()

        ani = animation.FuncAnimation(
            fig=fig,
            func=self.update_N_plot,
            fargs=(ax_y, ax_vy),
            frames=self.update_N_data,
            interval=500,
            repeat=False
        )

        plt.show()

    def update_N_data(self):

        lengths = []
        for _ in self.data_newton.keys() - "c":
            lengths.append(len(self.data_newton[_][0]) + 1)

        i = 1
        while i <= max(lengths):

            yield {
                mass: [
                    self.data_newton[mass][0][:i], [
                        ypoints[:i] for ypoints in self.data_newton[mass][1]
                    ]
                ] for mass in self.data_newton.keys() - "c"
            }

            i += 1

    def update_N_vs_G_A_data(self):

        lengths = []
        for _ in self.data_newton.keys() - "c":
            lengths.append(len(self.data_newton[_][0]) + 1)

        i = 1
        while i <= max(lengths):

            yield {
                mass: [
                    self.data_newton[mass][0][:i], [
                        ypoints[:i] for ypoints in self.data_newton[mass][1]
                    ]
                ] for mass in self.data_newton.keys() - "c"
            }

            i += 1

    def update_N_vs_G_A_plot(self, frame, ax_y, ax_vy):

        self._set_plot_parms(ax_y, "time", "height")
        self._set_plot_parms(ax_vy, "time", "speed")

        self.plot_y_vy_all_aristotel_v_G(ax_y, ax_vy)
        self.plot_y_vy_all_galilee_v_N(ax_y, ax_vy)

        for _, ls_ms in zip(frame, self.ls_ms):

            self._set_max_min_y_vy_t(self.data_newton[_])

            ax_y.plot(
                frame[_][0],
                frame[_][1][1],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_newton["c"],
                label="{}".format(_),
                marker=ls_ms[1],
                markersize=8
            )

            ax_vy.plot(
                frame[_][0],
                [abs(i) for i in frame[_][1][3]],
                linestyle=ls_ms[0],
                linewidth=1.2,
                color=self.data_newton["c"],
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

    def animate_all_newton_vs_G_A(self):

        fig, ax_y, ax_vy = self._get_y_vy_plot()

        self._load_aristotel_all()
        self._load_galilee_all()
        self._load_newton_all()

        ani = animation.FuncAnimation(
            fig=fig,
            func=self.update_N_vs_G_A_plot,
            fargs=(ax_y, ax_vy),
            frames=self.update_N_vs_G_A_data,
            interval=500,
            repeat=False
        )

        plt.show()

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

        self.N = newton.orbit()

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

        self.data_newton_orbit = []

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
    def _get_polar_plot():

        style.use("seaborn-poster")

        gs = GridSpec(nrows=1, ncols=1)

        fig = plt.figure()
        fig.set_tight_layout(True)

        ax = fig.add_subplot(gs[0,0], polar=True)

        return fig, ax

    def _load_all_newton_orbit(self):

        self.data_newton_orbit.clear()

        l_phi0 = [ -_*1e-2 for _ in range(0,630,50) ]

        for _ in l_phi0:

            self.data_newton_orbit.append(self.N.get_k_period_data(k=2, phi0=_))

    def _load_all_gr_orbit(self):

        self.data_newton_orbit.clear()

        l_phi0 = [ -_*1e-2 for _ in range(0,630,50) ]

        for _ in l_phi0:

            self.data_newton_orbit.append(self.N.get_k_period_data(k=2, phi0=_))

    def plot_all_newton_orbit(self):

        fig, ax = self._get_polar_plot()

        self._load_all_newton_orbit()

        for _ in self.data_newton_orbit:
            ax.plot(_[0], _[1][0])

        plt.show()

    def update_newton_orbit_plot(self, frame, ax):

        ax.clear()

        ax.plot(
            frame[0][0],
            frame[0][1][0],
            linestyle="-",
            linewidth=2,
            color="b",
        )

        for _ in frame[1:]:

            ax.plot(
                _[0],
                _[1][0],
                linestyle="--",
                linewidth=2,
                color="r",
                alpha=0.4
            )

    def update_newton_orbit_data(self):

        i = 1

        while i <= len(self.data_newton_orbit):

            yield self.data_newton_orbit[:i]

            i += 1

    def animate_all_newton_orbit(self):

        fig, ax = self._get_polar_plot()
        fig2, ax2 = self._get_polar_plot()

        self._load_all_newton_orbit()

        ax2.plot(
            self.data_newton_orbit[0][0],
            self.data_newton_orbit[0][1][0],
            linestyle="-",
            linewidth=2,
            color="b",
        )

        ani = animation.FuncAnimation(
            fig=fig,
            func=self.update_newton_orbit_plot,
            fargs=(ax,),
            frames=self.update_newton_orbit_data,
            interval=500,
            repeat=True
        )

        plt.show(block=True)

if __name__ == "__main__":

    print("\n Hello world \n")

