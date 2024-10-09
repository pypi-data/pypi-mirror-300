"""
Helps to view long nested dictionaries
"""

def view(d, length=3, return_obj=False):

    lines = []

    def view_recursive(d, lvl=0, length=3):

        assert length >= 2, "Length must be >= 2"

        tick = f"+{'-'*(length-1)}"
        pipe = f"|{' '*(length-1)}"

        for k, v in d.items():

            if lvl == 0:
                line = ""
            elif lvl == 1:
                line = tick
            else:
                line = f"{pipe*(lvl-1)}{tick}"
            
            if isinstance(v, dict) and lvl == 0:
                lines.append(f"{line}{k}")
                view_recursive(v, lvl+1, length)
            elif isinstance(v, dict) and lvl > 0:
                lines.append(f"{line}{k}")
                view_recursive(v, lvl+1, length)
            else:
                lines.append(f"{line}{k} <{type(v).__name__}>")

    view_recursive(d, length=length)

    if return_obj:
        return lines
    else:
        print('\n'.join(lines))
        return None
