from matplotlib import pyplot
import numpy as np

import nir.constants as const


def plot_plr(result_plr, result_approximation, g_interval):
    pyplot.clf()
    pyplot.ylim(10 ** -7, 10 ** 0)
    pyplot.xticks(np.arange(0, 1.1, 0.1))
    pyplot.xlabel("G")
    pyplot.ylabel("Package Loss Rate (PLR)")
    for polynom_name, _ in const.polynoms.items():
        pyplot.semilogy(g_interval, result_plr.get(polynom_name), label=polynom_name)
        pyplot.semilogy(g_interval, result_approximation.get(polynom_name), "--",
                        label="{} approx".format(polynom_name))
    pyplot.legend()
    pyplot.savefig("plr.png")
    pyplot.clf()


def plot_throughput(result_throughput, result_approximation, g_interval):
    pyplot.clf()
    pyplot.ylim(0, 1)
    pyplot.xticks(np.arange(0, 1.1, 0.1))
    pyplot.xlabel("G")
    pyplot.ylabel("Throughput")
    for polynom_name, _ in const.polynoms.items():
        pyplot.plot(g_interval, result_throughput.get(polynom_name), label=polynom_name)
        pyplot.plot(g_interval, result_approximation.get(polynom_name), "--",
                    label="{} approx".format(polynom_name))
    pyplot.legend()
    pyplot.savefig("throughput.png")
