# Prometheus export for Gitea

## What does it do ?

Export repositories metrics with prometheus format.

### Metrics exported

| Metric             | Labels                                  | Type  |
|:-------------------|:----------------------------------------|:------|
| user               | ['username', 'full_name']               | Gauge |
| org                | ['username', 'full_name', 'visibility'] | Gauge |
| repo               | ['name', 'owner']                       | Gauge |
| repo_size          | ['name', 'owner', 'unit']               | Gauge |
| repo_empty         | ['name', 'owner']                       | Gauge |
| repo_archived      | ['name', 'owner']                       | Gauge |
| repo_stars         | ['name', 'owner']                       | Gauge |
| repo_commits       | ['name', 'owner']                       | Gauge |
| repo_branches      | ['name', 'owner']                       | Gauge |
| repo_forks         | ['name', 'owner']                       | Gauge |
| repo_issues        | ['name', 'owner']                       | Gauge |
| repo_pull_requests | ['name', 'owner']                       | Gauge |

## Build it

```shell
$ docker build -t gitea-exporter:latest .
```

## Run it

Take a look at the [Docker compose file](docker-compose.yml)

## Sources

[Gitea](https://github.com/go-gitea/gitea)

Thanks to [Langenfeld/py-gitea](https://github.com/Langenfeld/py-gitea)

## Disclaimer

This software was built by me, for my usages. It may not work "as it is" in your setup.