"""Config of the FastMindAPI package which contains all kinds of settings and basic information about the job.
"""

import datetime

import pydantic

class FMConfig(pydantic.BaseModel):
    """
    """
    job_time: str
    type_check: bool = True
    log_model_io: bool = True


def get_config():
    return FMConfig(
        job_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        type_check = True
    )