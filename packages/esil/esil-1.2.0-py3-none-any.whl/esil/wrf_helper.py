'''
Author: Devin
Date: 2024-07-03 16:07:12
LastEditors: Devin
LastEditTime: 2024-10-09 11:08:40
Description: 

Copyright (c) 2024 by Devin, All Rights Reserved. 
'''
import os
import pickle
import netCDF4 as nc
import numpy as np

def get_model_lat_lon_proj(model_lat_lon_file,varibale_name="T2", model_pkl_file=None):
    dir=os.path.dirname(model_lat_lon_file)
    model_file=os.path.basename(model_lat_lon_file)
    model_pkl_file=os.path.join(dir,f'{model_file}.pkl') if model_pkl_file is None else model_pkl_file
    if os.path.exists(model_pkl_file):
        with open(model_pkl_file, 'rb') as file:
            cart_proj, model_lats, model_lons = pickle.load(file)
    else:       
        x,y,model_lons,model_lats,dx,dy,cart_proj=get_wrf_info(model_lat_lon_file,variable_name="T2")
        # model_lats, model_lons= to_np(lats), to_np(lons)
        with open(model_pkl_file, 'wb') as file:
            pickle.dump((cart_proj, model_lats, model_lons), file)
    return cart_proj,model_lats,model_lons

def get_wrf_info(wrf_out_file,variable_name="T2"):
    '''
    Get the x,y,lons,lats,dx,dy,cart_proj from wrf_out_file
    @param: wrf_out_file: the wrf output file
    @param: variable_name: the variable name to get the info
    @return: x,y,lons,lats,dx,dy,cart_proj: the x,y grid (lamber projection), lons,lats grid, dx,dy(grid size) and cartopy projection

    '''
    from wrf import (to_np, getvar, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)
    import netCDF4 as nc
    dataset = nc.Dataset(wrf_out_file, 'r')
    t2 = getvar(dataset,variable_name)
    cart_proj = get_cartopy(t2)
    lats, lons =latlon_coords(t2)
    lons,lats =to_np(lons), to_np(lats)
    xlims,ylims= cartopy_xlim(t2),cartopy_ylim(t2)
    x_coords,y_coords=np.linspace(xlims[0],xlims[1],lons.shape[1]),np.linspace(ylims[0],ylims[1],lons.shape[0])   
    x,y=np.meshgrid(x_coords,y_coords) 
    dx, dy=dataset.DX,dataset.DY 
    return x,y,lons,lats,dx,dy,cart_proj 