'''
create by WYD
2019 10 25
井网构造实验
1- 构造原始井网单元
2- 横向与纵向缩放，因子：x_zoom,y_zoom
3- 横向与纵向平移：因子：Delta_x,Delta_y
4- 井网单元形状改变，因子：夹角theta
5- 井网单元旋转，因子：gamma
'''

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from matplotlib.pyplot import MultipleLocator


def init_five_cell(cell_len,center_location,x_zoom,y_zoom,theta,gamma,Delta_x,Delta_y):
    '''
    初始化五点式井组单元
    :param cell_len: 井组单元边长
    :param center_location: 井组中心点位置[x,y]
    :return:
    '''

    x_cell_len=cell_len*x_zoom
    y_cell_len=cell_len*y_zoom


    point_LD_location=[center_location[0]-(cell_len/2)+Delta_x,center_location[1]-(cell_len/2)+Delta_y]
    point_LT_location=[y_cell_len*np.cos((theta-gamma)*np.pi/180)+point_LD_location[0],y_cell_len*np.sin((theta-gamma)*np.pi/180)+point_LD_location[1]]


    angle_a= (np.arctan( (np.cos(theta*np.pi/180)+(y_cell_len/x_cell_len) )/np.sin(theta*np.pi/180)))*180/np.pi
    angle_b=180-theta-angle_a
    angle_c=angle_a-90+theta-gamma
    diagonal_line_len = y_cell_len*np.sin(angle_a*np.pi/180)+x_cell_len*np.sin(angle_b*np.pi/180)

    point_RT_location=[ diagonal_line_len*np.cos(angle_c*np.pi/180)+point_LD_location[0],diagonal_line_len*np.sin(angle_c*np.pi/180)+point_LD_location[1]  ]
    point_RD_location=[ x_cell_len*np.cos(gamma*np.pi/180)+point_LD_location[0],point_LD_location[1]-x_cell_len*np.sin(gamma*np.pi/180) ]

    print(point_LD_location)
    print(point_LT_location)
    print(point_RT_location)

    print((point_LD_location[0]-point_LT_location[0])**2+(point_LD_location[1]-point_LT_location[1])**2)
    print((point_RT_location[0] - point_LT_location[0]) ** 2 + (point_RT_location[1] - point_LT_location[1]) ** 2)

    plt.scatter(point_LD_location[0], point_LD_location[1], marker='x', color='red', s=40, label='First')
    plt.scatter(point_LT_location[0], point_LT_location[1], marker='o', color='red', s=40, label='First')
    plt.scatter(point_RT_location[0], point_RT_location[1], marker='x', color='red', s=40, label='First')
    plt.scatter(point_RD_location[0], point_RD_location[1], marker='o', color='red', s=40, label='First')

    x_major_locator = MultipleLocator(10)
    # 把x轴的刻度间隔设置为1，并存在变量里
    y_major_locator = MultipleLocator(10)
    # 把y轴的刻度间隔设置为10，并存在变量里
    ax = plt.gca()
    # ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    # 把x轴的主刻度设置为1的倍数
    ax.yaxis.set_major_locator(y_major_locator)

    plt.show()


if __name__=="__main__":

    cell_len=100
    center_location=[50,50]
    x_zoom=1
    y_zoom=1
    theta=60
    gamma=15
    Delta_x=50
    Delta_y=50

    init_five_cell(cell_len, center_location, x_zoom, y_zoom, theta, gamma, Delta_x, Delta_y)
