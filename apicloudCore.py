# coding: utf-8
from config import apicloud_config

__author__ = 'wenop'

from apicloud_python_sdk.dataCloud import DataCloud

dataCloud = DataCloud(apicloud_config.app_id, apicloud_config.app_key)
# r = dataCloud.createObject("StorageContainerInfo",
#     {
#         "address": "TJUT-A0",
#         "num_in_group": "A08",
#         "status": "not-empty"
#     })


def __test_query():
    emptyContainers = dataCloud.doFilterSearch("StorageContainerInfo",
            filter= '{"where":{"status":"empty"}}'
        )

    test0 = dataCloud.doFilterSearch("StorageContainerInfo",
            filter= '{"where":{"id":"55fcdf311ae34dfb2c9d96da"}}'
        )

    for oneContainer in emptyContainers:
        print oneContainer


    if False:
        ret = dataCloud.doFilterSearch("PackageInfo",
            filter= '{"include":"user"}'
        )
        print '===after search 1'
        print ret

        ret = dataCloud.doFilterSearch("user",
            filter= '{"include":"PackageInfo"}'
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

def get_an_empty_container():
    emptyContainers = dataCloud.doFilterSearch("StorageContainerInfo",
        filter= '{"where":{"status":"empty"}}'
    )
    if emptyContainers.__len__()>0:
        return emptyContainers[0]
    return None


def gen_storage_code():
    import hashlib, time
    m2 = hashlib.md5()
    m2.update("%s-UZU-WENOP" % (time.time(), ))
    return m2.hexdigest()


def store_package_in_container(package, container):

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
    storageItem = dataCloud.doFilterSearch("StorageEntry",
        filter= '{"where":{"and":[{"code":"%s"},{"in_storage":"%s"}]}}' % (storageCode, True)
    )
    if storageItem.__len__()>0:
        # set the entryItem status
        dataCloud.updateObject("StorageEntry", storageItem[0].get('id'),
            {'in_storage': False}
        )

        # set the container status
        dataCloud.updateObject("StorageContainerInfo", storageItem[0].get('container_id_that_storage_in'),
            {'status': 'empty'}
        )
        return storageItem[0]
    return None



#
def p1():
    user = user_login('apicloud', '123456')
    package = new_package_for_user(user)
    container = get_an_empty_container()
    if not container:
        print 'no available container.'
        return
    entry = store_package_in_container(package, container)

    storageCode = entry.get('code')
    if storageCode:
        print 'storage code is:', storageCode
    else:
        print 'storage failed'


def p2():
    ret = draw_package_out('f16d8ace6ceb767a636503f6167756ff')
    print ret


#p2()



