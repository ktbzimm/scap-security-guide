#!/usr/bin/python2

#
# create_sockets_disabled.py
#   automatically generate checks for disabled sockets.
#
# NOTE: The file 'template_socket_disabled' should be located in the same
# working directory as this script. The template contains the following tags
# that *must* be replaced successfully in order for the checks to work.
#
# SOCKETNAME - the name of the socket that should be disabled
# PACKAGENAME - the name of the package that installs the socket
#

import sys
import re

from template_common import *

def output_checkfile(socketinfo):
    # get the items out of the list
    socketname, packagename = socketinfo

    file_content = load_modified(
        "./template_socket_disabled",
        { "SOCKETNAME":  socketname }
    )

    if packagename:
        file_from_template(
            "./template_socket_disabled",
            {
                "SOCKETNAME":  socketname,
                "PACKAGENAME": packagename
            },
            "./output/oval/socket_{0}_disabled.xml", socketname
        )

    else:
        file_from_template(
            "./template_socket_disabled",
            {
                "SOCKETNAME":  socketname,
            },
            regex_dict = {
                "\n\s*<criteria.*>\n\s*<extend_definition.*/>": "",
                "\s*</criteria>\n\s*</criteria>": "\n    </criteria>"
            }
            filename_format = "./output/oval/socket_{0}_disabled.xml",
            filename_value = socketname
        )

def main():
    if len(sys.argv) < 2:
        print ("Provide a CSV file containing lines of the format: " +
               "socketname,packagename")
        sys.exit(1)

    filename = sys.argv[1]
    csv_map(filename, output_checkfile, skip_comments = True)

    sys.exit(0)


if __name__ == "__main__":
    main()
