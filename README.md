# GPU Scanner

[Bestbuy Strategy Guide](https://docs.google.com/document/d/1EC3Li65gerZRG4gBiIs4rot-Bc4SceqWn413XGsOA4g/edit?usp=sharing)

A product page scanner designed to send out GPU stock drop notifications to one or both of the following endpoints:
 - a discord channel webhook: [GMU Channel Webhook](https://discordapp.com/api/webhooks/926904611082739733/H1ofplv4PUp_JVXhnao134nFiVBkK9wsWccvySIaF_BRsvJb2TU8a8RMcm4D9UHCjwhz)
 - an endpoint which executes a checkout bot

## Requirements

 - python-3.8.X
 - pip3

## Ubuntu Setup Guide

1. [Install python3](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/)
2. Install pip3: `sudo apt-get -y install python3-pip`
3. `git clone git@github.com:philip06/gpu-scalping-toolkit.git && cd gpu-scalping-toolkit`
4. `pip3 install -r requirements.txt`

## Usage Guide

##### Checkout Bot

Send bestbuy drop notification for a sku: 
 - `python3 gpu_scalping_toolkit.gpu_scanner.start_checkout SKU`

##### Bestbuy Scanning

Scanners will send a notification to our [GMU Channel Webhook](https://discordapp.com/api/webhooks/926904611082739733/H1ofplv4PUp_JVXhnao134nFiVBkK9wsWccvySIaF_BRsvJb2TU8a8RMcm4D9UHCjwhz)

Scan bestbuy product page for "High Demand Product" warning or "Add to Cart" button: 
 - `python3 gpu_scalping_toolkit.gpu_scanner.bestbuy_scanner SKU`

##### EVGA Scanning

Scan EVGA b stock page for specified product number to appear: 
 - `python3 -m gpu_scalping_toolkit.gpu_scanner.evga_scanner PN`

##### Bestbuy Checkout

Scan bestbuy product page for "High Demand Product" warning or "Add to Cart" button: 
 - `python3 -m gpu_scalping_toolkit.gpu_checkout_bot.bestbuy_checkout SKU`
