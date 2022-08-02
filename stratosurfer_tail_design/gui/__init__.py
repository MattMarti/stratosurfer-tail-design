from dataclasses import dataclass

@dataclass(frozen=True)
class ButtonSizes:
    GUI_BUTTON_WIDTH = 10
    GUI_BUTTON_PADDING = 20

from .airfoil_design_frame import AirfoilDesignFrame
from .tail_dimensions_design_frame import TailDimensionsDesignFrame
from .flat_section_design_frame import FlatSectionDesignFrame