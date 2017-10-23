#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import zipfile
import subprocess
import sys
import glob
# import traceback

import logging
import numpy as np

logger = logging.getLogger(__name__)

import argparse

if sys.version_info < (3, 0):
    import urllib as urllibr
else:
    import urllib.request as urllibr


# import funkcí z jiného adresáře
import os.path

path_to_script = os.path.dirname(os.path.abspath(__file__))


def submodule_update():
    # update submodules codes
    print ('Updating submodules')
    try:
        # import pdb; pdb.set_trace()
        subprocess.call('git submodule update --init --recursive', shell=True)
        # subprocess.call('git submodule update --init --recursive')

    except:
        print ('Probem with git submodules')


def check_python_architecture(pythondir, target_arch_str):
    """
    functions check architecture of target python
    """
    pyth_str = subprocess.check_output(
        [pythondir + 'python', '-c',
         'import platform; print platform.architecture()[0]'])
    if pyth_str[:2] != target_arch_str:
        raise Exception(
            "Wrong architecture of target python. Expected arch is"
            + target_arch_str)


def remove(local_file_name):
    try:
        os.remove(local_file_name)
    except Exception as e:
        print ("Cannot remove file '" + local_file_name + "'. Please remove\
        it manually.")
        print (e)


def downzip(url, destination='./sample_data/'):
    """
    Download, unzip and delete.
    """

    # url = "http://147.228.240.61/queetech/sample-data/jatra_06mm_jenjatra.zip"
    logmsg = "downloading from '" + url + "'"
    print logmsg
    logger.debug(logmsg)
    local_file_name = os.path.join(destination, 'tmp.zip')
    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall(destination)
    remove(local_file_name)


# you can get hash from command line with:
#  python imtools/sample_data.py -v sliver_training_001

# vessels.pkl nejprve vytvoří prázný adresář s názvem vessels.pkl, pak jej při rozbalování zase smaže
data_urls= {
    "head": ["http://147.228.240.61/queetech/sample-data/head.zip", "89e9b60fd23257f01c4a1632ff7bb800", "matlab"] ,
    "jatra_06mm_jenjatra": ["http://147.228.240.61/queetech/sample-data/jatra_06mm_jenjatra.zip", "jatra_06mm_jenjatra/*.dcm"],
    "jatra_5mm": ["http://147.228.240.61/queetech/sample-data/jatra_5mm.zip", '1b9039ffe1ff9af9caa344341c8cec03', "jatra_06mm/*.dcm"],
    "exp": ["http://147.228.240.61/queetech/sample-data/exp.zip", '74f2c10b17b6bd31bd03662df6cf884d'],
    "sliver_training_001": ["http://147.228.240.61/queetech/sample-data/sliver_training_001.zip","d64235727c0adafe13d24bfb311d1ed0","liver*001.*"],
    "volumetrie": ["http://147.228.240.61/queetech/sample-data/volumetrie.zip","6b2a2da67874ba526e2fe00a78dd19c9"],
    "vessels.pkl": ["http://147.228.240.61/queetech/sample-data/vessels.pkl.zip","698ef2bc345bb616f8d4195048538ded"],
    "biodur_sample": ["http://147.228.240.61/queetech/sample-data/biodur_sample.zip","d459dd5b308ca07d10414b3a3a9000ea"],
    "gensei_slices": ["http://147.228.240.61/queetech/sample-data/gensei_slices.zip", "ef93b121add8e4a133bb086e9e6491c9"],
    "exp_small": ["http://147.228.240.61/queetech/sample-data/exp_small.zip", "0526ba8ea363fe8b5227f5807b7aaca7"],
    "vincentka": ["http://147.228.240.61/queetech/vincentka.zip", "a30fdabaa39c5ce032a3223ed30b88e3"],
    "vincentka_sample": ["http://147.228.240.61/queetech/sample-data/vincentka_sample.zip"],
    "donut": "http://147.228.240.61/queetech/sample-data/donut.zip",
    # není nutné pole, stačí jen string
    # "exp_small": "http://147.228.240.61/queetech/sample-data/exp_small.zip",
}

def get_sample_data(data_label=None, destination_dir="."):
    """
    Same as get() due to back compatibility
    :param data_label:
    :param destination_dir:
    :return:
    """
    get(data_label=data_label, destination_dir=destination_dir)

