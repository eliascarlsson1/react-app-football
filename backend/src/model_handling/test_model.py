from typing import List, Dict
from ..model_handling.apply_model_utils import (
    apply_model,
    load_x_and_y_parameters_from_model,
)
from ..data_handling.calculations import calculate_basic_roi


# FIXME: Implement test later
# Retruns a dictionary of key "PL2122" etc. to ROI
def get_roi_for_model_and_test(
    test_data: List[str], model: str, test: str = ""
) -> Dict[str, str]:
    df_dict = apply_model(model, test_data)
    roi_dict: Dict[str, str] = {}
    y_par = load_x_and_y_parameters_from_model(model)[1]
    for key in df_dict:
        roi_dict[key] = calculate_basic_roi(df_dict[key], y_par)
    return roi_dict
