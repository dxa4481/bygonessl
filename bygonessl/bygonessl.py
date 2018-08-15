import requests
import argparse
import dateutil.parser
import json
import datetime
import pytz
import os
import sys

try:
    app_id = os.environ["facebook_app_id"]
    app_token = os.environ["facebook_app_token"]
except KeyError:
    print("No facebook_app_id and facebook_app_token environment variables detected")
    sys.exit(1)


def bygoneMITMTest(domain, domainCreated):
    url = "https://graph.facebook.com/certificates?query={}&fields=cert_hash_sha256,not_valid_after,not_valid_before&access_token={}&limit=5000".format(domain, app_token)
    req = requests.get(url)
    results = req.json()
    now = datetime.datetime.now(pytz.UTC)
    for result in results["data"]:
        goodUntil = dateutil.parser.parse(result["not_valid_after"])
        certCreated = dateutil.parser.parse(result["not_valid_before"])
        if goodUntil > domainCreated and certCreated < domainCreated and goodUntil > now:
            print("BygoneSSL MITM with {} for cert {} good until {}".format(domain, result["cert_hash_sha256"], result["not_valid_after"]))


def bygoneDOSTest(domains):
    certs = []
    for domain in domains:
        url = "https://graph.facebook.com/certificates?query={}&fields=domains,not_valid_after,cert_hash_sha256&access_token={}&limit=5000".format(domain, app_token)
        now = datetime.datetime.now(pytz.UTC)
        req = requests.get(url)
        results = req.json()
        for result in results["data"]:
            goodUntil = dateutil.parser.parse(result["not_valid_after"])
            if goodUntil > now:
                certs.append((result["domains"], result["cert_hash_sha256"]))
    for cert in certs:
        for certDomain in cert[0]:
            certDomain = ".{}".format(certDomain.lower())
            domainIsOwned = False
            for ownedDomain in domains:
                ownedDomain = ".{}".format(ownedDomain.lower())
                if certDomain.endswith(ownedDomain):
                    domainIsOwned = True
                    break
            if not domainIsOwned:
                print("BygoneSSL DoS detected on a cert with {} domains. Cert sha256: {}".format(len(cert[0]), cert[1]))
                break

def main():
    parser = argparse.ArgumentParser(description='BygoneSSL configuration.')
    parser.add_argument("--config", dest="config", help="Path to the configuration file")
    args = parser.parse_args()
    if not args.config:
        print("Must specify config file with --config")
        sys.exit()
    with open(args.config, 'r') as f:
        config = json.loads(f.read())
    if config["bygoneDOS"]:
        domains = []
        for domain in config["domains"]:
            domains.append(domain["domain"])
        bygoneDOSTest(domains)
    if config["bygoneMITM"]:
        for domain in config["domains"]:
            bygoneMITMTest(domain["domain"], dateutil.parser.parse(domain["domainCreated"]))

if __name__ == '__main__':
    main()
