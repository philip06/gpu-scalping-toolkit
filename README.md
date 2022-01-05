# GPU Scanner

A product page scanner designed to send out GPU stock drop notifications to one or both of the following endpoints:
 - a discord channel webhook: [GMU Channel Webhook](https://discordapp.com/api/webhooks/926904611082739733/H1ofplv4PUp_JVXhnao134nFiVBkK9wsWccvySIaF_BRsvJb2TU8a8RMcm4D9UHCjwhz)
 - an endpoint which executes a checkout bot

## Requirements

 - python-3.8.X
 - pip3

## Ubuntu Setup Guide

1. [Install python3](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/)
2. Install pip3: `sudo apt-get -y install python3-pip`
3. `git clone git@github.com:philip06/gpu-scanner.git && cd gpu-scanner`
4. `python3 -m pip install -r requirements.txt`

## Usage Guide

##### Discord Notification

Currently will send a notification to our [GMU Channel Webhook](https://discordapp.com/api/webhooks/926904611082739733/H1ofplv4PUp_JVXhnao134nFiVBkK9wsWccvySIaF_BRsvJb2TU8a8RMcm4D9UHCjwhz)

Send bestbuy drop notification for a sku: 
 - `python3 discord_bot.py`

##### Bestbuy Scanning

Scan bestbuy product page for "High Demand Product" warning or "Add to Cart" button: 
 - `python3 bestbuy_scanner.py SKU`

##### EVGA Scanning

Scan EVGA b stock page for specified product number to appear: 
 - `python3 evga_scanner.py PN`
