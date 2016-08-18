# vrealize-automation

This repository stores tools and and an SDK for VMware's vRealize Automation. Most of these are my first attempts at building something useful in python so expect bugs.

## Overview

A basic vRealize automation wrapper API called vralib. I'm sure someone somewhere will want to change this over time and that's fine. 

The library has few dependencies; you pretty much just need requests and the python standard library to get started. 

* requirements.txt - Library requirements for the vRA SDK. Should just need requests. 


## Sample Scripts

In the 'tool-samples' directory you'll find a series of helpful but simples tools that leverage this API to give you an idea of usage.

* get-catalog.py - Returns a prettytable formatted list of catalog names and IDs. The IDs can be used to request resources
* get-items.py - A script to pull a list of provisioned items.


## Setup 

Right now you'll just need the Python Requests library. 

    pip install requests

Import the library:

    import vralib

## Usage

### Log into the vRA instance

Use the vralib.Session.login() method to log into the vRealize automation server by creating an object with the .login @classmethod:

    vra = vralib.Session.login(username, password, cloudurl, tenant, ssl_verify=False)
    
Variables are defined as:
* username - a string containing the username that's logging into the environment. Typically it's user@domain
* password - a string containing the password for the specified user. 
* cloudurl - a string that contains the FQDN or IP address of the vrealize automation server. Don't include the https bit. The library will sort out specific URLs for you
* tenant - an optional string that contains the tenant you want to log into. If you leave this blank it will log into the default tenant
* ssl_verify - a boolean value that can be used to disable SSL verification. Helpful for when you don't have signed/trusted certificates (like a development environment) 

### Getting data from the API

Once logged in you can access various methods through the object. For example to retrieve all of the available catalog items:

    catalog = vra.get_catalogitem_byname(name)

Most returns are going to be python dictionaries. 

        
# Contributions welcome!


