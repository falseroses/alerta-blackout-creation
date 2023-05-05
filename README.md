# alerta-blackout-creation
Script for easier Alerta Blackouts creation. If you hate a lot of monotonous actions in Alerta UI when creating a blackout of 1 alert for multiple envs then that script for you :)

options:
  -h, --help                        show this help message and exit
  --env ENV [ENV ...]               Environment name. Examples: "PROD", "prod dev stage". Also you can specify "all" to select all ENVs
  --event EVENT, -e EVENT           Event name. Examples: "HighMemoryUsage", "KubeJobFailed"
  --resource RESOURCE, -r RESOURCE  Resource name. Examples: "prometheus-exporters-prometheus-es-exporter:9206", "ip-100-167-52-188.eu-west-3.compute.internal"
  --service SERVICE [SERVICE ...], -s SERVICE [SERVICE ...]
                                    Service name. Examples: "Nginx", "Elastic", "Nginx Elastic"
  --duration DURATION, -d DURATION  Blackout duration. Examples: "30m", "3h", "7d"
  --text TEXT, -t TEXT              Blackout reason. Examples: "Planned maintenance", "Known problem, JIRA-4291"

Examples:
alerta-blackout-creation.py --env all --event HighCpuUsage --resource ip-100-167-52-188.eu-west-3.compute.internal --duration 14d --text "Known problem, JIRA-4291"
alerta-blackout-creation.py --env prod dev stage -e IstioHighRequestLatency -d 3h -t "Planned maintenance"
alerta-blackout-creation.py --env prod -e "KubernetesApiClientErrors" -d 60d -t "JIRA-4107"

A script based on the Alerta API whose documentation can be found at this link: https://docs.alerta.io/api/reference.html#create-a-blackout