def get(data_label=None, destination_dir="."):
    """
    Download sample data by data label. Labels can be listed by sample_data.data_urls.keys()
    :param data_label: label of data. If it is set to None, all data are downloaded
    :param destination_dir: output dir for data
    :return:
    """
    try:
        os.mkdir(destination_dir)
    except:
        pass
    if data_label is None:
        data_label=data_urls.keys()

    if type(data_label) == str:
        data_label = [data_label]

    for label in data_label:
        # make all data:url have length 3
        data_url = data_urls[label]
        if type(data_url) == str:
            # back compatibility
            data_url = [data_url]
        data_url.extend([None, None])
        data_url = data_url[:3]
        url, expected_hash, hash_path = data_url

        if hash_path is None:
            hash_path = label

        try:
            computed_hash = checksum(os.path.join(destination_dir, hash_path))
        except:
            # there is probably no checksumdir module
            logger.warning("problem with sample_data.checksum()")
            computed_hash = None

        logger.info("dataset '" + label + "'")
        logger.info("expected hash: '" + str(expected_hash) + "'")
        logger.info("computed hash: '" + str(computed_hash) + "'")
        if (computed_hash is not None) and (expected_hash == computed_hash):
            logger.info("match ok - no download needed")
        else:
            logger.info("downloading")
            downzip(url, destination=destination_dir)
            logger.info("finished")
            downloaded_hash = checksum(os.path.join(destination_dir, hash_path))
            logger.info("downloaded hash: '" + str(downloaded_hash) + "'")
            if downloaded_hash != expected_hash:
                logger.warning("downloaded hash is different from expected hash\n" + \
                    "expected hash: '" + str(expected_hash) + "'\n" + \
                    "downloaded hash: '" + str(downloaded_hash) + "'\n")

def checksum(path, hashfunc='md5'):
    """
    Return checksum given by path. Wildcards can be used in check sum. Function is strongly
    dependent on checksumdir package by 'cakepietoast'.

    :param path:
    :param hashfunc:
    :return:
    """
    import checksumdir
    hash_func = checksumdir.HASH_FUNCS.get(hashfunc)
    if not hash_func:
        raise NotImplementedError('{} not implemented.'.format(hashfunc))

    if os.path.isdir(path):
        return checksumdir.dirhash(path, hashfunc=hashfunc)

    hashvalues = []
    path_list = glob.glob(path)
    logger.debug("path_list " + str(path_list))
    for path in path_list:
        if os.path.isfile(path):
            hashvalues.append(checksumdir._filehash(path, hashfunc=hash_func))
    logger.debug(str(hashvalues))
    hash = checksumdir._reduce_hash(hashvalues, hashfunc=hash_func)
    return hash

def donut():
    """
    Generate donut like shape with stick inside

    :return: datap with keys data3d, segmentation and voxelsize_mm
    """
    import numpy as np
    segmentation = np.zeros([20, 30, 40])
    # generate test data
    segmentation[6:10, 7:24, 10:37] = 1
    segmentation[6:10, 7, 10] = 0
    segmentation[6:10, 23, 10] = 0
    segmentation[6:10, 7, 36] = 0
    segmentation[6:10, 23, 36] = 0
    segmentation[2:18, 12:19, 18:28] = 2

    data3d = segmentation * 100 + np.random.random(segmentation.shape) * 30
    voxelsize_mm=[3,2,1]

    import io3d
    datap = {
        'data3d': data3d,
        'segmentation': segmentation,
        'voxelsize_mm': voxelsize_mm
    }
    # io3d.write(datap, "donut.pklz")
    return datap

def get_sample_data_old():
    # download sample data
    print('Downloading sample data')
    try:
        os.mkdir('sample_data')
    except:
        pass

    # Puvodni URL z mathworks
    # url =  "http://www.mathworks.com/matlabcentral/fileexchange/2762-dicom-example-files?download=true"
    # url = "http://www.mathworks.com/includes_content/domainRedirect/domainRedirect.html?uri=http%3A%2F%2Fwww.mathworks.com%2Fmatlabcentral%2Ffileexchange%2F2762-dicom-example-files%3Fdownload%3Dtrue%26nocookie%3Dtrue"
    url = "http://147.228.240.61/queetech/sample-data/head.zip"
    local_file_name = './sample_data/head.zip'

    urlobj = urllibr.urlopen(url)
    url = urlobj.geturl()
    urllibr.urlretrieve(url, local_file_name)

    datafile = zipfile.ZipFile(local_file_name)
    #datafile.setpassword('queetech')
    datafile.extractall('./sample_data/')
    remove(local_file_name)

