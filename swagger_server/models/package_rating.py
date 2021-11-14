# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PackageRating(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, bus_factor: float=None, correctness: float=None, ramp_up: float=None, responsive_maintainer: float=None, license_score: float=None, good_pinning_practice: float=None):  # noqa: E501
        """PackageRating - a model defined in Swagger

        :param bus_factor: The bus_factor of this PackageRating.  # noqa: E501
        :type bus_factor: float
        :param correctness: The correctness of this PackageRating.  # noqa: E501
        :type correctness: float
        :param ramp_up: The ramp_up of this PackageRating.  # noqa: E501
        :type ramp_up: float
        :param responsive_maintainer: The responsive_maintainer of this PackageRating.  # noqa: E501
        :type responsive_maintainer: float
        :param license_score: The license_score of this PackageRating.  # noqa: E501
        :type license_score: float
        :param good_pinning_practice: The good_pinning_practice of this PackageRating.  # noqa: E501
        :type good_pinning_practice: float
        """
        self.swagger_types = {
            'bus_factor': float,
            'correctness': float,
            'ramp_up': float,
            'responsive_maintainer': float,
            'license_score': float,
            'good_pinning_practice': float
        }

        self.attribute_map = {
            'bus_factor': 'BusFactor',
            'correctness': 'Correctness',
            'ramp_up': 'RampUp',
            'responsive_maintainer': 'ResponsiveMaintainer',
            'license_score': 'LicenseScore',
            'good_pinning_practice': 'GoodPinningPractice'
        }
        self._bus_factor = bus_factor
        self._correctness = correctness
        self._ramp_up = ramp_up
        self._responsive_maintainer = responsive_maintainer
        self._license_score = license_score
        self._good_pinning_practice = good_pinning_practice

    @classmethod
    def from_dict(cls, dikt) -> 'PackageRating':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PackageRating of this PackageRating.  # noqa: E501
        :rtype: PackageRating
        """
        return util.deserialize_model(dikt, cls)

    @property
    def bus_factor(self) -> float:
        """Gets the bus_factor of this PackageRating.


        :return: The bus_factor of this PackageRating.
        :rtype: float
        """
        return self._bus_factor

    @bus_factor.setter
    def bus_factor(self, bus_factor: float):
        """Sets the bus_factor of this PackageRating.


        :param bus_factor: The bus_factor of this PackageRating.
        :type bus_factor: float
        """
        if bus_factor is None:
            raise ValueError("Invalid value for `bus_factor`, must not be `None`")  # noqa: E501

        self._bus_factor = bus_factor

    @property
    def correctness(self) -> float:
        """Gets the correctness of this PackageRating.


        :return: The correctness of this PackageRating.
        :rtype: float
        """
        return self._correctness

    @correctness.setter
    def correctness(self, correctness: float):
        """Sets the correctness of this PackageRating.


        :param correctness: The correctness of this PackageRating.
        :type correctness: float
        """
        if correctness is None:
            raise ValueError("Invalid value for `correctness`, must not be `None`")  # noqa: E501

        self._correctness = correctness

    @property
    def ramp_up(self) -> float:
        """Gets the ramp_up of this PackageRating.


        :return: The ramp_up of this PackageRating.
        :rtype: float
        """
        return self._ramp_up

    @ramp_up.setter
    def ramp_up(self, ramp_up: float):
        """Sets the ramp_up of this PackageRating.


        :param ramp_up: The ramp_up of this PackageRating.
        :type ramp_up: float
        """
        if ramp_up is None:
            raise ValueError("Invalid value for `ramp_up`, must not be `None`")  # noqa: E501

        self._ramp_up = ramp_up

    @property
    def responsive_maintainer(self) -> float:
        """Gets the responsive_maintainer of this PackageRating.


        :return: The responsive_maintainer of this PackageRating.
        :rtype: float
        """
        return self._responsive_maintainer

    @responsive_maintainer.setter
    def responsive_maintainer(self, responsive_maintainer: float):
        """Sets the responsive_maintainer of this PackageRating.


        :param responsive_maintainer: The responsive_maintainer of this PackageRating.
        :type responsive_maintainer: float
        """
        if responsive_maintainer is None:
            raise ValueError("Invalid value for `responsive_maintainer`, must not be `None`")  # noqa: E501

        self._responsive_maintainer = responsive_maintainer

    @property
    def license_score(self) -> float:
        """Gets the license_score of this PackageRating.


        :return: The license_score of this PackageRating.
        :rtype: float
        """
        return self._license_score

    @license_score.setter
    def license_score(self, license_score: float):
        """Sets the license_score of this PackageRating.


        :param license_score: The license_score of this PackageRating.
        :type license_score: float
        """
        if license_score is None:
            raise ValueError("Invalid value for `license_score`, must not be `None`")  # noqa: E501

        self._license_score = license_score

    @property
    def good_pinning_practice(self) -> float:
        """Gets the good_pinning_practice of this PackageRating.

        The fraction of its dependencies that are pinned to at least a specific major+minor version, e.g. version 2.3.X of a package. (If there are zero dependencies, they should receive a 1.0 rating. If there are two dependencies, one pinned to this degree, then they should receive a ½ = 0.5 rating).  # noqa: E501

        :return: The good_pinning_practice of this PackageRating.
        :rtype: float
        """
        return self._good_pinning_practice

    @good_pinning_practice.setter
    def good_pinning_practice(self, good_pinning_practice: float):
        """Sets the good_pinning_practice of this PackageRating.

        The fraction of its dependencies that are pinned to at least a specific major+minor version, e.g. version 2.3.X of a package. (If there are zero dependencies, they should receive a 1.0 rating. If there are two dependencies, one pinned to this degree, then they should receive a ½ = 0.5 rating).  # noqa: E501

        :param good_pinning_practice: The good_pinning_practice of this PackageRating.
        :type good_pinning_practice: float
        """
        if good_pinning_practice is None:
            raise ValueError("Invalid value for `good_pinning_practice`, must not be `None`")  # noqa: E501

        self._good_pinning_practice = good_pinning_practice
