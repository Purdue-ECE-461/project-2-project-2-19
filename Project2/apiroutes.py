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
    
    return "IDk"


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
    return 'Wiped SQL and Blobs.!'
