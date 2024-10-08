# -*- coding: utf-8 -*-
"""
    pyGarufa.components.globals

    Defines library global variables
"""

import ssl

from .enums import Environment
from collections import defaultdict

# Default environment used if None environment is specified.
default_environment = None

# Environment specific configuration.
environment_config = {
    Environment.REMARKET: {
        "url": "https://api.remarkets.primary.com.ar/",
        "ws": "wss://api.remarkets.primary.com.ar/",
        "ssl": True,
        "proxies": None,
        "rest_client": defaultdict(dict),
        "ws_client": defaultdict(dict),
        "token": defaultdict(dict),
        "user": defaultdict(dict),
        "password": defaultdict(dict),
        "account": defaultdict(dict),
        "initialized": False,
        "proprietary": "PBCP",
        "heartbeat": 30,
        "ssl_opt": None
    },
    Environment.LIVE: {
        "url": "https://api.primary.com.ar/",
        "ws": "wss://api.primary.com.ar/",
        "ssl": True,
        "proxies": None,
        "rest_client": defaultdict(dict),
        "ws_client": defaultdict(dict),
        "token": defaultdict(dict),
        "user": defaultdict(dict),
        "password": defaultdict(dict),
        "account": defaultdict(dict),
        "initialized": False,
        "proprietary": "api",
        "heartbeat": 30,
        "ssl_opt": None
    },
    Environment.VETA: {
        "url": "https://api.veta.xoms.com.ar/",
        "ws": "wss://api.veta.xoms.com.ar/",
        "ssl": True,
        "proxies": None,
        "rest_client": defaultdict(dict),
        "ws_client": defaultdict(dict),
        "token": defaultdict(dict),
        "user": defaultdict(dict),
        "password": defaultdict(dict),
        "account": defaultdict(dict),
        "initialized": False,
        "proprietary": "api",
        "heartbeat": 30,
        "ssl_opt": None
    },
    Environment.RABELLO: {
        "url": "https://api.rabello.xoms.com.ar/",
        "ws": "wss://api.rabello.xoms.com.ar/",
        "ssl": True,
        "proxies": None,
        "rest_client": defaultdict(dict),
        "ws_client": defaultdict(dict),
        "token": defaultdict(dict),
        "user": defaultdict(dict),
        "password": defaultdict(dict),
        "account": defaultdict(dict),
        "initialized": False,
        "proprietary": "api",
        "heartbeat": 30,
        "ssl_opt": None
    },
    Environment.BULL: {
        "url": "https://api.bull.xoms.com.ar/",
        "ws": "wss://api.bull.xoms.com.ar/",
        "ssl": True,
        "proxies": None,
        "rest_client": defaultdict(dict),
        "ws_client": defaultdict(dict),
        "token": defaultdict(dict),
        "user": defaultdict(dict),
        "password": defaultdict(dict),
        "account": defaultdict(dict),
        "initialized": False,
        "proprietary": "api",
        "heartbeat": 30,
        "ssl_opt": None
    }
}
