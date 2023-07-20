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