# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 02:12:38 2021

@author: garvi
"""


'''

This file is a bridge between the auto-generated server stubs and the existing front-end 
.. impl.

'''

# Files
from Project2 import app
from swagger_server.models.authentication_request import AuthenticationRequest  # noqa: E501
from swagger_server.models.authentication_token import AuthenticationToken  # noqa: E501
from swagger_server.models.enumerate_offset import EnumerateOffset  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.package import Package  # noqa: E501
from swagger_server.models.package_history_entry import PackageHistoryEntry  # noqa: E501
from swagger_server.models.package_id import PackageID  # noqa: E501
from swagger_server.models.package_metadata import PackageMetadata  # noqa: E501
from swagger_server.models.package_name import PackageName  # noqa: E501
from swagger_server.models.package_query import PackageQuery  # noqa: E501
from swagger_server.models.package_rating import PackageRating  # noqa: E501
from swagger_server import util

from swagger_server.controllers import controller_helper

# Libraries
import connexion

@app.route("/authenticate", methods=['PUT'])
def create_auth_token():
    if connexion.request.is_json:
        body = AuthenticationRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'This system does not support authentication.', 501


@app.route("/package", methods=['POST'])
def package_create(body=None, x_authorization=None):  # noqa: 

    if connexion.request.is_json:
         body = Package.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
         x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501

    response = controller_helper.convert_and_upload_zip(body.data.content, 
                                                                body.metadata.name,
                                                                body.metadata.version,
                                                                body.metadata.id)
    
    print (response)
    print (response[1])
    return response[1]



@app.route("/package/<id>", methods=["GET"])
def package_retrieve(id=None, x_authorization=None):  # noqa: E501
    """package_retrieve

    Return this package. # noqa: E501

    :param id: ID of package to fetch
    :type id: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: Package
    """
    if connexion.request.is_json:
        id = PackageID.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    
    
    ret = controller_helper.get_package_by_id(id)
    return ret


@app.route("/package/<id>", methods=["PUT"])
def package_update(id, body=None, x_authorization=None):  # noqa: E501
    """Update this version of the package.

    The name, version, and ID must match.  The package contents (from PackageData) will replace the previous contents. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Package.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        id = PackageID.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    
    
    
    ret = controller_helper.update_package_by_id(body.data.content,
                                              id,
                                              body.metadata.name,
                                              body.metadata.version)
    return ret 



@app.route("/package/<id>", methods=["DELETE"])
def package_delete(id, x_authorization=None):  # noqa: E501
    """Delete this version of the package.

     # noqa: E501

    :param id: Package ID
    :type id: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        id = PackageID.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    
    
    ret = controller_helper.delete_package_by_id(id)
    return ret

@app.route("/package/<id>/rate", methods=["GET"])
def package_rate(id=None, x_authorization=None):  # noqa: E501
    """package_rate

     # noqa: E501

    :param id: 
    :type id: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: PackageRating
    """
    if connexion.request.is_json:
        id = PackageID.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501

    ret = controller_helper.get_rating_by_id(id)

    return ret


@app.route("/package/byName/<name>", methods=["GET"])
def package_by_name_get(name, x_authorization=None):  # noqa: E501
    """package_by_name_get

    Return the history of this package (all versions). # noqa: E501

    :param name: 
    :type name: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: List[PackageHistoryEntry]
    """
    if connexion.request.is_json:
        name = PackageName.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    
    ret = controller_helper.get_packages_by_name(name)
    return ret


@app.route("/package/byName/<name>", methods=["DELETE"])
def package_by_name_delete(name, x_authorization=None):  # noqa: E501
    """Delete all versions of this package.

     # noqa: E501

    :param name: 
    :type name: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        name = PackageName.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    
    
    ret = controller_helper.delete_package_by_name(name)
    return ret


@app.route("/packages", methods=["POST"])
def packages_list():
    offset = 1
    if connexion.request.is_json:
        body = [PackageQuery.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    if connexion.request.is_json:
        offset = EnumerateOffset.from_dict(connexion.request.get_json())  # noqa: E501
    ret = controller_helper.paginate(int(offset))
    
    print ("HERE IS IT IN THE FNAL RETURN")
    return ret



@app.route("/reset", methods=['DELETE'])
def registry_reset(x_authorization=None):  # noqa: E501
    """registry_reset

     # noqa: E501

    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    
    controller_helper.tear_down()
    return 'Registry is reset.', 200
