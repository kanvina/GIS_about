'''
create by WYD
2019 9 21
栅格数据提取等值线算法实现
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_data_node_array(data_array):
    data_size=np.shape(data_array)

    data_add_up=np.array([data_array[0,:]])
    data_add_low=np.array([data_array[(data_size[0]-1),:]])
    data_array=np.concatenate((data_add_up,data_array,data_add_low),axis=0)

    data_add_left=np.array([data_array[:,0]]).transpose()
    data_add_right=np.array([data_array[:,data_size[1]-1]]).transpose()
    data_array_add=np.concatenate((data_add_left,data_array,data_add_right),axis=1)

    return data_array_add

def get_horizontal_line_info(data_array_add,target_value,data_tif_info):
    dict_horizontal_line={}
    r_xize,c_size=np.shape(data_array_add)
    c_size=c_size-1

    for i in range(r_xize*c_size):
        rate=-1
        row_i=int(np.floor(i/c_size))
        column_i = i % c_size
        data_value=[data_array_add[row_i,column_i],data_array_add[row_i,column_i+1]]

        location_list=[]

        if (data_value[0]-target_value) * (data_value[1]-target_value)<=0:
            rate=abs(data_value[0]-target_value)/abs(data_value[1]-data_value[0])
            cell_len=data_tif_info['cell_len']

            min_x=data_tif_info['min_x']-cell_len
            min_y=data_tif_info['min_y']-cell_len

            max_x=data_tif_info['max_x']+cell_len
            max_y=data_tif_info['max_y']+cell_len
            location_x=min_x+(cell_len/2)+column_i*cell_len+rate*cell_len
            location_y=max_y-(cell_len/2)-row_i*cell_len
            location_list.append(location_x)
            location_list.append(location_y)


        dict_horizontal_line['h%s_%s'%(row_i,column_i)]=[[row_i,column_i],data_value,False,location_list]

    return dict_horizontal_line

def get_vertical_line_info(data_array_add,target_value,data_tif_info):
    dict_vertical_line={}
    r_xize,c_size=np.shape(data_array_add)
    r_xize=r_xize-1

    for i in range(r_xize*c_size):
        rate=-1
        row_i=int(np.floor(i/c_size))
        column_i = i % c_size
        location_list = []
        data_value=[data_array_add[row_i,column_i],data_array_add[row_i+1,column_i]]

        if (data_value[0] - target_value) * (data_value[1] - target_value) <= 0:
            rate=abs(data_value[0]-target_value)/abs(data_value[1]-data_value[0])
            cell_len = data_tif_info['cell_len']

            min_x = data_tif_info['min_x'] - cell_len
            min_y = data_tif_info['min_y'] - cell_len

            max_x = data_tif_info['max_x'] + cell_len
            max_y = data_tif_info['max_y'] + cell_len

            location_x=min_x+(cell_len/2)+column_i*cell_len
            location_y=max_y-(cell_len/2)-row_i*cell_len-rate*cell_len

            location_list.append(location_x)
            location_list.append(location_y)


        dict_vertical_line['v%s_%s'%(row_i,column_i)]=[[row_i,column_i],data_value,False,location_list]
    return dict_vertical_line

def get_next(point_name,dict_all_point,last_point):
    all_close_points = []

    if str(point_name).find('h') !=-1:
        taget_point_all_info=dict_all_point[point_name]
        r_c=taget_point_all_info[0]
        r=r_c[0]
        c=r_c[1]
        location_x_y=taget_point_all_info[1]

        if 'h%s_%s'%(r-1,c) in dict_all_point and 'h%s_%s'%(r-1,c)  != last_point:

            location_a=dict_all_point['h%s_%s'%(r-1,c)][1]
            distance_a=((location_x_y[0]-location_a[0])**2+(location_x_y[1]-location_a[1])**2)**0.5
            all_close_points.append(['h%s_%s' % (r - 1, c),distance_a])

        if 'h%s_%s'%(r+1,c) in dict_all_point and 'h%s_%s'%(r+1,c) !=  last_point :
            location_b=dict_all_point['h%s_%s'%(r+1,c)][1]
            distance_b=((location_x_y[0]-location_b[0])**2+(location_x_y[1]-location_b[1])**2)**0.5
            all_close_points.append(['h%s_%s' % (r + 1, c),distance_b])

        if 'v%s_%s'%(r-1,c) in dict_all_point and 'v%s_%s'%(r-1,c)  !=  last_point  :
            location_c=dict_all_point['v%s_%s'%(r-1,c)][1]
            distance_c=((location_x_y[0]-location_c[0])**2+(location_x_y[1]-location_c[1])**2)**0.5
            all_close_points.append(['v%s_%s'%(r-1,c), distance_c])

        if 'v%s_%s'%(r,c) in dict_all_point and 'v%s_%s'%(r,c) != last_point :
            location_d=dict_all_point['v%s_%s'%(r,c)][1]
            distance_d=((location_x_y[0]-location_d[0])**2+(location_x_y[1]-location_d[1])**2)**0.5
            all_close_points.append(['v%s_%s'%(r,c), distance_d])

        if 'v%s_%s' % (r-1, c+1) in dict_all_point and 'v%s_%s' % (r-1, c+1) != last_point :
            location_e = dict_all_point['v%s_%s' % (r-1, c+1)][1]
            distance_e = ((location_x_y[0] - location_e[0]) ** 2 + (location_x_y[1] - location_e[1]) ** 2) ** 0.5
            all_close_points.append(['v%s_%s' % (r - 1, c+1), distance_e])

        if 'v%s_%s' % (r, c+1) in dict_all_point and  'v%s_%s' % (r, c+1) != last_point:
            location_f = dict_all_point['v%s_%s' % (r, c+1)][1]
            distance_f = ((location_x_y[0] - location_f[0]) ** 2 + (location_x_y[1] - location_f[1]) ** 2) ** 0.5
            all_close_points.append(['v%s_%s' % (r , c+1), distance_f])

        all_close_points=np.array(all_close_points)
        distance_min=np.min(np.array(all_close_points[:,1],dtype=float))
        index_min=np.argwhere(np.array(all_close_points[:,1],dtype=float)==distance_min)[0][0]
        next_point=all_close_points[index_min,0]
        dict_all_point[next_point][2]=True


    if str(point_name).find('v') != -1:

        taget_point_all_info=dict_all_point[point_name]
        r_c=taget_point_all_info[0]
        r=r_c[0]
        c=r_c[1]
        location_x_y=taget_point_all_info[1]

        if 'v%s_%s'%(r,c-1) in dict_all_point and   'v%s_%s'%(r,c-1) != last_point :
            location_a=dict_all_point[ 'v%s_%s'%(r,c-1)][1]
            distance_a=((location_x_y[0]-location_a[0])**2+(location_x_y[1]-location_a[1])**2)**0.5
            all_close_points.append(['v%s_%s' % (r ,c-1),distance_a])

        if 'v%s_%s'%(r,c+1) in dict_all_point and  'v%s_%s'%(r,c+1)!= last_point  :
            location_b=dict_all_point[ 'v%s_%s'%(r,c+1)][1]
            distance_b=((location_x_y[0]-location_b[0])**2+(location_x_y[1]-location_b[1])**2)**0.5
            all_close_points.append(['v%s_%s' % (r ,c+1),distance_b])

        if 'h%s_%s'%(r,c-1) in dict_all_point and 'h%s_%s'%(r,c-1) != last_point  :
            location_c=dict_all_point[ 'h%s_%s'%(r,c-1)][1]
            distance_c=((location_x_y[0]-location_c[0])**2+(location_x_y[1]-location_c[1])**2)**0.5
            all_close_points.append(['h%s_%s' % (r ,c-1),distance_c])

        if 'h%s_%s'%(r+1,c-1) in dict_all_point and  'h%s_%s'%(r+1,c-1) != last_point :
            location_d=dict_all_point[ 'h%s_%s'%(r+1,c-1)][1]
            distance_d=((location_x_y[0]-location_d[0])**2+(location_x_y[1]-location_d[1])**2)**0.5
            all_close_points.append(['h%s_%s' % (r+1 ,c-1),distance_d])

        if 'h%s_%s'%(r,c) in dict_all_point and  'h%s_%s'%(r,c) != last_point :
            location_e=dict_all_point[ 'h%s_%s'%(r,c)][1]
            distance_e=((location_x_y[0]-location_e[0])**2+(location_x_y[1]-location_e[1])**2)**0.5
            all_close_points.append(['h%s_%s' % (r ,c),distance_e])

        if 'h%s_%s'%(r+1,c) in dict_all_point and 'h%s_%s'%(r+1,c) != last_point  :
            location_f=dict_all_point[ 'h%s_%s'%(r+1,c)][1]
            distance_f=((location_x_y[0]-location_f[0])**2+(location_x_y[1]-location_f[1])**2)**0.5
            all_close_points.append(['h%s_%s' % (r+1 ,c),distance_f])

        all_close_points = np.array(all_close_points)
        distance_min = np.min(np.array(all_close_points[:, 1], dtype=float))
        index_min = np.argwhere(np.array(all_close_points[:, 1], dtype=float) == distance_min)[0][0]
        next_point = all_close_points[index_min, 0]
        dict_all_point[next_point][2] = True

    return next_point

def draw_contour(location_list):
    x_list=np.array(location_list)[:,0]
    y_list=np.array(location_list)[:,1]
    plt.plot(x_list, y_list)
    plt.xlim(0, 1000)
    plt.ylim(0, 1000)
    plt.show()


if __name__=="__main__":

    target_value=350

    data_tif_info=\
        {
            'min_x':0,
            'max_x':1000,
            'min_y':0,
            'max_y':1000,
            'cell_len':10
        }


    data_array=np.array(pd.read_excel('data_out/data_IDW.xls'))
    data_array_add=get_data_node_array(data_array)
    dict_horizontal_line=get_horizontal_line_info(data_array_add,target_value,data_tif_info)
    dict_vertical_line=get_vertical_line_info(data_array_add,target_value,data_tif_info)
    dict_taget_point_h = {}
    dict_taget_point_v = {}

    for h_name in dict_horizontal_line:
        horizontal_line_list=dict_horizontal_line[h_name]

        r_c=horizontal_line_list[0]
        is_cross=horizontal_line_list[2]
        location_x_y=horizontal_line_list[3]

        if is_cross ==False:
            if len(location_x_y) >0:
                dict_taget_point_h[h_name]=[r_c,location_x_y,is_cross]
    for v_name in dict_vertical_line:
        vertical_line_list=dict_vertical_line[v_name]

        r_c=vertical_line_list[0]
        is_cross=vertical_line_list[2]
        location_x_y=vertical_line_list[3]

        if is_cross ==False:
            if len(location_x_y) >0:
                dict_taget_point_v[v_name]=[r_c,location_x_y,is_cross]

    dict_taget_point_h.update(dict_taget_point_v)
    dict_all_point=dict_taget_point_h

    contour_all_list=[]

    for taget_point_name in dict_all_point:

        taget_point_info=dict_all_point[taget_point_name]
        is_cross=taget_point_info[2]
        if is_cross == False:
            contour_list = []
            is_end=0
            last_point = ''
            now_point = taget_point_name
            contour_list.append(now_point)

            while is_end ==0:
                try:
                    next_point=get_next(now_point,dict_all_point,last_point)
                except:
                    print('包含开等值线')


                if next_point not in contour_list:
                    contour_list.append(next_point)
                    last_point=now_point
                    now_point=next_point
                else:
                    contour_list.append(next_point)
                    contour_all_list.append(contour_list)
                    is_end=1


    points_location_list=[]
    for points_name_list in contour_all_list:
        location_list=[]
        for point_name in points_name_list:
            point_location=dict_all_point[point_name][1]
            location_list.append(point_location)
        points_location_list.append(location_list)
        draw_contour(location_list)


    pd.DataFrame(points_location_list).to_excel('data_out/{0}等值线拐点坐标.xls'.format(target_value),index=0,header=0)































