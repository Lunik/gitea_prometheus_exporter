import requests
from types import SimpleNamespace

from .GiteaAPI import GiteaAPI
from .GiteaUser import GiteaUser
from .GiteaOrganization import GiteaOrganization


class GiteaVersion(SimpleNamespace):
  pass

class Gitea:
  def __init__(self, url, token):
    self.api = GiteaAPI(url, token)

  def get_version(self):
    return GiteaVersion(**self.api.requests_get("version"))

  def get_users(self):
    res = self.api.requests_get("admin/users")
    return [GiteaUser(self.api, **u) for u in res]

  def get_orgs(self):
    res = self.api.requests_get("admin/orgs")
    return [GiteaOrganization(self.api, **o) for o in res]