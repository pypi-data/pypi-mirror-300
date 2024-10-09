"""
Finds path thru dict to desired key
"""

from    collections import deque
import  warnings

def seek(d, target, strategy="dfs"):

    paths = []

    def seek_dfs(d, target, idx=0, current_path=None):
        
        # Base case: current path is not given
        if current_path is None:
            current_path = []

        # Base case: sequence has been fully matched
        if idx == len(target):
            return current_path
        
        for k, v in d.items():
            new_path = current_path + [k]
            candidate = (v, new_path)
            # If key matches current part of sequence, look deeper 
            if k == target[idx]:
                # If it is the last key in the sequence, it's a match
                if idx == len(target) - 1 and candidate not in paths:
                    paths.append(candidate)
                # Otherwise continue deeper into the sequence
                if isinstance(v, dict):
                    result = seek_dfs(
                        v, 
                        target, 
                        idx=idx + 1, 
                        current_path=new_path
                    )
                    if result is not None and candidate not in paths:
                        paths.append(candidate)
            # If not, look deeper into the dict, but not the sequence
            if isinstance(v, dict):
                result = seek_dfs(
                    v, 
                    target, 
                    idx=idx, 
                    current_path=new_path
                )
                if result is not None and candidate not in paths:
                    paths.append(candidate)
        return None

    def seek_bfs(d, target, current_path=None):
        pass

    def seek_hybrid(d, target, current_path=None):
        pass

    def combine_keys(keys):

        return keys

    if strategy=="dfs":
        seek_dfs(d, target)
    elif strategy=="bfs":
        seek_bfs(d, target)
    elif strategy=="hybrid":
        seek_hybrid(d, target)
    else:
        raise ValueError("Strategy should be one of ['dfs', 'bfs', 'hybrid']")

    if len(paths) > 1:
        warnings.warn(
            f"\n> There are multiple paths that lead to target {'/'.join(target)}"
            f"\n> Consider being more specific with your target."
        )

    return paths