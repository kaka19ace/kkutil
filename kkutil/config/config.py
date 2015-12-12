#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @date     Dec 13 2015
# @brief     
#

import os
import threading


class Config(object):
    TYPE_YAML = 1
    TYPE_ETCD = 2

    _threading_lock = threading.Lock()

    def __init__(self, config_type=TYPE_YAML):
        if config_type == self.TYPE_YAML:
            from .yaml import YamlHelper
            self.helper = YamlHelper()
        elif config_type == self.TYPE_ETCD:
            from .etcd import EtcdHelper
            self.helper = EtcdHelper()
        else:
            raise ValueError("not support type: {0}".format(config_type))

        self.type = config_type

    def set_yaml_config_path(self, path):
        """
        for yaml
        set config dir path to cover the default config path
        :param path:
        """
        if self.type != self.TYPE_YAML:
            raise TypeError(
                "method not support current config_type: {0} for path: {1}".format(self.type, path)
            )
        if not isinstance(path, str):
            raise TypeError("path {0} is not str".format(path))
        if not os.path.isdir(path):
            raise OSError("dir path is not exists: {0}".format(path))

        with self._threading_lock:
            self.helper.config_path = path

