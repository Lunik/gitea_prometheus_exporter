
from types import SimpleNamespace

from .GiteaRepository import GiteaRepository

class GiteaOrganization(SimpleNamespace):
  def __init__(self, api, **args):
    self.api = api
    self.base_endpoint = "orgs"
    SimpleNamespace.__init__(self, **args)

  def get_repositories(self):
    res = self.api.requests_get("{base_endpoint}/{name}/repos".format(
      base_endpoint=self.base_endpoint,
      name=self.username)
    )
    
    repos = []

    for r in res:
      repo = GiteaRepository(self.api, **r)
      repo.owner = self

      repos.append(repo)

    return repos