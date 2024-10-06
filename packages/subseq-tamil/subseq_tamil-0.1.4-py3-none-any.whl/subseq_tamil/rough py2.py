# subsequence.py
def is_subsequence(s: str, t: str) -> bool:
    """
    Check if 's' is a subsequence of 't'.
    
    Parameters:
    s (str): The sequence to check if it is a subsequence.
    t (str): The sequence to check against.
    
    Returns:
    bool: True if 's' is a subsequence of 't', otherwise False.
    """
    t_iter = iter(t)  # Create an iterator for 't'
    return all(char in t_iter for char in s)
