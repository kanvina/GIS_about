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


class well_grid():

    def __init__(self):

        self.cell_len = 100
        self.center_location = [50, 50]
        self.x_zoom = 1
        self.y_zoom = 1
        self.theta = 60
        self.gamma = 15
        self.Delta_x = 50
        self.Delta_y = 50



    def init_five_cell(self):

        x_cell_len=self.cell_len*self.x_zoom
        y_cell_len=self.cell_len*self.y_zoom

        angle_a= (np.arctan( (np.cos(self.theta*np.pi/180)+(y_cell_len/x_cell_len) )/np.sin(self.theta*np.pi/180)))*180/np.pi
        angle_b=180-self.theta-angle_a
        angle_c=angle_a-90+self.theta-self.gamma
        diagonal_line_len = y_cell_len*np.sin(angle_a*np.pi/180)+x_cell_len*np.sin(angle_b*np.pi/180)


        point_LD_location=[self.center_location[0]-(self.cell_len/2)+self.Delta_x,self.center_location[1]-(self.cell_len/2)+self.Delta_y]
        point_LT_location=[y_cell_len*np.cos((self.theta-self.gamma)*np.pi/180)+point_LD_location[0],y_cell_len*np.sin((self.theta-self.gamma)*np.pi/180)+point_LD_location[1]]

        point_RT_location=[ diagonal_line_len*np.cos(angle_c*np.pi/180)+point_LD_location[0],diagonal_line_len*np.sin(angle_c*np.pi/180)+point_LD_location[1]  ]
        point_RD_location=[ x_cell_len*np.cos(self.gamma*np.pi/180)+point_LD_location[0],point_LD_location[1]-x_cell_len*np.sin(self.gamma*np.pi/180) ]
        point_center_location=[ 0.5*diagonal_line_len*np.cos((angle_a+self.theta-self.gamma-90)*np.pi/180)+point_LD_location[0],0.5*diagonal_line_len*np.sin((angle_a+self.theta-self.gamma-90)*np.pi/180)+point_LD_location[1] ]
        return [point_LD_location,point_LT_location,point_RT_location,point_RD_location,point_center_location]



def draw_scatter(points):
    point_LD_location=points[0]
    point_LT_location=points[1]
    point_RT_location=points[2]
    point_RD_location=points[3]
    point_center_location=points[4]
    plt.scatter(point_LD_location[0], point_LD_location[1], marker='o', color='red', s=40, label='First')
    plt.scatter(point_LT_location[0], point_LT_location[1], marker='o', color='red', s=40, label='First')
    plt.scatter(point_RT_location[0], point_RT_location[1], marker='o', color='red', s=40, label='First')
    plt.scatter(point_RD_location[0], point_RD_location[1], marker='o', color='red', s=40, label='First')
    plt.scatter(point_center_location[0], point_center_location[1], marker='x', color='red', s=40, label='First')

    plt.show()

if __name__=="__main__":

    grid=well_grid()
    points=grid.init_five_cell()
    draw_scatter(points)


