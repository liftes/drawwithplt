from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib.patches import ConnectionPatch
import matplotlib.ticker as mtick
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import matplotlib.gridspec as gridspec

import scipy.interpolate as spi
from scipy.interpolate import splrep,splev

from matplotlib import offsetbox, rcParams
from matplotlib.colors import ListedColormap,LinearSegmentedColormap

# ---------------------------------------------------------------

FONTSIZE = 12
AXISSIZE = 14
DPI_SAVE = 1000
config = {
    "font.family": 'serif',
    "font.size": FONTSIZE,
    "xtick.labelsize":AXISSIZE,
    "ytick.labelsize":AXISSIZE,
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
    # "font.serif": ['Microsoft YaHei'],
}
rcParams.update(config)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.unicode_minus'] = False


# 提供修改默认参数的快捷接口
def UpdataFontSize(axissize,fontsize):
    config = {
        "font.size": fontsize,
        "xtick.labelsize":axissize,
        "ytick.labelsize":axissize,
    }
    rcParams.update(config)

def UpdataConfig(config):
    rcParams.update(config)


def SaveFig(flag, path, filepath="figure/"):
    # 保存图片
    if flag:
        if not os.path.isdir(filepath):
            os.mkdir(filepath)
        plt.savefig(filepath+path, bbox_inches='tight', dpi=DPI_SAVE)
    else:
        pass


def TestColorList(clist):
    # 显示色卡
    num = len(clist)
    gs = SetSubFig_GS(3, num+int(num/2), (6, 4))
    plt.subplots_adjust(wspace=0.3, hspace=0.2)
    for i, color in enumerate(clist):
        if type(color) != str:
            color = tuple([int(i*255) for i in color])
        img = Image.new('RGB', (10, 10), color)
        ax = plt.subplot(gs[0, i])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis("off")
        # ax.set_title(color)
        ax.imshow(img)
    ax = plt.subplot(gs[1:, :num])
    xvalue = np.arange(0, 2*np.pi, 0.1)
    for i, color in enumerate(clist):
        ax.plot(xvalue, np.sin((i+0.5)*xvalue), "-", color=color, label="%d" % i)
    ax.grid(":",alpha=0.3)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.legend(loc = 4)

    ax = plt.subplot(gs[:, num:])
    # ax.barh(range(num),range(1+num,1,-1),color=clist)
    xvalue = np.arange(0, 0.5, 0.05)
    for i, color in enumerate(clist):
        ax.plot(xvalue, np.exp((i+0.5)*xvalue), "s", color=color,
                markerfacecolor='none', label="%d" % i)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc = 2)
    plt.show()


def SetColor(string, array):
    # 用户应用现有颜色，如“tab10”
    color_list = plt.cm.get_cmap(string)(array)
    TestColorList(color_list)
    return color_list


def SetColorSelf(colorlist,N,NS=5):
    # 用户自定义简便颜色，并提供渐变分级
    newcmp = LinearSegmentedColormap.from_list("mylist",colorlist,N)
    colorlist = plt.cm.get_cmap(newcmp)(np.linspace(0,1,NS))
    return newcmp,colorlist


def SetSubFig(xnum, ynum, size):
    # 规范子图（各图大小一致）
    fig, ax = plt.subplots(xnum, ynum, figsize=size)
    if xnum+ynum > 2:
        axes = ax.flatten()
        return fig, axes
    else:
        return fig, ax

def SetSubFig_GS(xnum, ynum, size):
    # 返回子图网格，自由度更高，使用需要plt.subplot
    plt.figure(figsize=size)
    gs = gridspec.GridSpec(xnum, ynum)
    return gs


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


def snsFix(xlist: np.array, ylist: np.array, z: np.array, xl={}, yl={}, zl={}, normalZero=True, contour=False, contournum=5, contourstyle='--', contourcolor="w", contourfmt='%.1f', ax=False, cbar=True, mask=np.array([])):
    # normalZero:是否反转x轴数据以使得左下角为零点
    # xl、yl中包含：name：标签名，step：采样步长，start：采样开始点，end：采样结束点，angle：标签旋转角度；zl中包含：name：标签名，color：字符串，cmap类型，min：最小值，max：最大值；
    if normalZero:
        z = z[::-1, :]
        xlist = xlist[::-1]

    if mask.shape[0] == 0:
        mask = np.zeros_like(z,dtype=np.bool)

    xl, yl, zl = initDict(xlist, ylist, z, xl, yl, zl)

    if ax:
        ax = sns.heatmap(z, vmax=zl["max"], vmin=zl["min"] , cmap=zl["color"],
                     ax = ax, cbar=False, mask=mask)
    else:
        ax = sns.heatmap(z, vmax=zl["max"], vmin=zl["min"] , cmap=zl["color"],
                     cbar=False, mask=mask)

    # 绘制颜色条
    if cbar:
        cbar = ax.figure.colorbar(ax.collections[0])
        cbar.set_label(zl["name"])

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
    return ax, cbar


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
    # 样条差值拟合
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


def polyfit(x_arr,y_arr,step=1000,order=3,delete=1,turn=False,c="gray",label="",ax=plt,x=np.array([]),NeedPlot=True):
    # 多项式拟合
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
    if NeedPlot:
        if turn:
            ax.plot(y,x,color=c,label=label)
        else:
            ax.plot(x,y,color=c,label=label)
    return p1


# 自定义色卡区
CSL_4_1 = ["#384259","#f73859","#7ac7c4","#f07b3f"]
CSL_4_2 = ["#2a557f","#44bd9d","#f04f75","#fdcd6e"]
CSL_2_1 = ["#b7282e","#0f1021"]
CSMap_1 = SetColorSelf(["k","#b7282e","w"],N=1000)