# get jatra_06mm_jenjatra

    # url = "http://147.228.240.61/queetech/sample-data/jatra_06mm_jenjatraplus.zip"
    # local_file_name = './sample_data/jatra_06mm_jenjatraplus.zip'
    url = "http://147.228.240.61/queetech/sample-data/jatra_06mm_jenjatra.zip"
    local_file_name = './sample_data/jatra_06mm_jenjatra.zip'
    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall('./sample_data/')
    remove(local_file_name)
# get jatra 5mm
    url = "http://147.228.240.61/queetech/sample-data/jatra_5mm.zip"
    local_file_name = './sample_data/jatra_5mm.zip'

    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall('./sample_data/')
    remove(local_file_name)

# get experiment data
    url = "http://147.228.240.61/queetech/sample-data/exp.zip"
    local_file_name = './sample_data/exp.zip'
    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall('./sample_data/')
    remove(local_file_name)
# get sliver sample
    url = "http://147.228.240.61/queetech/sample-data/sliver_training_001.zip"
    local_file_name = './sample_data/sliver_training_001.zip'
    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall('./sample_data/')
    remove(local_file_name)

# get volumetry sample
    url = "http://147.228.240.61/queetech/sample-data/volumetrie.zip"
    local_file_name = './sample_data/volumetrie.zip'
    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall('./sample_data/')
    remove(local_file_name)

# get organ.pkl and vessels.pkl
    url = "http://147.228.240.61/queetech/sample-data/organ.pkl.zip"
    local_file_name = './sample_data/organ.pkl.zip'
    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall('./sample_data/')
    remove(local_file_name)

    url = "http://147.228.240.61/queetech/sample-data/vessels.pkl.zip"
    local_file_name = './sample_data/vessels.pkl.zip'
    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall('./sample_data/')
    remove(local_file_name)

# get biodur samples
    url = "http://147.228.240.61/queetech/sample-data/biodur_sample.zip"
    local_file_name = './sample_data/biodur_sample.zip'
    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall('./sample_data/')
    remove(local_file_name)

# get gensei samples
    url = "http://147.228.240.61/queetech/sample-data/gensei_slices.zip"
    local_file_name = './sample_data/gensei_slices.zip'
    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall('./sample_data/')
    remove(local_file_name)

    downzip("http://147.228.240.61/queetech/sample-data/exp_small.zip")



def download_and_run(url, local_file_name):
    urllibr.urlretrieve(url, local_file_name)
    subprocess.call(local_file_name)


