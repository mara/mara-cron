import os
import pathlib
import shlex

from . import config


class CronJob():
    """ A cron job configuration """
    def __init__(self, id: str, description: str, command: str,
                 default_time_pattern: str = None, default_enabled: bool = True):
        self.id = id
        self.description = description
        self.time_pattern = default_time_pattern
        self.command = command
        self.enabled = default_enabled

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
    """ A configuration for a mara job"""
    def __init__(self, id: str, description: str, command: str, args: dict = None,
                 default_time_pattern: str = None, default_enabled = True):
        virtual_env_path = os.environ['VIRTUAL_ENV']
        if not virtual_env_path:
            raise Exception('Could not determine virtual environment path. VIRTUAL_ENV not set')

        mara_root_path = pathlib.Path(virtual_env_path).parent.resolve()

        job_command = f'cd {mara_root_path} ; . ./.venv/bin/activate ; flask {command}'

        if args:
            for param, value in args.items() if args else {}:
                job_command += f' {param}' \
                                + (f' {value}' if value and not isinstance(value, bool) else '')

        super().__init__(id=id, description=description, command=job_command,
                         default_time_pattern=default_time_pattern, default_enabled=default_enabled)


class RunPipelineJob(MaraJob):
    """ A configuration for a job executing a mara pipeline"""
    def __init__(self, id: str, description: str, path: str = None, nodes: [str] = None, with_upstreams: bool = False,
                 default_time_pattern: str = None, default_enabled = True):
        """
        A job running a mara pipeline.
        """
        command = 'mara_pipelines.ui.run'
        args = {
            '--disable-colors': False
        }
        if path:
            args['--path'] = path
        if nodes:
            args['--nodes'] = ','.join(nodes)
        if with_upstreams:
            args['--with_upstreams'] = with_upstreams

        super().__init__(id=id, description=description, command=command, args=args,
                         default_time_pattern=default_time_pattern, default_enabled=default_enabled)