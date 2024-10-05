import requests

from .utils import set_logger
from .exceptions import QueryFailedException

logger = set_logger(__name__)


class PrometheusQuerier:
    """
    Base class for querying DataSource.
    :parameter endpoint: str, URL of the Prometheus server.
    """

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def prometheus_is_up(self):
        try:
            resp = requests.get(self.endpoint)
            return resp.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f'request failed with code {e.response.status_code}')
        except Exception as e:
            logger.error(f'generic error: {e}')

    def make_query_range(self, query, _from, _to, step='1m'):
        """
        Query Prometheus server with a range.
        :param query: is the query to be executed.
        :param _from: is the start time of the range, in unix timestamp.
        :param _to: is the end time of the range, in unix timestamp.
        :param step: is the step of the range.
        :return: list of results.
        """
        try:
            resp = requests.get(
                url=f'{self.endpoint}/api/v1/query_range',
                params={
                    'query': query,
                    'start': _from,
                    'end': _to,
                    'step': step,
                }
            )
            resp.raise_for_status()
            data = resp.json()

            if data['status'] != 'success':
                raise QueryFailedException(f'query {query} failed')

            return data['data']['result']

        except requests.exceptions.RequestException as e:
            logger.error(f'request failed with code {e.response.status_code}')
        except Exception as e:
            logger.error(f'generic Error: {e}')

    def make_query(self, query):
        """
        Query Prometheus server.
        :param query:
        :return:
        """
        try:
            resp = requests.get(
                url=f'{self.endpoint}/api/v1/query',
                params={'query': query}
            )
            resp.raise_for_status()
            data = resp.json()

            if data['status'] != 'success':
                raise QueryFailedException(f'query {query} failed')

            return data['data']['result']

        except requests.exceptions.RequestException as e:
            logger.error(f'request failed with code {e.response.status_code}')
        except Exception as e:
            logger.error(f'generic error: {e}')

    def get_all_metric(self):
        """
        Get all metrics from Prometheus server.
        :return: list of metrics.
        """
        try:
            resp = requests.get(
                url=f'{self.endpoint}/api/v1/label/__name__/values'
            )
            resp.raise_for_status()
            data = resp.json()

            if data['status'] != 'success':
                raise QueryFailedException(f'query failed')
            return data['data']
        except requests.exceptions.RequestException as e:
            logger.error(f'request failed with code {e.response.status_code}')
        except Exception as e:
            logger.error(f'generic error: {e}')
