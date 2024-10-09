from functools import cache, wraps
from inspect import getfullargspec
from typing import Literal

import numpy as np
from scipy.interpolate import make_interp_spline

from pylegs.config import configs
from pylegs.io import read_table


def pseudo_vectorial(*vec_args):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      args_name = getfullargspec(func)[0]
      args_dict = {**dict(zip(args_name, args)), **kwargs}
                
      is_vector = False
      vec_len = -1
      for k in vec_args:
        is_vector = is_vector or not np.isscalar(args_dict[k])
        if is_vector:
          vec_len = len(args_dict[k])
      
      if is_vector:
        vec_iter = ({k: args_dict[k][i] for k in vec_args} for i in range(vec_len))
        scalar_args = {k: v for k, v in args_dict.items() if k not in vec_args}
        return np.asarray([
          func(**scalar_args, **_vector_args)
          for _vector_args in vec_iter
        ])
      return func(*args, **kwargs)
    return wrapper
  return decorator


def compute_ellipse_bb(x, y, major, minor, angle_deg):
  """
  Compute tight ellipse bounding box.
  
  see https://stackoverflow.com/questions/87734/how-do-you-calculate-the-axis-aligned-bounding-box-of-an-ellipse#88020
  """
  eps = 1e-10
  angle_rad = np.radians(angle_deg)
  angle_rad_eps = np.radians(angle_deg + eps)
  
  t = np.arctan(-minor / 2 * np.tan(angle_rad_eps) / (major / 2))
  [min_x, max_x] = np.sort([
    x + major / 2 * np.cos(t) * np.cos(angle_rad) - 
    minor / 2 * np.sin(t) * np.sin(angle_rad) 
    for t in (t, t + np.pi)
  ], axis=0)
  
  t = np.arctan(minor / 2 * 1. / np.tan(angle_rad_eps) / (major / 2))
  [min_y, max_y] = np.sort([
    y + minor / 2 * np.sin(t) * np.cos(angle_rad) +
    major / 2 * np.cos(t) * np.sin(angle_rad) 
    for t in (t, t + np.pi)
  ], axis=0)
  
  return min_x, min_y, max_x, max_y



# @pseudo_vectorial('shape_e1', 'shape_e2')
def compute_ellipse_params(shape_e1: float, shape_e2: float, max_e: float = None):
  eps = 1e-10
  e = np.sqrt(shape_e1 ** 2 + shape_e2 ** 2)
  if max_e is not None:
    e = np.minimum(e, max_e)
  b = 1 - e
  a = 1 + e
  angle = 180 - np.rad2deg(np.arctan2(shape_e2 + eps, shape_e1 + eps) / 2)
  mask = np.greater(b, a)
  if np.isscalar(mask):
    a, b = b, a
    angle += 180
  else:
    temp = a[mask]
    a[mask] = b[mask]
    b[mask] = temp
    angle[mask] += 180
  return a, b, angle



@cache
def _get_correction_factor_df():
  return read_table(configs.CORRECTION_FACTOR_PATH)



@cache
def _get_correction_factor_model(
  kind: Literal['circle', 'ellipse'], 
  interp: Literal['step', 'linear']
):
  df = _get_correction_factor_df()
  if kind.lower() == 'ellipse' and interp.lower() == 'step':
    return make_interp_spline(df.mag_r.values, df.cf_ellip_step.values, 0)
  elif kind.lower() == 'ellipse' and  interp.lower() == 'linear':
    return make_interp_spline(df.mag_r.values + 0.5, df.cf_ellip_linear.values, 1)
  elif kind.lower() == 'circle' and interp.lower() == 'step':
    return make_interp_spline(df.mag_r.values, df.cf_circ_step.values, 0)
  elif kind.lower() == 'circle' and interp.lower() == 'linear':
    return make_interp_spline(df.mag_r.values + 0.5, df.cf_circ_linear.values, 1)
  


def correction_factor_ellipse(
  mag_r: float, 
  interp: Literal['step', 'linear'] = 'linear'
):
  if interp == 'linear':
    return _get_correction_factor_model('ellipse', 'linear')(mag_r)
  return _get_correction_factor_model('ellipse', 'step')(mag_r)



def correction_factor_circle(
  mag_r: float, 
  interp: Literal['step', 'linear'] = 'linear'
):
  if interp == 'linear':
    return _get_correction_factor_model('circle', 'linear')(mag_r)
  return _get_correction_factor_model('circle', 'step')(mag_r)



# @pseudo_vectorial('shape_e1', 'shape_e2', 'mag_r')
def compute_fov_ellip(shape_e1, shape_e2, mag_r, interp):
  a, b, angle = compute_ellipse_params(shape_e1, shape_e2, 0.6)
  x0, y0, x1, y1 = compute_ellipse_bb(0, 0, b, a, angle)
  cf = correction_factor_ellipse(mag_r, interp=interp)
  width = np.abs(x1 - x0) * 2
  height = np.abs(y1 - y0) * 2
  return np.maximum(width, height) * cf * 60



# @pseudo_vectorial('shape_e1', 'shape_e2', 'mag_r')
def compute_pixscale_ellip(shape_e1, shape_e2, size, mag_r, interp):
  fov = compute_fov_ellip(shape_e1=shape_e1, shape_e2=shape_e2, mag_r=mag_r, interp=interp)
  return fov / size



# @pseudo_vectorial('shape_r', 'mag_r')
def compute_fov_circ(shape_r, mag_r, interp):
  cf = correction_factor_circle(mag_r, interp=interp)
  return 2 * shape_r * cf



# @pseudo_vectorial('shape_r', 'mag_r')
def compute_pixscale_circle(shape_r, size, mag_r, interp):
  fov = compute_fov_circ(shape_r=shape_r, mag_r=mag_r, interp=interp)
  return fov / size


  


if __name__ == '__main__':
  df = read_table('/home/natan/repos/legacy-stamps/samples/sample_10-11_300.csv')
  x = compute_pixscale_ellip(df.shape_e1.values, df.shape_e2.values, 300, df.mag_r.values, 'linear')
  y = df.pixscale_ellip_linear.values
  print(np.allclose(x, y))
  # print(compute_ellipse_bb(0, 0, 10, 15, 45))
  # print(compute_ellipse_bb(0, 0, np.asarray([10, 20]), np.asarray([15, 30]), np.asarray([45, -45])))