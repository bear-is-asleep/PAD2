import numpy as np
def convert_edges_to_centers(edges):
  """_summary_

  Args:
      edges (_type_): _description_

  Returns:
      _type_: _description_
  """
  de = edges[1]-edges[0]
  return [e+de/2 for e in edges[:-1]]

# function
def get_common_members(a, b):  
    """_summary_

    Args:
        a (list): _description_
        b (list): _description_

    Returns:
        list: _description_
    
    """ 
    a_set = set(a)
    b_set = set(b)
     
    # check length
    if len(a_set.intersection(b_set)) > 0:
        return(list(a_set.intersection(b_set))) 
    else: 
        return []

def is_traj_in_volume(traj, volume, n=10000):
    """
    Given a trajectory of start and end points, check if the trajectory is in the volume.
    Rough calculation by sampling n points along the trajectory and checking if 
    any of the points are in the volume.
    
    Args:
        traj (list): list of start and end points (6)
        volume (list): list of start and end points of the volume (3,2)
        n (int): number of points to sample along the trajectory
    Returns:
        bool: True if the trajectory is in the volume
    """
    #Unpack values
    x1, y1, z1, x2, y2, z2 = traj
    xmin, ymin, zmin = volume[0]
    xmax, ymax, zmax = volume[1]
    points = np.array([np.linspace(x1, x2, n), np.linspace(y1, y2, n), np.linspace(z1, z2, n)]).T
    return np.any(np.logical_and(np.all(points >= volume[0], axis=1), np.all(points <= volume[1], axis=1)))    
