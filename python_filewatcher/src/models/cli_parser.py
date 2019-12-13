import argparse
from src.models.load_yaml import load_config


def cli_parser(_logger):
    """Parser of arguments from cli
    :args: Logs()
    :return: params
    """
    # get the obj Logs()
    logger = _logger
    # start parsing args cli
    parser = argparse.ArgumentParser(description="Monotoring of directory contents")

    # set all arguments possibilities
    root_group = parser.add_mutually_exclusive_group()
    parser.add_argument("-d", "--directory", type=str, help="directory name")
    parser.add_argument("-i", "--interval", type=int, help="number of seconds")
    parser.add_argument("-l", "--logging", type=str, help="logging config filename")
    group_list_config = root_group.add_mutually_exclusive_group()
    group_list_config.add_argument("-c", "--config", type=str,
                                   help="[interval int in seconds, directory path] config yaml filename")

    # get args
    args = parser.parse_args()

    # loading logs if true
    logged = False
    params = []

    # if logging file config given
    if args.logging:
        _logging = args.logging
        # init logs
        logger.handle_log_cases(case='set', filename=_logging)
        logged = True
        # write logs
        logger.handle_log_cases(text="Logs processing...", case='info')
        params.append(args.logging)
        print("logging: ", params)
    else:
        print("warning: must be set on '-l true' to handle debugs, infos, warnings")

    # if yaml file config given
    if args.config:
        # load YAML config file
        _config_yaml = load_config(args.config)
        _interval = _config_yaml['interval']
        _directory = _config_yaml['directory']
        if logged is True:
            # write logs
            logger.handle_log_cases(text="Loading YAML config file...", case='info')
        params.append(_directory)
        params.append(_interval)
        print("config YAML: ", params)
        return check_params(params, logged, logger)

    # if directory given
    if args.directory:
        # change the directory by the argument passed for --directory
        _directory = args.directory
        if logged is True:
            # write logs
            logger.handle_log_cases(text="Setting directory to monitor...", case='info')
        params.append(_directory)
        print("new path to monitor: ", params)
    else:
        if logged is True:
            logger.handle_log_cases(text="Directory to monitor @required", case='critical')

    # if interval given
    if args.interval:
        # get the interval duration
        _interval = args.interval
        if logged is True:
            # write logs
            logger.handle_log_cases(text="Setting interval in seconds...", case='info')
        params.append(_interval)
        print("interval: ", params)
    else:
        if logged is True:
            # write logs
            logger.handle_log_cases(text="Interval in seconds @required", case='critical')

    return check_params(params, logged, logger)


def check_params(params, logged, logger):
    """Check parameters
    :args: params, logged, logger
    :return: params
    """
    if len(params) > 1:

        # if true you return params
        if logged is True:
            # write logs
            logger.handle_log_cases(text="Loading the params...", case='info')

        return params

    else:
        # if not you return an empty params
        if logged is True:
            # write logs
            logger.handle_log_cases(text="Too much critical alerts, stopping to process...", case='critical')
            logger.handle_log_cases(text="Check your logs for more informations", case='debug')

        params = []
        return params
