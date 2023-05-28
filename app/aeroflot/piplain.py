import runpy
import datetime
import time
from logger import logger
from app.config import path_project


# Путь до каталога с файлами данных
path = path_project.scr

starttime = time.time()
logger.info('Запуск расчета')


modules = [
    f"{path}data_preprocessing_1.py",
    f"{path}data_preprocessing_2.py",
    f"{path}data_preprocessing_3.py",
    f"{path}forecast_1_flight.py",
    f"{path}forecast_2_reserv.py",
    f"{path}pg_data_loading.py"
    ]
try:
    for load_file in modules:
        logger.info(f"Module: {load_file}")
        runpy.run_path(load_file, run_name='__main__')
except Exception as exc:
    logger.error(f'ОШИБКА !!! \n{exc}')
    raise
finally:
    logger.info('Время обработки данных: ' + str(
        datetime.timedelta(seconds=(time.time() - starttime))))
