from gitea import *

def get_repo_commit_count(gitea, repo):
  page_endpoint = Repository.REPO_COMMITS % (repo.owner.username, repo.name)

  response = gitea.requests.get(gitea.url + "/api/v1" + page_endpoint + "?limit=1", headers=gitea.headers, params={})

  if 'X-Total' in response.headers:
    return int(response.headers.get('X-Total'))
  else:
    return 0

def gitea_export(app):
  metrics = dict()

  try:
    gitea = Gitea(app.config['MODULE_CONFIG']['url'], app.config['MODULE_CONFIG']['auth']['token'])
    gitea.get_version()
  except Exception as e:
    print("[WARNING] Unable to initiate connection with gitea.")
    return metrics

  try:
    metrics['users'] = gitea.get_users()
  except Exception as e:
    print(e)
    print("[WARNING] Unable to retrieve 'Gitea Users'.")
    metrics['users'] = dict()

  try:
    metrics['orgs'] = gitea.get_orgs()
  except Exception as e:
    print(e)
    print("[WARNING] Unable to retrieve 'Gitea Users'.")
    metrics['orgs'] = dict()


  metrics['repos'] = []

  try:
    for user in metrics['users']:
      metrics['repos'] += user.get_repositories()
  except Exception as e:
    print(e)
    print("[WARNING] Unable to retrieve 'Gitea Users repos'.")

  try:
    for org in metrics['orgs']:
      metrics['repos'] += org.get_repositories()
  except Exception as e:
    print(e)
    print("[WARNING] Unable to retrieve 'Gitea Orgs repos'.")

  try:
    for repo in metrics['repos']:
      repo.branches_count = len(repo.get_branches()) if not repo.empty else 0
      repo.commits_count = get_repo_commit_count(gitea, repo) if not repo.empty else 0
  except Exception as e:
    print(e)
    print("[WARNING] Unable to retrieve 'Gitea repos git infos'.")

  return metrics
