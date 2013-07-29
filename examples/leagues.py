#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


es = everysport.Everysport(os.environ['EVERYSPORT_APIKEY'])

for league in es.leagues.hockey():
    print league








