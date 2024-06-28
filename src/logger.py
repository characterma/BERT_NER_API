from loguru import logger
import os
import sys
import yaml
conf_file_path = "configs/configs.yaml"
with open(conf_file_path, 'r') as f:
    conf_info = yaml.load(f, Loader=yaml.FullLoader)
logger_level = conf_info['APP']['LOGGIN_LEVEL']

logger.remove()
LOG_DIR = os.path.expanduser("./logs")
success_file = os.path.join(LOG_DIR, "SUCCESS.log")
failed_file = os.path.join(LOG_DIR, "FAILED.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger.add(sys.stdout,
           level=logger_level,
           filter=lambda record: record["level"].name == "INFO")
logger.add(sys.stdout,
           level=logger_level,
           filter=lambda record: record["level"].name == "ERROR")

# logger.add(success_file,
#            level=logger_level,
#            rotation="5 days",
#            compression="zip",
#            retention='10 days',
#            filter=lambda record: record["level"].name == "INFO")
# logger.add(failed_file,
#            level=logger_level,
#            rotation="5 days",
#            compression="zip",
#            retention='10 days',
#            filter=lambda record: record["level"].name == "ERROR")
logger.info(f"设置日志级别为： {logger_level}")
logger.info(f"sucess log file path: {success_file}, failed log file path: {failed_file}")
logger.debug("测试DEBUG级别是否输出日志")
logger.info("测试INFO级别是否输出日志")
logger.error("测试ERROR级别是否输出日志")





