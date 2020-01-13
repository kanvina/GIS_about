import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from osgeo import gdal
import ospybook as pb
import pandas as pd

def read_tif(path):

    ds = gdal.Open(path)
    band = ds.GetRasterBand(1)#DEM数据只有一种波段
    # ov_band=band.GetOverview(band.GetOverviewCount()-3)
    # data=ov_band.ReadAsArray()
    data = band.ReadAsArray()#data即为dem图像像元的数值矩阵
    return data,ds,band

if __name__ =="__main__":

    data, ds, band=read_tif('data/gas2_Extract.tif')

    #计算边界坐标
    geotransform = ds.GetGeoTransform()
    minx = geotransform[0]
    maxy = geotransform[3]
    maxx = minx + band.XSize * geotransform[1]
    miny = maxy + band.YSize * geotransform[5]
    x = np.arange(minx, maxx, geotransform[1])
    y = np.arange(maxy, miny, geotransform[5])
    x, y = np.meshgrid(x[:band.XSize], y[:band.YSize])

    '''
    三维显示
    '''
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # plt.axis('equal')
    ax.plot_surface(x, y, data, cmap='gist_earth', lw=0)
    #ax.plot_wireframe(x, y, data)
    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()

    '''
    输出至csv
    '''
    # pd.DataFrame(data).to_csv('gas2.csv',index=0,header=0)


