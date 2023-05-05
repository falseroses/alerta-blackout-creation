import argparse
import os
import sys
import requests


alerta_api_url = os.environ.get('ALERTA_API_URL')
alerta_api_token = os.environ.get('ALERTA_API_KEY')

# check if URL is specified
if alerta_api_url == None:
    print("ALERTA_API_URL environment variable is not set")
    sys.exit()
# check if token is specified
if alerta_api_token == None:
    print("ALERTA_API_KEY environment variable is not set")
    sys.exit()


def args_parser():
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog, max_help_position=36),
        description='Script for Alerta Blackouts creation',
        epilog='Examples:\n\
alerta-blackout-creation.py --env all --event HighCpuUsage --resource ip-100-167-52-188.eu-west-3.compute.internal --duration 14d --text "Known problem, JIRA-4291"\n\
alerta-blackout-creation.py --env prod dev stage -e IstioHighRequestLatency -d 3h -t "Planned maintenance"\n\
alerta-blackout-creation.py --env prod -e "KubernetesApiClientErrors" -d 60d -t "JIRA-4107"\n\n\
A script based on the Alerta API whose documentation can be found at this link: https://docs.alerta.io/api/reference.html#create-a-blackout')

    parser.add_argument('--env', nargs='+', required=True,
                        help='Environment name. Examples: "PROD", "prod dev stage". Also you can specify "all" to select all ENVs')
    parser.add_argument('--event', '-e', type=str, required=False,
                        help='Event name. Examples: "HighMemoryUsage", "KubeJobFailed"')
    parser.add_argument('--resource', '-r', type=str,
                        required=False, help='Resource name. Examples: "prometheus-exporters-prometheus-es-exporter:9206", "ip-100-167-52-188.eu-west-3.compute.internal"')
    parser.add_argument('--service', '-s', nargs='+',
                        required=False, default=[], help='Service name. Examples: "Nginx", "Elastic", "Nginx Elastic"')
    parser.add_argument('--duration', '-d', type=str, required=True,
                        help='Blackout duration. Examples: "30m", "3h", "7d"')
    parser.add_argument('--text', '-t', type=str, required=False,
                        help='Blackout reason. Examples: "Planned maintenance", "Known problem, JIRA-4291"')

    parsed_args = parser.parse_args()

    # parse the env argument to insert all envs in case 'all' value was entered
    if "all" in parsed_args.env:
        r = requests.get(alerta_api_url + '/environments', headers={
            'Authorization': 'Key {}'.format(alerta_api_token)}, verify=False, proxies={"http": "", "https": ""})
        if r.json()['status'] == 'error':
            print(
                f"{r.json()['status'].upper()}: {r.json()['message']}")
            sys.exit()
        parsed_args.env = []
        for environment in r.json()['environments']:
            parsed_args.env.append(environment['environment'])

    # parse the duration argument to support specifying value in minutes, hours, days
    parsed_args.duration = int(parsed_args.duration[:-1]) * 60 if parsed_args.duration[-1].lower() == "m" else \
        int(parsed_args.duration[:-1]) * 3600 if parsed_args.duration[-1].lower() == "h" else \
        int(parsed_args.duration[:-1]) * 86400 if parsed_args.duration[-1].lower() == "d" else \
        parsed_args.duration

    return parsed_args


def blackout_create(url, token, json):
    r = requests.post(url + '/blackout', headers={
                      'Authorization': 'Key {}'.format(token)}, json=json, verify=False, proxies={"http": "", "https": ""})

    if r.json()['status'] == 'ok':
        print(
            f"[{r.json()['blackout']['environment']}] Status: {r.json()['status'].upper()}")
    elif r.json()['status'] == 'error':
        print(
            f"[{json['environment']}] Status: {r.json()['status'].upper()}: {r.json()['message']}")
    else:
        print(
            f"[{json['environment']}] Status: {r.text}")


def main():
    # disable InsecureRequestWarning messages
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning)
    # assign values provided in a cli as parameters
    args = args_parser()

    for environment in args.env:
        blackout_json = {'environment': environment.lower(),
                         'event': args.event, 'resource': args.resource, 'duration': args.duration, 'text': args.text, 'service': args.service}
        blackout_create(alerta_api_url, alerta_api_token, blackout_json)


if __name__ == '__main__':
    main()
