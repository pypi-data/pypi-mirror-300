import json
import logging
import time
from pprint import pprint
from typing import Any

import requests

from mediacatch.utils import MediacatchAPIError, MediacatchError, MediacatchTimeoutError

logger = logging.getLogger('mediacatch.vision.result')


def wait_for_result(
    file_id: str,
    url: str = 'https://api.mediacatch.io/vision',
    timeout: int = 3600,
    delay: int = 10,
    verbose: bool = True,
) -> dict[str, Any] | None:
    """Wait for result from a URL.

    Args:
        file_id (str): The file ID to get the result from.
        url (str): The URL to get the result from.
        timeout (int, optional): Timeout for waiting in seconds. Defaults to 3600.
        delay (int, optional): Delay between each request. Defaults to 10.
        verbose (bool, optional): If True, print log messages. Defaults to True.

    Returns:
        dict[str, Any] | None: Dictionary with the result from the URL or None if failed.
    """
    result_url = f'{url}/result/{file_id}'
    if verbose:
        logger.info(f'Waiting for result from {result_url}')

    start_time = time.time()
    end_time = start_time + timeout
    while time.time() < end_time:
        try:
            response = requests.get(result_url)
            if response.status_code in [404, 429, 500]:
                if verbose:
                    pprint(response.json())

                raise MediacatchAPIError(response.status_code, response.json())

            if response.status_code == 102:
                if verbose:
                    logger.info(f'Waiting for result from {result_url}')

                time.sleep(delay)
                continue
            elif response.status_code == 504:
                time.sleep(delay)
                continue

            response.raise_for_status()
            if response.status_code == 204:
                if verbose:
                    logger.info(f'No results found for {file_id}')

                return {}

            result = response.json()
            elapsed_time = time.time() - start_time
            if verbose:
                logger.info(f'Got result from {result_url} in {elapsed_time:.2f} seconds')

            return result

        except (requests.RequestException, json.JSONDecodeError):
            if verbose:
                logger.error('Error occurred while waiting for JSON response')

        except Exception as e:
            if verbose:
                logger.error(f'Failed to get result from {result_url}: {e}')

            raise MediacatchError(f'Failed to get result from {result_url}: {e}')

        time.sleep(delay)

    if verbose:
        logger.error(f'Timeout waiting for result from {result_url}, give up')

    raise MediacatchTimeoutError(f'Timeout waiting for result from {result_url}')


if __name__ == '__main__':
    file_id = '66e6fb29b775ebfd11fb40f7'
    result = wait_for_result(file_id)
    print(result)
