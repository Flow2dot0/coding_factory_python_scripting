import src.sqlite as db
from src.checksum import *
from os import listdir
from os.path import isfile, join
import time

from src.models.Logs import Logs
from src.models.cli_parser import cli_parser


def main():
    """Main module"""
    _logger = Logs()
    _run = False
    _with_logs = False
    # parse arguments
    get_list = cli_parser(_logger)
    if get_list is not None:

        if len(get_list) > 1:
            _run = True
            if len(get_list) == 3:
                _with_logs = True

    # running app
    if _run is True:
        db.init()
        _logger.handle_log_cases(case="info", text="Daemon ready")
        directory = get_list[1] if _with_logs else get_list[0]
        interval = get_list[2] if _with_logs else get_list[1]

        while True:
            files = [f for f in listdir(directory) if isfile(join(directory, f))]  # fetch all files in directory
            db_files = db.select_filename()
            for file in files:
                # Delete all files existing in folder and database
                for db_file in db_files:
                    if (db_file == file):
                        del db_files[db_files.index(file)]

                # File exist in db
                checksum = checksum_file(directory + file)
                if db.count(file) > 0:
                    if db.select(file)[2] != checksum:
                        text = ''.join(["File ", file, " changed"])
                        _logger.handle_log_cases(case="info", text=text)
                        if (db.update_signature(file, checksum) == False):
                            _logger.handle_log_cases(case="warning", text="Error while updating database")
                else:
                    text = ''.join(["New file detected : ", file])
                    _logger.handle_log_cases(case="info", text=text)
                    db.write(file, directory, checksum)

            # Detect file removed here
            for deleted in db_files:
                if (db.remove_filename(deleted)):
                    text = ''.join(["File ", deleted, " removed"])
                    _logger.handle_log_cases(case="info", text=text)
                else:
                    _logger.handle_log_cases(case="warning", text="Error remove filename in database")

            time.sleep(interval)  # in sec


if __name__ == '__main__':
    main()
