import copy
import json
import sys
import typing
from crontab import CronTab, CronItem

from . import config
from .job import CronJob


def current() -> CronTab:
    tabfile = config.tabfile()
    if tabfile:
        cron = CronTab(tabfile=tabfile)
    else:
        cron = CronTab(user=config.user())

    return cron


def _build_job_comment(job_id: str, module_name: str = None) -> str:
    job_comment_dict = {}
    instance = config.instance_name()
    if instance:
        job_comment_dict['instance'] = instance

    if module_name:
        job_comment_dict['module'] = module_name

    job_comment_dict['job_id'] = job_id

    return f'mara {json.dumps(job_comment_dict)}'


def get_job(cron: CronTab, job_id: str, module_name: str = None) -> typing.Optional[CronItem]:
    job_comment = _build_job_comment(job_id, module_name)

    for j in cron.find_comment(job_comment):
        return j


def generate() -> CronTab:
    cron = current()

    # iterate through defined cron jobs
    cronjob_modules = {}
    for module_name, module in copy.copy(sys.modules).items():
        if 'MARA_CRON_JOBS' in dir(module):
            cronjobs = getattr(module, 'MARA_CRON_JOBS')
            if isinstance(cronjobs, typing.Callable):
                cronjobs = cronjobs()
            assert (isinstance(cronjobs, typing.Iterable))
            cronjob_modules[module_name] = {}
            for cronjob in cronjobs:
                assert (isinstance(cronjob, CronJob))

                job_comment = _build_job_comment(
                                  job_id=cronjob.id,
                                  module_name=(module_name if module_name != 'app' else None))

                job = None
                for j in cron.find_comment(job_comment):
                    job = j
                    job.set_command(cronjob.shell_command)
                    break

                if not job:
                    if not cronjob.time_pattern:
                        continue
                    job = cron.new(command=cronjob.shell_command, comment=job_comment)

                enabled = cronjob.enabled and config.enabled()

                if cronjob.time_pattern:
                    job.setall(cronjob.time_pattern)
                else:
                    # time pattern not set, keep the current time pattern and disable the cronjob
                    enabled = False

                job.enable(enabled)

    return cron
