import logging

import APIRequests


def main():
    set_logging_config()

    logging.info('Start App; initializing APIRequests')
    api_requests = APIRequests.APIRequests()
    logging.info('Start main loop!')
    api_requests.main_loop()


def set_logging_config():
    logging.basicConfig(filename='test_log.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.DEBUG)


if __name__ == '__main__':
    main()
