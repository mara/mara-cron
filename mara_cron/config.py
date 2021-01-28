import typing as t


def enabled() -> bool:
    """
    A global parameter which lets you disable/activate all cron jobs

    Default value: False.
    """
    return False


def instance_name() -> t.Optional[str]:
    """
    Lets you define a name of your mara instance.

    Cron jobs will be executed per instance.
    """
    return None


def user() -> t.Union[bool, str]:
    """
    The crontab user:
    - you can return the name of crontab user
    - you can enter 'true' in case you want to get the crontab of the current user

    By default the current user is taken
    """
    return True


def tabfile() -> t.Optional[str]:
    """
    The crontab file. Use '/etc/crontab' in order to use

    By default not set. This will override the user() config.
    """
    return None
