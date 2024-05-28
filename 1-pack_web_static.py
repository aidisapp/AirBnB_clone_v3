#!/usr/bin/python3
"""
Fabric script that generates a tgz archive
from the contents of the web_static directory.
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static directory.
    Creates a versions directory if it does not exist and stores the archive
    with a timestamp in its filename. The archive includes the contents of
    the web_static directory.

    Returns:
        str: The path to the created archive file if successful,
        None otherwise.
    """
    # Get the current time formatted as YYYYMMDDHHMMSS
    time = datetime.utcnow().strftime('%Y%m%d%H%M%S')

    # Construct the archive file name
    file_name = "versions/web_static_{}.tgz".format(time)

    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p ./versions")

        # Create a tar gzipped archive
        local("tar --create --verbose -z --file={}./web_static".format(
            file_name))

        # Return the path to the created archive file
        return file_name
    except Exception as e:
        # Print the exception for debugging purposes
        print("An error occurred:", e)

        # Return None if an exception occurs
        return None
