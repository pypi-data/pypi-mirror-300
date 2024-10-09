import functools
from typing import Callable, Any

from ... import config, logger

def generation_logger(func: Callable) -> Callable:
    @functools.wraps(func)  # 保留 func 的元信息
    def wrapper(self, *args, **kwargs) -> Any:
        result = func(self, *args, **kwargs)
        if config.log_model_io:
            logger.info("【model_io】"+self.backend+":"+self.model_name+".generate()")
            logger.info("- input_text: "+result["input_text"])
            logger.info("- output_text: "+result["output_text"])
        return result
    return wrapper