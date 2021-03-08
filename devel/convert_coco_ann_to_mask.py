###############################################################################
#
# Awet Haileslassie Gebrehiwot
# awethaileslassie21@gmail.com
#
###############################################################################

import json
import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import polygon
from pathlib import Path
from loguru import logger

class AnnotationTOmask:
    def __init__(self, annotation_file):
        # load dataset
        print('loading annotations ...')
        dataset = json.load(open(annotation_file, 'r'))
        print('annotations loaded!')

        # creating index
        print('creating index...')
        imgToAnns = {ann['image_id']: [] for ann in dataset['annotations']}
        anns =      {ann['id']:       [] for ann in dataset['annotations']}
        for ann in dataset['annotations']:
            imgToAnns[ann['image_id']] += [ann]
            anns[ann['id']] = ann

        imgs      = {im['id']: {} for im in dataset['images']}
        for img in dataset['images']:
            imgs[img['id']] = img

        cats = []
        catToImgs = []
        cats = {cat['id']: [] for cat in dataset['categories']}
        for cat in dataset['categories']:
            cats[cat['id']] = cat
        catToImgs = {cat['id']: [] for cat in dataset['categories']}
        for ann in dataset['annotations']:
            catToImgs[ann['category_id']] += [ann['image_id']]

        print('index created!')

        # create class members
        self.anns = anns
        self.imgToAnns = imgToAnns
        self.catToImgs = catToImgs
        self.imgs = imgs
        self.cats = cats
        self.dataset = dataset


    def getAnnIds(self, imgIds, catIds):
        """
        Get ann ids for given cats from all images
        """
        imgIds = imgIds if type(imgIds) == list else [imgIds]
        catIds = catIds if type(catIds) == list else [catIds]

        if not len(imgIds) == 0:
            anns = sum([self.imgToAnns[imgId] for imgId in imgIds if imgId in self.imgToAnns],[])
        else:
            anns = self.dataset['annotations']
        anns = anns if len(catIds)  == 0 else [ann for ann in anns if ann['category_id'] in catIds]
        ids = [ann['id'] for ann in anns]

        return ids

    def getCatIds(self, catNms=[], catIds=[]):
        """ 
        get integer array of cat ids for given cat names, given cat ids
        """
        if len(catNms) == len(catIds) == 0:
            cats = self.dataset['categories']
        else:
            print('+++++++++++++++++++++')
            cats = self.dataset['categories']
            cats = cats if len(catNms) == 0 else [cat for cat in cats if cat['name']          in catNms]
            cats = cats if len(catIds) == 0 else [cat for cat in cats if cat['id']            in catIds]
        ids = [cat['id'] for cat in cats]
        return ids

    def getImgIds(self, imgIds=[], catIds=[]):
        '''
        return an integer array of img ids for given ids with all given cats
        '''
        ids = set(imgIds)
        for catId in catIds:
            if len(ids) == 0:
                ids = set(self.catToImgs[catId])
            else:
                ids &= set(self.catToImgs[catId])
        return list(ids)

    def loadAnns(self, ids=[]):
        """
        loaded ann objects for integer ids specifying annotations
        """
        if type(ids) == list:
            return [self.anns[id] for id in ids]
        elif type(ids) == int:
            return [self.anns[ids]]

    def loadImgs(self, ids):
        """
        Load loaded img objects with the specified ids.
        """
        return [self.imgs[ids]]

    def getSeg(self, anns):
        """
        get annotations segmentatins
        """
        if len(anns) == 0:
            print('no annotations found')
            return 0

        S = []
        for ann in anns:
            for seg in ann['segmentation']:
                S.append(seg)
        return S

    def segToMask(self, S, h, w ):
         """
         Convert polygon segmentation to binary mask.
           S: polygon segmentation mask, h: target mask height, w: target mask width
         """
         M = np.zeros((h,w))
         for s in S:
             N = len(s)
             rr, cc = polygon(np.array(s[1:N:2]), np.array(s[0:N:2])) # (y, x)
             M[rr, cc] = 1
         return M


import sys
#coco_filename must include not only name of Coco file, but also it`s full direction (location) in your PC
#output_dir is used for controll output direction (location) in your PC
#output_type - type of "Save fail" of our program| results]
#organ - name of segmentation part rom what we want have mask ""
def CocoToMask(coco_filename, output_dir, organ, voxelsize_mm=None, output_type="JPG", show=False):
    #file_path = 'task_cell track 20200226-dii-30las-2pre1-2020_10_26_13_28_36-coco 1.0/annotations/instances_default.json'

    file_path = coco_filename
    cv_an = AnnotationTOmask(file_path)
    cv_an1=cv_an.getImgIds()
    print('getImgIds', cv_an1)
    # extract the region we want to mask ( Right Kidny,  Liver)

    #catIds = cv_an.getCatIds(catNms=['cell'])
    catIds = cv_an.getCatIds(catNms=[organ])
    #catIds = cv_an.getCatIds(catNms=['Liver'])
    #catIds = cv_an.getCatIds(catNms=['Left Kidney'])

    print('catIds', catIds)
    imgIds = cv_an.getImgIds(catIds=catIds)
    if len(imgIds) == 0:
        logger.warning(f"Label '{organ}' not found.")
    print('imgIds',imgIds)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # create empty files
    for imgName in cv_an.dataset['images']:
        print('imgName', imgName)
        M = np.zeros([imgName['width'], imgName['height']])
        image_path = Path(output_dir) / ('MaskOfPIG_'+str(imgName['file_name'])+'.'+output_type)
        logger.debug(image_path)
        plt.imsave(image_path, np.uint8(M), cmap = 'gray')

    # rewrite images with label
    for im in imgIds:
        print("iM", im)
        imgName = cv_an.loadImgs(im)[0]
        anns_ids = cv_an.getAnnIds(imgIds=imgName['id'], catIds=catIds)
        anns = cv_an.loadAnns(anns_ids)
        S = cv_an.getSeg(anns)
        M = cv_an.segToMask(S, imgName['width'], imgName['height'])
        plt.figure()
        plt.imshow(M)
        if show:
            plt.show()
        image_path = Path(output_dir) / ('MaskOfPIG_'+str(imgName['file_name'])+'.'+output_type)
        logger.debug(image_path)
        plt.imsave(image_path, np.uint8(M), cmap = 'gray')
    print('DOne')
