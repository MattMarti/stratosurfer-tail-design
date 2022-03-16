import io
import pytest

import stratosurfer_tail_design.xfoil_data_parsing as parsing


def test_load_xfoil_polar():
    
    file_str = """
       XFOIL         Version 6.99
  
   alpha    CL        CD   
  ------ -------- ---------
  -7.000  -0.3   0.06
  -6.500  -0.2   0.05
  -6.000  -0.2   0.03
    """
    
    polar_data = parsing.load_xfoil_polar(io.StringIO(file_str))
    
    assert "alpha" in polar_data
    assert "CL" in polar_data
    assert "CD" in polar_data

    assert len(polar_data["alpha"]) == 3
    assert len(polar_data["CL"]) == 3
    assert len(polar_data["CD"]) == 3
    
    assert polar_data["alpha"][0] == -7
    assert polar_data["alpha"][1] == -6.5
    assert polar_data["alpha"][2] == -6

    assert polar_data["CL"][0] == -.3
    assert polar_data["CL"][1] == -.2
    assert polar_data["CL"][2] == -.2
    
    assert polar_data["CD"][0] == 0.06
    assert polar_data["CD"][1] == 0.05
    assert polar_data["CD"][2] == 0.03
    