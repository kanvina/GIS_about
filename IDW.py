'''
create by WYD
2019 9 21
IDW空间插值底层算法实现
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#从xls提取数据
def get_array_excel(path):
    data_arr=np.array(pd.read_excel(path))
    return data_arr
#获取数据范围
def get_range(data_arr):
    min_x=np.min(data_arr[:,0])
    max_x=np.max(data_arr[:,0])

    min_y = np.min(data_arr[:, 1])
    max_y = np.max(data_arr[:, 1])
    data_range=[min_x,max_x,min_y,max_y]
    return data_range
#网格范围
def get_grid_size(range,cell_len):
    row_size= int((range[3]-range[2])/cell_len)
    column_size= int((range[1]-range[0])/cell_len)
    return row_size,column_size
#获取中心点坐标
def get_cell_center(row_i,column_i,cell_len,data_range):
    x_center=data_range[0]+(column_i*cell_len)+(cell_len/2)
    y_center=data_range[3]-(row_i*cell_len)-(cell_len/2)
    center_loction=[x_center,y_center]
    return center_loction
#


def get_z(data_arr,center_loction,p,n):
    distance_list =[]
    for point_x_y_z in data_arr:
        point_xi=point_x_y_z[0]
        point_yi=point_x_y_z[1]
        distance=((point_xi-center_loction[0])**2+(point_yi-center_loction[1])**2)**0.5
        distance_list.append(distance)
    wi_num=0
    wi_list= []
    distance_list=np.array(distance_list)
    distance_sort_list=np.sort(distance_list)[0:12]
    distance_idx_list=np.argsort(distance_list)[0:12]


    for distance_point in distance_sort_list:
        wi_point=distance_point**-p
        wi_num=wi_num+wi_point
        wi_list.append(wi_point)
    z_i_sum=0
    for i in range(len(wi_list)):
        idx=distance_idx_list[i]
        wi_list[i]=wi_list[i]/wi_num
        z_i=data_arr[idx,n]*wi_list[i]
        z_i_sum=z_i_sum+z_i

    return z_i_sum

def run_IDW(data_arr, row_size, column_size,cell_len,data_range,p,n):
    data_IDW=np.zeros((row_size,column_size))
    for index in range(row_size*column_size):
        row_i=int(np.floor(index/column_size))
        column_i=index%column_size
        center_loction=get_cell_center(row_i,column_i,cell_len,data_range)
        z=get_z(data_arr,center_loction,p,n)
        data_IDW[row_i,column_i]=z
    return data_IDW

def main_IDW(path_point_xls,cell_len,p,n):
    '''

    :param path_point_xls:
    :param cell_len:
    :param p:
    :param n: 待插值列数
    :return:
    '''
    data_arr = get_array_excel(path_point_xls)
    data_range = get_range(data_arr)
    row_size, column_size = get_grid_size(data_range, cell_len)
    data_IDW = run_IDW(data_arr, row_size, column_size, cell_len, data_range, p,n)
    return data_IDW,data_range

if __name__ =="__main__":

    path_point_xls='data/data_points.xls'
    cell_len = 10
    p=2#。幂指数
    n=2#待插值列数

    data_IDW,data_range=main_IDW(path_point_xls, cell_len, p,n)
    print(data_IDW)
    print(data_range)

    pd.DataFrame(data_IDW).to_csv('data/data_IDW.csv',index=0)

    plt.imshow(data_IDW)
    plt.show()





