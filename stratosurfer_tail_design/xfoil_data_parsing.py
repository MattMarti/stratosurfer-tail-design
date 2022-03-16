def load_xfoil_polar_file(filename:str):
    with open(filename, "r") as fid:
        return load_xfoil_polar(fid)


def load_xfoil_polar(fileobj):
        line = fileobj.readline()
        while line:
            previous_line = line
            line = fileobj.readline()
            if "----" in line:
                break
            else:
                previous_line = line
        column_names = previous_line.split()
        
        polar_data = {}
        for key in column_names:
            polar_data[key] = []
        
        for line in fileobj.readlines():
            line_values = line.split()
            for key, value_str in zip(column_names, line_values):
                polar_data[key].append(float(value_str))
        
        return polar_data
