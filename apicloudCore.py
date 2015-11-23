# coding: utf-8
import httplib
from config import apicloud_config
import config

__author__ = 'wenop'

from apicloud_python_sdk.dataCloud import DataCloud

dataCloud = DataCloud(apicloud_config.app_id, apicloud_config.app_key)
# r = dataCloud.createObject("StorageContainerInfo",
# {
# "address": "TJUT-A0",
# "num_in_group": "A08",
#         "status": "not-empty"
#     })


def __test_query():
    emptyContainers = dataCloud.doFilterSearch("StorageContainerInfo",
                                               filter='{"where":{"status":"empty"}}'
    )

    test0 = dataCloud.doFilterSearch("StorageContainerInfo",
                                     filter='{"where":{"id":"55fcdf311ae34dfb2c9d96da"}}'
    )

    for oneContainer in emptyContainers:
        print oneContainer

    if False:
        ret = dataCloud.doFilterSearch("PackageInfo",
                                       filter='{"include":"user"}'
        )
        print '===after search 1'
        print ret

        ret = dataCloud.doFilterSearch("user",
                                       filter='{"include":"PackageInfo"}'
        )
        print '===after search 2'
        print ret


def signUp_new_user(username, password, phone, email=None, ):
    dataCloud.createUser(
        {
            "username": username,
            "password": password,
            "phone": phone
            # "email": email,
        }
    )

def add_succVal(value):
    # 增加一条SuccIndicator
    dataCloud.createObject("SuccIndicator",
        {
            'value': value
        }
    )

def get_an_empty_container():
    emptyContainers = dataCloud.doFilterSearch("StorageContainerInfo",
                                               filter='{"where":{"status":"empty"}}'
    )
    if emptyContainers.__len__() > 0:
        return emptyContainers[0]
    return None

import json
def gen_storage_code():
    import hashlib, time

    m2 = hashlib.md5()
    m2.update("%s-UZU-WENOP" % (time.time(), ))
    return m2.hexdigest()

    # code = {
    #     "c": "r",   # command for receiver
    #     "code": m2.hexdigest()
    # }
    # return json.dumps(code)

def get_user_phone(userId):
    user = dataCloud.getObject("user", userId)
    if user:
        return user.get('username')
    return None

def store_package_in_container(package_id, containerInfo, deliver_id, onSuccVal):
    """
    :param package:
    :param container:
    :return: 返回StorageEntry
    """

    # 设置packageInfo的is_in_container=true
    packageInfo = dataCloud.getObject("PackageInfo", package_id)
    dataCloud.updateObject("PackageInfo", package_id,
       {'is_in_container': True}
    )

    code = gen_storage_code()

    # create a new StorageEntry
    newEntry = dataCloud.createObject("StorageEntry",
          {
              'receiver_id_that_storage_for': packageInfo['receiver_id'],
              'container_id_that_storage_in': containerInfo['id'],
              'package_id_that_storage_for': package_id,
              'code': code,
              'in_storage': True
          }
    )

    print '===after create newEntry'
    print newEntry

    # set container status
    dataCloud.updateObject("StorageContainerInfo", containerInfo['id'],
           {'status': 'not-empty'}
    )

    # 增加一条SuccIndicator
    add_succVal(onSuccVal)

    return newEntry, packageInfo['receiver_id']

def OLDstore_package_in_container(package, container):
    """

    :param package:
    :param container:
    :return: 返回StorageEntry
    """

    code = gen_storage_code()
    # create a new StorageEntry
    newEntry = dataCloud.createObject("StorageEntry",
                                      {
                                          'receiver_id_that_storage_for': package['receiver_id'],
                                          'container_id_that_storage_in': container['id'],
                                          'code': code,
                                          'in_storage': True
                                      })
    print '===after create newEntry'
    print newEntry

    # set container status
    dataCloud.updateObject("StorageContainerInfo", container['id'],
                           {'status': 'not-empty'}
    )

    return newEntry



    # # set relation container info
    # r = dataCloud.createRelationObject('StorageEntry', newEntry['id'],
    #     'container_that_storage_in', container
    # )
    # print '===after createRelationObject'
    # print r


def user_login(username, password):
    # user0 = dataCloud.doFilterSearch("user", '{"where":{"username":"t1"}}')
    user = dataCloud.userLogin(username, password)
    user = dataCloud.getUserInfo(user.get('userId'), user.get('id'))
    #print user
    return user


def new_package_for_user(user):
    newPackage = dataCloud.createObject("PackageInfo",
        {
            'receiver_id': user['id']
        })
    print '===after create packageInfo'
    print newPackage
    return newPackage


def draw_package_out(storageCode):
    err = "unknown err"
    storageItem = dataCloud.doFilterSearch("StorageEntry",
                                           filter='{"where":{"and":[{"code":"%s"},{"in_storage":"%s"}]}}'
                                                  % (storageCode, True))

    if storageItem.__len__() > 0:
        # set the entryItem status
        dataCloud.updateObject("StorageEntry", storageItem[0].get('id'),
                               {'in_storage': False}
        )

        # set the container status
        dataCloud.updateObject("StorageContainerInfo", storageItem[0].get('container_id_that_storage_in'),
                               {'status': 'empty'}
        )

        err = None
        return err, storageItem[0]
    else:
        err = "container not found"
    return err, None

#
def __p1():
    user = user_login('apicloud', '123456')
    package = new_package_for_user(user)
    container = get_an_empty_container()
    if not container:
        print 'no available container.'
        return
    entry = OLDstore_package_in_container(package, container)

    storageCode = entry.get('code')
    if storageCode:
        print 'storage code is:', storageCode
    else:
        print 'storage failed'


def __p2():
    ret = draw_package_out('f16d8ace6ceb767a636503f6167756ff')
    print ret


#p2()



