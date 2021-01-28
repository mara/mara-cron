import os


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


class MaraJob(CronJob):
    """ A configuration for a mara command"""
    def __init__(self, id: str, description: str, time_pattern: str, command: str,
                 args: dict = None, enabled = True):
        virtual_env_path = os.environ['VIRTUAL_ENV']
        if not virtual_env_path:
            raise Exception('Could not determine virtual environment path. VIRTUAL_ENV not set')

        job_command = f'source {virtual_env_path}/bin/activate; flask {command}'

        if args:
            for param, value in args.items() if args else {}:
                job_command += f' {param}' \
                                + (f' {value}' if value and not isinstance(value, bool) else '')

        super().__init__(id, description, time_pattern=time_pattern, command=job_command,
                         enabled=enabled)
