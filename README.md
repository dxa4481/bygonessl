# BygoneSSL
This tool detects the two classes of vulnerability defined at [insecure.design](https://insecure.design)

The tool can be ran to detect either Man In The Middle, or Denial of Service

## Denial of Service
To run the tool in DoS mode, make sure you supply ALL the domains you own in the config file, otherwise the tool won't work. It is designed to report certs containing domains you don't own.

## Man in the Middle
To run the tool in MITM mode, make sure you accurately list the date you FIRST registered the domain, otherwise you will recieve inaccurate results.


## Install
Install with either
```
pip install -r requirements.txt
```

Or run the Dockerfile

## Setup
Set two environment variables for your facebook developer account:

```
export facebook_app_id=<id>
export facebook_app_token=<token>
```

Make sure you escape the pipe in the app token.

## Configure

Create a config file with the following:

```
{
    "domains": [
        {
            "domain": "insecure.design",
            "domainCreated": "2018-04-10T23:59:59+0000"
        }
    ],
    "bygoneDOS": true,
    "bygoneMITM": true
}
```

## Run the tool
Run the tool with the following:
```
python bygonessl.py --config <pathToJsonFile>
```
