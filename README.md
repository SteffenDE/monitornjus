# monitornjus
## What is MonitorNjus?
Python WSGI application written for displaying various pages time-based or static on a monitor in the intranet (e.g. in a school).

## Alternative Versions:
### classic version ###
[monitornjus-classic](https://github.com/SteffenDE/monitornjus-classic)<br>
[mod_python](https://files.steffend.de/monitornjus/0.9.2/momp.zip)<br>
[Classic-ASP](https://files.steffend.de/monitornjus/0.9.2/moasp.zip)

## example
http://monitornjus.steffend.de

## Setup
### German
Was wird benötigt?
* Python 2.7
* Flask, Jinja2
* WSGI fähiger Webserver

#### Einstellungen
In der Datei "settings.py" werden mögliche Einstellungen vorgenommen.<br>
Sollte man einen Apache mit mod_wsgi einsetzen, dann muss man den Pfad in der Datei "apache.wsgi" verändern.