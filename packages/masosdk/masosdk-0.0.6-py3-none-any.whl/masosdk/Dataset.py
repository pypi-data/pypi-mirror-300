import os
import numpy as np
import requests

from .config import Config


class Dataset:
    def __init__(self, api_token, **kwargs):
        self.api_token = api_token
        self.name = None
        self.shape = None
        self.id = None

        if kwargs.get('name') and kwargs.get('shape'):
            self.create_new(kwargs.get('name'), kwargs.get('shape'))
        elif kwargs.get('id'):
            self.create_from_id(kwargs.get('id'))

    def create_new(self, name, shape):
        self.name = name

        self.shape = shape

        response = requests.post(
            f'{Config.base_url}/dataset/',
            headers={"Authorization": f"{self.api_token}"},
            json={
                'name': self.name,
                'shape': self.shape
            },
            verify=False
        )

        response.raise_for_status()

        if response.status_code == 200:
            self.id = response.json()

    def create_from_id(self, id):
        self.id = id

        requests.get(
            f'{Config.base_url}/dataset/{self.id}/open',
            headers={"Authorization": f"{self.api_token}"},
            verify=False,
        )

        response = requests.get(
            f'{Config.base_url}/dataset/{self.id}',
            headers={"Authorization": f"{self.api_token}"},
            verify=False,
        )

        response.raise_for_status()

        data = response.json()

        self.name = data['path']

        self.shape = data['shape']

    def upload_array(self, data, slc):
        position = [i if value != -1 else 0 for value, i in enumerate(slc)]
        displayed_dimensions = [i for i, value in enumerate(slc) if value == -1]

        response = requests.put(
            f'{Config.base_url}/array/{self.id}/',
            headers={"Authorization": f"{self.api_token}"},
            json={
                'data': list(data.flatten('F')),
                'position': position,
                'displayed_dimensions': displayed_dimensions,
            },
            verify=False
        )

        response.raise_for_status()

    def get_array(self, slc):
        response = requests.get(
            f'{Config.base_url}/array/{self.id}/',
            headers={"Authorization": f"{self.api_token}"},
            params={
                'position': tuple(slc)
            },
            verify=False
        )

        response.raise_for_status()

        data = np.array(response.json()['data'])

        shape = tuple([self.shape[i] for i, x in enumerate(slc) if x == -1])

        data = np.reshape(data, shape)

        return data

    def get_parameter(self, key):
        response = requests.get(
            f'{Config.base_url}/parameter/{self.id}/',
            headers={"Authorization": f"{self.api_token}"},
            params={
                'key': key
            },
            verify=False
        )

        response.raise_for_status()

        return response.json()

    def set_parameter(self, key, value):
        requests.post(
            f'{Config.base_url}/parameter/',
            headers={"Authorization": f"{self.api_token}"},
            json={
                'dataset_id': self.id,
                'key': key,
                'value': value,
                'type': self.get_parameter_type(value)
            },
            verify=False
        )

    @staticmethod
    def get_parameter_type(value):
        if isinstance(value, bool):
            return 'boolean'
        if isinstance(value, int):
            return 'int'
        if isinstance(value, float):
            return 'float'
        if isinstance(value, str):
            return 'str'
        if isinstance(value, (list, tuple)):
            if all(isinstance(value, bool) for value in value):
                return 'bool'
            if all(isinstance(element, int) for element in value):
                return 'int[]'
            if all(isinstance(element, float) for element in value):
                return 'float[]'
            if all(isinstance(element, str) for element in value):
                return 'str[]'

    def delete(self):
        requests.delete(
            f'{Config.base_url}/dataset/{self.id}',
            headers={"Authorization": f"{self.api_token}"},
            verify=False
        )
