def is_subsequence(s: str, t: str) -> bool:
    t_iter = iter(t)  # Create an iterator for 't'
    return all(char in t_iter for char in s)
