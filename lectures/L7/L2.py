
import numpy as np

def L2(v, *args):
    """ Calculates L2 norm of a vector.
    
    Args
    ----
    v: Sequence[Numeric]
        Vector for which we wish to calculate the norm.
    args: Sequence[floats], optional
        Weight vector where args[i] will be applied to v[i]. If provided, length must be equal 
        to that of v.
    
    Returns
    -------
    Float representing the L2 norm.
    """
    s = 0.0 # Initialize sum
    if len(args) == 0: # No weight vector
        for vi in v:
            s += vi * vi
    else: # Weight vector present
        w = args[0] # Get the weight vector
        if (len(w) != len(v)): # Check lengths of lists
            raise ValueError("Length of list of weights must match length of target list.")
        for i, vi in enumerate(v):
            s += w[i] * w[i] * vi * vi
    return np.sqrt(s)