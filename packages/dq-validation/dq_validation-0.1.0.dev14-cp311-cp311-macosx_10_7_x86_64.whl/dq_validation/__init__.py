import os

from .config import DEFAULT_USE_SPARK_FILE_SIZE_THRESHOLD_BYTES

from . import spark
from . import default


def run(
        input_path: str,
        config_path: str,
        report_path: str,
        types_path: str,
        output_path: str,
        force_spark: bool = False,
        spark_threshold_bytes: int = DEFAULT_USE_SPARK_FILE_SIZE_THRESHOLD_BYTES,
        temp_dir: str = "/scratch",
        drop_invalid_rows: bool = False,
):
    does_input_file_exist = os.path.exists(input_path)
    if not does_input_file_exist:
        raise Exception("Input file does not exist")

    input_file_size = os.path.getsize(input_path)
    print(f"Input file size: {round(input_file_size / 1000000, 2)} MB")

    if force_spark or input_file_size > spark_threshold_bytes:
        use_spark = True
    else:
        use_spark = False

    # TODO: What do to with empty files?

    print(f"Using spark: {use_spark}")
    if not use_spark:
        default.run(
            input_path=input_path,
            config_path=config_path,
            report_path=report_path,
            types_path=types_path,
            output_path=output_path,
            temp_dir=temp_dir,
            drop_invalid_rows=drop_invalid_rows
        )
    else:
        spark.run(
            input_path=input_path,
            config_path=config_path,
            report_path=report_path,
            types_path=types_path,
            output_path=output_path,
            temp_dir=temp_dir,
            drop_invalid_rows=drop_invalid_rows
        )
