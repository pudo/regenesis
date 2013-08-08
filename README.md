ReGENESIS
=========

ReGENESIS is a toolkit and web service to facilitate access to German national 
and regional statistics. The Python scripts will query the bulk export API of 
GENESIS, a statistical database software and transform the exported data to a 
local database as well as to a set of plain text data dumps. 

For more information, read the [announce post](http://pudo.org/blog/2013/08/08/regenesis.html).


Usage
-----

After installation, ReGENESIS is controlled through a series of script commands
in regenesis/manage.py:

    # Download all bulk data from the regional statistics database to a local cache:
    $ python regenesis/manage.py fetch -u regional

    # Load the bulk data cache into a local database:
    $ python regenesis/manage.py load -u regional 

    # Generate static data and HTML output:
    $ python regenesis/manage.py freezedata
    $ python regenesis/manage.py freezehtml

For debugging purposes, the Flask application used to generate the HTML interface
can also be executed directly: 

    $ python regenesis/manage.py runserver

If you want to use the database directly for querying the data, check out ``queries.sql`` 
to see some sample SQL. 


Installation
------------

ReGENESIS requires only an external database, such as Postgres to be available on 
your machine.

The software should always be installed inside a Python virtual environment. To set 
it up, execute these instructions: 

    virtualenv pyenv
    source pyenv/bin/activate
    git clone git@github.com:pudo/regenesis.git
    pip install -r regenesis/requirements.txt

Afterwards, you can override ReGENESIS' default settings by creating a local
configuration file and exporting its path to the environment each time before you 
run the software.

    cp regenesis/regenesis/default_settings.py settings.py
    # edit the file to set relevant values like DB strings.
    REGENESIS_SETTINGS=`pwd`/settings.py
    export REGENESIS_SETTINGS

To use the sync.sh script uploading data to S3, you'll need to create an s3cmd 
configuration file in the local directory. 


Contributions and License
-------------------------

ReGENESIS is licensed under the conditions of the MIT license. Any contributions 
to the code base are appreciated, please just submit a pull request or open an 
issue to discuss your idea. 