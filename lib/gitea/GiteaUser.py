from types import SimpleNamespace

from .GiteaRepository import GiteaRepository

class GiteaUser(SimpleNamespace):
  def __init__(self, api, **args):
    self.api = api
    self.base_endpoint = "users"
    SimpleNamespace.__init__(self, **args)

  def get_repositories(self):
    res = self.api.requests_get("{base_endpoint}/{username}/repos".format(
      base_endpoint=self.base_endpoint,
      username=self.username)
    )

    repos = []

    for r in res:
      repo = GiteaRepository(self.api, **r)
      repo.owner = self

      repos.append(repo)

    return repos