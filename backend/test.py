from src.model_handling.pipeline import apply_pipeline
from src.data_handling.database_con import get_pipeline_names

print(get_pipeline_names())

apply_pipeline("test pipeline1")
