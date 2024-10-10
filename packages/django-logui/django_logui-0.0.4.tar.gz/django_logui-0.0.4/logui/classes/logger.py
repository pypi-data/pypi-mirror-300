from __future__ import annotations

import logging
import os


class Logger:
    def __init__(
            self,
            name: str,
            level: str = 'DEBUG',
            include_in: list[str] | tuple[str] | None = None,
            files_before_archiving: int = 360,
            propagate: bool = False,
    ):
        self.name = name
        self.level = level
        self.include_in = include_in or []
        self.files_before_archiving = files_before_archiving
        self.propagate = propagate


class LoggingBuilder:
    def __init__(
            self,
            logs_dir: str,
            loggers: list[Logger, ...] | tuple[Logger, ...],
            format: str = '{levelname} {asctime}: {message}',
            datefmt: str = '%d-%m %H:%M:%S'
    ):
        self.logs_dir = logs_dir
        self.format = format
        self.datefmt = datefmt
        self.loggers = loggers

    @staticmethod
    def check_loggers(LOGGING: dict) -> None:
        if True if os.environ.get('RUN_MAIN') != 'true' else False:
            for logger_name in LOGGING['loggers']:
                log = logging.getLogger(logger_name)
                log.warning(f'Logger found: {logger_name}')

    def build(self) -> dict:
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'base_formatter': {
                    'format': self.format,
                    'style': '{',
                    'datefmt': self.datefmt,
                }
            },
            'handlers': {},
            'loggers': {}
        }

        # Создание папки для логов
        os.makedirs(self.logs_dir, exist_ok=True)

        # Определяем хендлер для консоли
        LOGGING['handlers']['console'] = {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'base_formatter',
        }

        # Добавление логгеров
        for logger in self.loggers:
            logger_name = logger.name
            log_dir = os.path.join(self.logs_dir, logger_name)
            os.makedirs(log_dir, exist_ok=True)

            log_file_handler_name = f'{logger_name}_file'
            LOGGING['handlers'][log_file_handler_name] = {
                'level': logger.level,
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(log_dir, f'{logger_name}.log'),
                'when': 'midnight',
                'backupCount': logger.files_before_archiving,
                'formatter': 'base_formatter',
                'encoding': 'utf-8',
                'delay': True,
            }

            LOGGING['loggers'][logger_name] = {
                'handlers': ['console', log_file_handler_name],
                'level': logger.level,
                'propagate': logger.propagate,
            }

            # Добавление логгера в другие логгеры
            for include_logger in logger.include_in:
                if include_logger not in LOGGING['loggers']:
                    LOGGING['loggers'][include_logger] = {
                        'handlers': ['console'],
                        'level': 'DEBUG',
                        'propagate': False,
                    }
                LOGGING['loggers'][include_logger]['handlers'].append(log_file_handler_name)

        return LOGGING
