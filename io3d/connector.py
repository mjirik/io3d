#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Module for readin 3D dicom data
"""

# import funkcí z jiného adresáře
import sys
import os.path

# path_to_script = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(path_to_script, "../extern/pyseg_base/src"))
# sys.path.append(os.path.join(path_to_script,
#                              "../extern/py3DSeedEditor/"))
# ys.path.append(os.path.join(path_to_script, "../extern/"))
# mport featurevector

import logging
logger = logging.getLogger(__name__)
import argparse

__author__ = 'mjirik'

import paramiko

host = "147.228.47.162"                    #hard-coded
port = 22
transport = paramiko.Transport((host, port))

username = "lisa_sftp"                #hard-coded
username = "lisa_normal"                #hard-coded
password = "L154.sftp"                #hard-coded
# username = "mjirik"                #hard-coded
# password = "titanic"                #hard-coded
transport.connect(username = username, password = password)

sftp = paramiko.SFTPClient.from_transport(transport)

import sys
path = './' + sys.argv[1]    #hard-coded
localpath = sys.argv[1]
sftp.put(localpath, path)

sftp.close()
transport.close()
print('Upload done.')



