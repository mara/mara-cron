import os
import pathlib
import shlex

from . import config


class CronJob():
    """ A cron job configuration """
    def __init__(self, id: str, description: str,
                 time_pattern: str, command: str,
                 enabled: bool = True):
        self.id = id
        self.description = description
        self.time_pattern = time_pattern
        self.command = command
        self.enabled = enabled

    @property
    def shell_command(self):
        if config.log_path():
            log_path = pathlib.Path(config.log_path())

            log_full_path = None
            if log_path.is_file():
                log_full_path = str(log_path.absolute())
            elif log_path.is_dir():
                log_full_path = str((log_path / 'mara-cron_$(date "+%Y%m%d_%H%M%S").log').absolute())

            if log_full_path:
                log_command = f'{{ echo "MARA CRON JOB {self.id} START $(date)"; {self.command}; echo "MARA CRON JOB {self.id} END $(date)" ; }}'

                if '$' not in log_full_path:
                    log_full_path = shlex.quote(log_full_path)

                return f'{log_command} >> {log_full_path} 2>&1'

        return self.command


class MaraJob(CronJob):
    """ A configuration for a mara command"""
    def __init__(self, id: str, description: str, time_pattern: str, command: str,
                 args: dict = None, enabled = True):
        virtual_env_path = os.environ['VIRTUAL_ENV']
        if not virtual_env_path:
            raise Exception('Could not determine virtual environment path. VIRTUAL_ENV not set')

        mara_root_path = pathlib.Path(virtual_env_path).parent.resolve()

        job_command = f'cd {mara_root_path} ; source .venv/bin/activate ; flask {command}'

        if args:
            for param, value in args.items() if args else {}:
                job_command += f' {param}' \
                                + (f' {value}' if value and not isinstance(value, bool) else '')

        super().__init__(id, description, time_pattern=time_pattern, command=job_command,
                         enabled=enabled)
