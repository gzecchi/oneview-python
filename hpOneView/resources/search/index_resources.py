# -*- coding: utf-8 -*-
###
# (C) Copyright [2019] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

from hpOneView.resources.resource import ResourceClient
from urllib.parse import quote


class IndexResources(object):
    """
    Index Resources API client.

    """

    URI = '/rest/index/resources'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, category='', count=-1, fields='', filter='', padding=0, query='', reference_uri='',
                sort='', start=0, user_query='', view=''):
        """
        Gets a list of index resources based on optional sorting and filtering and is constrained by start
        and count parameters.

        Args:
            category (str or list):
                 Category of resources. Multiple Category parameters are applied with OR condition.
            count (int):
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            fields (str):
                Specifies which fields should be returned in the result set.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            padding (int):
                Number of resources to be returned before the reference URI resource.
            query (str):
                 A general query string to narrow the list of resources returned.
                 The default is no query - all resources are returned.
            reference_uri (str):
                Load one page of resources, pagination is applied with reference to referenceUri provided.
            sort (str):
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.
            start (int):
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            user_query (str):
                Free text Query string to search the resources. This will match the string in any field that is indexed.
            view (str):
                Return a specific subset of the attributes of the resource or collection, by specifying the name of a predefined view.

        Returns:
            list: A list of index resources.
        """
        uri = self.URI + '?'

        uri += self.__list_or_str_to_query(category, 'category')
        uri += self.__list_or_str_to_query(fields, 'fields')
        uri += self.__list_or_str_to_query(filter, 'filter')
        uri += self.__list_or_str_to_query(padding, 'padding')
        uri += self.__list_or_str_to_query(query, 'query')
        uri += self.__list_or_str_to_query(reference_uri, 'referenceUri')
        uri += self.__list_or_str_to_query(sort, 'sort')
        uri += self.__list_or_str_to_query(user_query, 'userQuery')
        uri += self.__list_or_str_to_query(view, 'view')

        uri = uri.replace('?&', '?')

        return self._client.get_all(start=start, count=count, uri=uri)

    def get(self, uri):
        """
        Gets an index resource by URI.

        Args:
            uri: The resource URI.

        Returns:
            dict: The index resource.
        """
        uri = self.URI + uri
        return self._client.get(uri)

    def get_aggregated(self, attribute, category, child_limit=6, filter='', query='', user_query=''):
        """
        Gets a list of index resources based on optional sorting and filtering and is constrained by start
        and count parameters.

        Args:
            attribute (list or str):
                Attribute to pass in as query filter.
            category (str):
                Category of resources. Multiple Category parameters are applied with an OR condition.
            child_limit (int):
                Number of resources to be retrieved. Default=6.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            query (str):
                A general query string to narrow the list of resources returned.
                The default is no query - all resources are returned.
            user_query (str):
                Free text Query string to search the resources.
                This will match the string in any field that is indexed.

        Returns:
            list: An aggregated list of index resources.
        """
        uri = self.URI + '/aggregated?'

        # Add attribute to query
        uri += self.__list_or_str_to_query(attribute, 'attribute')
        uri += self.__list_or_str_to_query(category, 'category')
        uri += self.__list_or_str_to_query(child_limit, 'childLimit')
        uri += self.__list_or_str_to_query(filter, 'filter')
        uri += self.__list_or_str_to_query(query, 'query')
        uri += self.__list_or_str_to_query(user_query, 'userQuery')

        uri = uri.replace('?&', '?')

        return self._client.get(uri)

    def __list_or_str_to_query(self, list_or_str, field_name):
        formated_query = ''
        if list_or_str:
            if isinstance(list_or_str, list):
                for f in list_or_str:
                    formated_query = formated_query + "&{0}=".format(field_name) + ''.join(quote(str(f)))
            else:
                formated_query = "&{0}=".format(field_name) + str(list_or_str)
        return formated_query