def get_conda_path():
    """
    Return anaconda or miniconda directory
    :return: anaconda directory
    """

    dstdir = ''
    # try:
    import subprocess
    import re
    # cond info --root work only for root environment
    # p = subprocess.Popen(['conda', 'info', '--root'], stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
    p = subprocess.Popen(['conda', 'info', '-e'], stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
    out, err = p.communicate()

    dstdir = out.strip()
    dstdir = re.search("\*(.*)\n", dstdir).group(1).strip()
    # except:
    #     import traceback
    #     traceback.print_exc()

    # import os.path as op
    # conda_pth = op.expanduser('~/anaconda/bin')
    # if not op.exists(conda_pth):
    #     conda_pth = op.expanduser('~/miniconda/bin')
    # return conda_pth
    return dstdir

def generate(size = 100, liver_intensity=100, noise_intensity=20, portal_vein_intensity=130, spleen_intensity=90):
    boundary = int(size/4)
    voxelsize_mm = [1.0, 1.5, 1.5]
    slab = {
        'liver': 1,
        'porta': 2,
        'spleen': 17
    }

    segmentation = np.zeros([size, size, size], dtype=np.uint8)
    segmentation[boundary:-boundary, boundary:-2*boundary, 2*boundary:-boundary] = 1
    segmentation[:, boundary*2:boundary*2+5, boundary*2:boundary*2+5] = 2
    segmentation[:, boundary*2:boundary*2+5, boundary*2:boundary*2+5] = 2
    segmentation[:, -5:, -boundary:] = 17


    seeds = np.zeros([size, size, size], dtype=np.uint8)
    seeds[
    boundary + 1 : boundary + 4,
    boundary + 1 : boundary + 4,
    2 * boundary + 1 : 2 * boundary + 4
    ] = 1

    noise = (np.random.random(segmentation.shape) * noise_intensity).astype(np.int)
    data3d = np.zeros(segmentation.shape, dtype=np.int)
    data3d [segmentation == 1] = liver_intensity
    data3d [segmentation == 2] = portal_vein_intensity
    data3d [segmentation == 17] = spleen_intensity
    data3d += noise


    datap = {
        'data3d': data3d,
        'segmentation': segmentation,
        'voxelsize_mm': voxelsize_mm,
        'seeds': seeds,
        'slab': slab
    }
    return datap


def file_copy_and_replace_lines(in_path, out_path):
    import shutil
    import fileinput

    # print "path to script:"
    # print path_to_script
    lisa_path = os.path.abspath(path_to_script)

    shutil.copy2(in_path, out_path)
    conda_path = get_conda_path()

    # print 'ip ', in_path
    # print 'op ', out_path
    # print 'cp ', conda_path
    for line in fileinput.input(out_path, inplace=true):
        # coma on end makes no linebreak
        line = line.replace("@{lisa_path}", lisa_path)
        line = line.replace("@{conda_path}", conda_path)
        print line


def make_icon():
    import platform

    system = platform.system()
    if system == 'Darwin':
        # MacOS
        __make_icon_osx()
        pass
    elif system == "Linux":
        __make_icon_linux()


def __make_icon_osx():
    home_path = os.path.expanduser('~')
    in_path = os.path.join(path_to_script, "applications/lisa_gui")
    dt_path = os.path.join(home_path, "Desktop")
    subprocess.call(['ln', '-s', in_path, dt_path])


def __make_icon_linux():

    in_path = os.path.join(path_to_script, "applications/lisa.desktop.in")
    in_path_ha = os.path.join(path_to_script, "applications/ha.desktop.in")
    print "icon input path:"
    print in_path, in_path_ha

    home_path = os.path.expanduser('~')

    if os.path.exists(os.path.join(home_path, 'Desktop')):
        desktop_path = os.path.join(home_path, 'Desktop')
    elif os.path.exists(os.path.join(home_path, 'Plocha')):
        desktop_path = os.path.join(home_path, 'Plocha')
    else:
        print "Cannot find desktop directory"
        desktop_path = None

    # copy desktop files to desktop
    if desktop_path is not None:
        out_path = os.path.join(desktop_path, "lisa.desktop")
        out_path_ha = os.path.join(desktop_path, "ha.desktop")

        # fi = fileinput.input(out_path, inplace=True)
        print "icon output path:"
        print out_path, out_path_ha
        file_copy_and_replace_lines(in_path, out_path)
        file_copy_and_replace_lines(in_path_ha, out_path_ha)

    # copy desktop files to $HOME/.local/share/applications/
    # to be accesable in application menu (Linux)
    local_app_path = os.path.join(home_path, '.local/share/applications')
    if os.path.exists(local_app_path) and os.path.isdir(local_app_path):
        out_path = os.path.join(local_app_path, "lisa.desktop")

        out_path_ha = os.path.join(local_app_path, "ha.desktop")

        print "icon output path:"
        print out_path, out_path_ha
        file_copy_and_replace_lines(in_path, out_path)
        file_copy_and_replace_lines(in_path_ha, out_path_ha)

    else:
        print "Couldnt find $HOME/.local/share/applications/."


def main():
    logger = logging.getLogger()

    logger.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    #logger.debug('input params')

    # input parser
    parser = argparse.ArgumentParser(
        description=
        "Download sample data")
    parser.add_argument(
        "labels", metavar="N", nargs="+",
        default=None,
        help='Get sample data')
    parser.add_argument(
        '-l', '--print_labels', action="store_true",
        default=False,
        help='print all available labels')
    parser.add_argument(
        '-v', '--verbatim', action="store_true",
        default=False,
        help='more messages')
    parser.add_argument(
        '-d', '--debug', # action="store_true",
        default=None,
        help='set debug level')
    parser.add_argument(
        '-o', '--destination_dir',
        default=".",
        help='set output directory')

    args = parser.parse_args()


#    if args.get_sample_data == False and args.install == False and args.build_gco == False:
## default setup is install and get sample data
#        args.get_sample_data = True
#        args.install = True
#        args.build_gco = False
    if args.verbatim:
        # logger.setLevel(logging.DEBUG)
        logger.setLevel(logging.INFO)
    if args.debug is not None:
        logger.setLevel(int(args.debug))

    get(args.labels, destination_dir=args.destination_dir)

                #submodule_update()


if __name__ == "__main__":
    main()
