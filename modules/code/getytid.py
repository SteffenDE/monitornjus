#!/usr/bin/env python
# Beilage zu MonitorNjus, 07.05.2015 (Version 0.7.1)
# http://stackoverflow.com/a/7936523

from urlparse import urlparse
from urlparse import parse_qs


def video_id(value):
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return ""
