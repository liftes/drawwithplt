from matplotlib.axes import Axes
import pylab
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib.patches import ConnectionPatch
import matplotlib.ticker as mtick
from mpl_toolkits.mplot3d import Axes3D

import scipy.interpolate as spi
from scipy.interpolate import splrep,splev

from matplotlib import offsetbox, rcParams

config = {
    "font.family": 'serif',
    "font.size": 12,
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.unicode_minus'] = False

def SaveFig(flag, path, filepath="figure/"):
    if flag:
        if not os.path.isdir(filepath):
            os.mkdir(filepath)
        plt.savefig(filepath+path, bbox_inches='tight', dpi=600)
    else:
        pass


def SetColor(string, array):
    color_list = plt.cm.get_cmap(string)(array)
    return color_list


def SetSubFig(xnum, ynum, size):
    fig, ax = plt.subplots(xnum, ynum, figsize=size)
    if xnum+ynum > 2:
        axes = ax.flatten()
        return fig, axes
    else:
        return fig, ax


def Zone_and_linked(ax, axins, zone_left, zone_right, x, y, linked='bottom',
                    x_ratio=0.05, y_ratio=0.05):
    """缩放内嵌图形，并且进行连线
    ax:         调用plt.subplots返回的画布。例如： fig,ax = plt.subplots(1,1)
    axins:      内嵌图的画布。 例如 axins = ax.inset_axes((0.4,0.1,0.4,0.3))
    zone_left:  要放大区域的横坐标左端点
    zone_right: 要放大区域的横坐标右端点
    x:          X轴标签
    y:          列表，所有y值
    linked:     进行连线的位置，{'bottom','top','left','right'}
    x_ratio:    X轴缩放比例
    y_ratio:    Y轴缩放比例
    """
    xlim_left = x[zone_left]-(x[zone_right]-x[zone_left])*x_ratio
    xlim_right = x[zone_right]+(x[zone_right]-x[zone_left])*x_ratio

    y_data = np.hstack([yi[zone_left:zone_right] for yi in y])
    ylim_bottom = np.min(y_data)-(np.max(y_data)-np.min(y_data))*y_ratio
    ylim_top = np.max(y_data)+(np.max(y_data)-np.min(y_data))*y_ratio

    axins.set_xlim(xlim_left, xlim_right)
    axins.set_ylim(ylim_bottom, ylim_top)

    ax.plot([xlim_left, xlim_right, xlim_right, xlim_left, xlim_left],
            [ylim_bottom, ylim_bottom, ylim_top, ylim_top, ylim_bottom], "black")

    if linked == 'bottom':
        xyA_1, xyB_1 = (xlim_left, ylim_top), (xlim_left, ylim_bottom)
        xyA_2, xyB_2 = (xlim_right, ylim_top), (xlim_right, ylim_bottom)
    elif linked == 'top':
        xyA_1, xyB_1 = (xlim_left, ylim_bottom), (xlim_left, ylim_top)
        xyA_2, xyB_2 = (xlim_right, ylim_bottom), (xlim_right, ylim_top)
    elif linked == 'left':
        xyA_1, xyB_1 = (xlim_right, ylim_top), (xlim_left, ylim_top)
        xyA_2, xyB_2 = (xlim_right, ylim_bottom), (xlim_left, ylim_bottom)
    elif linked == 'right':
        xyA_1, xyB_1 = (xlim_left, ylim_top), (xlim_right, ylim_top)
        xyA_2, xyB_2 = (xlim_left, ylim_bottom), (xlim_right, ylim_bottom)

    con = ConnectionPatch(xyA=xyA_1, xyB=xyB_1, coordsA="data",
                          coordsB="data", axesA=axins, axesB=ax)
    axins.add_artist(con)
    con = ConnectionPatch(xyA=xyA_2, xyB=xyB_2, coordsA="data",
                          coordsB="data", axesA=axins, axesB=ax)
    axins.add_artist(con)


def initDict(xlist, ylist, z, xl, yl, zl):
    xl.setdefault("name", "x")
    xl.setdefault("step", 5)
    xl.setdefault("start", 0)
    xl.setdefault("end", xlist.shape[0])
    xl.setdefault("angle", 0)
    xl.setdefault("fmt", "%.2f")

    yl.setdefault("name", "y")
    yl.setdefault("step", 5)
    yl.setdefault("start", 0)
    yl.setdefault("end", ylist.shape[0])
    yl.setdefault("angle", 0)
    yl.setdefault("fmt", "%.2f")

    zl.setdefault("name", "z")
    zl.setdefault("color", "YlGnBu_r")
    zl.setdefault("min", np.min(z))
    zl.setdefault("max", np.max(z))
    zl.setdefault("step", 5)
    zl.setdefault("vx", 45)
    zl.setdefault("vz", 15)
    zl.setdefault("a", 1)
    return xl, yl, zl


def snsFix(xlist: np.array, ylist: np.array, z: np.array, xl={}, yl={}, zl={}, normalZero=True, contour=False, contournum=5, contourstyle='--', contourcolor="w", contourfmt='%.1f', ax=False, cbar=True):
    # normalZero:是否反转x轴数据以使得左下角为零点
    # xl、yl中包含：name：标签名，step：采样步长，start：采样开始点，end：采样结束点，angle：标签旋转角度；zl中包含：name：标签名，color：字符串，cmap类型，min：最小值，max：最大值；
    if normalZero:
        z = z[::-1, :]
        xlist = xlist[::-1]

    xl, yl, zl = initDict(xlist, ylist, z, xl, yl, zl)

    if ax:
        ax = sns.heatmap(z, vmax=zl["max"], vmin=zl["min"] , cmap=zl["color"],
                     cbar_kws={'label': zl["name"]}, ax = ax, cbar=cbar)
    else:
        ax = sns.heatmap(z, vmax=zl["max"], vmin=zl["min"] , cmap=zl["color"],
                     cbar_kws={'label': zl["name"]}, cbar=cbar)

    # 是否绘制等高线
    if contour:
        X, Y = np.meshgrid(range(ylist.shape[0]), range(xlist.shape[0]))
        c = ax.contour(X, Y, z, contournum, colors=contourcolor,
                       linestyles=contourstyle)
        plt.clabel(c, inline=True, fmt=contourfmt)

    ax.set_yticks(np.arange(xl["start"], xl["end"], xl["step"]))
    ax.set_yticklabels([xl["fmt"] % i for i in xlist.take(
                range(xl["start"], xl["end"], xl["step"]))],
               rotation=xl["angle"])
    ax.set_ylabel(xl["name"])
    ax.set_xticks(np.arange(yl["start"], yl["end"], yl["step"]))
    ax.set_xticklabels([yl["fmt"] % i for i in ylist.take(
                range(yl["start"], yl["end"], yl["step"]))],
               rotation=yl["angle"])
    ax.set_xlabel(yl["name"])
    ax.tick_params(direction="out")
    return ax


def Plot3DFix(figure, xlist: np.array, ylist: np.array, z: np.array, xl={}, yl={}, zl={}, contour=False, contournum=5, contourstyle='--', continuefmt='%.1f'):
    # 参数字典初始化
    xl, yl, zl = initDict(xlist, ylist, z, xl, yl, zl)
    ax = Axes3D(figure)
    X, Y = np.meshgrid(ylist, xlist)
    surf = ax.plot_surface(
        X, Y, z, cmap=zl["color"], lw=3, rstride=1, cstride=1, vmax=zl["max"], vmin=zl["min"], alpha=zl["a"])

    if contour:
        # ax.contour(X, Y, z, contournum, colors="k", zdir ='z',
        #                 linestyles=contourstyle)
        c = ax.contour(X, Y, z, contournum, cmap=zl["color"],
                       linestyles=contourstyle, offset=zl["min"])
        plt.clabel(c, inline=True, fmt=continuefmt)
    ax.set_zlim(zl["min"], zl["max"])
    ax.view_init(elev=zl["vx"], azim=zl["vz"])
    figure.colorbar(surf, shrink=0.7, aspect=20)
    ax.set_xlabel(xl["name"])
    ax.set_ylabel(yl["name"])
    ax.set_zlabel(zl["name"])
    return figure, ax


def spline(x_arr,y_arr,step=1000,order=3,delete=1,turn=False,c="gray",label=""):
    if turn:
        tmp = x_arr
        x_arr = y_arr
        y_arr = tmp
    x_arr = np.array(x_arr)
    y_arr = np.array(y_arr)
    x_arr = x_arr.take(range(1, x_arr.shape[0], delete))
    y_arr = y_arr.take(range(1, y_arr.shape[0], delete))
    tk = splrep(x_arr, y_arr, k=order) # Returns the knots and coefficents
    ### Evaluate the spline using the knots and coefficents on the domian x
    x = np.linspace(np.min(x_arr),np.max(x_arr) , step) # new x-grid
    y = splev(x, tk, der=0)
    ### Plot
    if turn:
        plt.plot(y,x,color=c,label=label)
    else:
        plt.plot(x,y,color=c,label=label)


def polyfit(x_arr,y_arr,step=1000,order=3,delete=1,turn=False,c="gray",label="",ax=plt,x=np.array([])):
    if turn:
        tmp = x_arr
        x_arr = y_arr
        y_arr = tmp
    x_arr = np.array(x_arr)
    y_arr = np.array(y_arr)
    x_arr = x_arr.take(range(1, x_arr.shape[0], delete))
    y_arr = y_arr.take(range(1, y_arr.shape[0], delete))
    if x.shape[0] == 0:
        x = np.linspace(np.min(x_arr),np.max(x_arr) , step) # new x-grid
    z1 = np.polyfit(x_arr,y_arr,order)
    p1 = np.poly1d(z1)
    y = p1(x)
    if turn:
        ax.plot(y,x,color=c,label=label)
    else:
        ax.plot(x,y,color=c,label=label)
    return p1