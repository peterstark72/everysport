#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import everysport


EVERYSPORT_APIKEY = os.environ['EVERYSPORT_APIKEY'] 


def main():

    api = everysport.Api(EVERYSPORT_APIKEY)

    results = api.get_results(everysport.ALLSVENSKAN)

    print results._asjson()



if __name__ == '__main__':
    main()