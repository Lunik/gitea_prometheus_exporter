import requests
import json

class GiteaAPI:
  def __init__(self, base_url, token, api_version="v1"):
    self.base_url = "{url}/api/{version}".format(url=base_url, version=api_version)
    self.headers = {
      "Authorization": "token {}".format(token),
      "Content-type": "application/json",
    }

    self.requests = requests.Session()

  @staticmethod
  def parse_response(result):
    if result.text and len(result.text) > 3:
        return json.loads(result.text)
    return {}

  def _get_url(self, endpoint):
    return "{url}/{endpoint}".format(url=self.base_url, endpoint=endpoint)

  def requests_get(self, endpoint, params={}, raw=False):
    params = params.copy()
    response = self.requests.get(self._get_url(endpoint), headers=self.headers, params=params)

    print(response.url)

    if raw:
      return response

    if response.status_code == 204:
      return None

    if response.status_code not in [200, 201]:
      message = "Received status code: %s (%s)" % (
        response.status_code,
        response.url,
      )

      if response.status_code in [404]:
          raise Exception(message)

      if response.status_code in [403]:
          raise Exception(
              "Unauthorized: %s - Check your permissions and try again! (%s)"
              % (response.url, message)
          )

      if response.status_code in [409]:
          raise Exception(message)

      raise Exception(message)

    result = self.parse_response(response)

    if "X-Total-Count" in response.headers and len(result) > 0:
      if "page" in params:
        params['page'] += 1
      else:
        params['page'] = 2

      result += self.requests_get(endpoint, params=params)

    return result