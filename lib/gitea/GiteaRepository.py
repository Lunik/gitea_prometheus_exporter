from types import SimpleNamespace

def get_repo_commit_count(gitea, repo):
  page_endpoint = Repository.REPO_COMMITS % (repo.owner.username, repo.name)

  response = gitea.requests.get(gitea.url + "/api/v1" + page_endpoint + "?limit=1", headers=gitea.headers, params={})

  if 'X-Total' in response.headers:
    return int(response.headers.get('X-Total'))
  else:
    return 0

class GiteaRepository(SimpleNamespace):
  def __init__(self, api, **args):
    self.api = api
    self.base_endpoint = "repos"
    SimpleNamespace.__init__(self, **args)

  def get_branches(self):
    res = self.api.requests_get("{base_endpoint}/{owner}/{name}/branches".format(
      base_endpoint=self.base_endpoint,
      name=self.name,
      owner=self.owner.username)
    )

    return res

  def get_commit_count(self):
    res = self.api.requests_get("{base_endpoint}/{owner}/{name}/commits".format(
      base_endpoint=self.base_endpoint,
      name=self.name,
      owner=self.owner.username),
      params=dict(limit=1),
      raw=True
    )

    if 'X-Total' in res.headers:
      return int(res.headers.get('X-Total'))
    else:
      return 0