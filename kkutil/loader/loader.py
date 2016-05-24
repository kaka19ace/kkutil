#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import threading
import logging


class Loader(object):
    _config = NotImplemented
    _config_cache_map = {}
    _lock = threading.RLock()

    @classmethod
    def set_config(cls, config):
        """
        :param config: kkutils.config.Config instance
        """
        with cls._lock:
            cls._config = config

    @classmethod
    def set_logger(cls, logger):
        with cls._lock:
            cls.logger = logger

    @classmethod
    def _load_by_key(cls, key):
        if cls._config_cache_map.get(key, None) is None:
            with cls._lock:
                if cls._config_cache_map.get(key, None) is None:
                    cls._config_cache_map[key] = cls._config.get_config_data(key)
        return cls._config_cache_map[key]

    @classmethod
    def load_config(cls, key, field=None):
        """
        just support two level config

        :param key: first level
        :param field: if not None: just want second level config
        :return: dict about config
        """
        if field is None:
            return cls._load_by_key()

        entry_config = cls._load_by_key(key)
        sub_config = entry_config.get(field)
        if not sub_config:
            raise AttributeError("could not get sub config: key={0} field={1}".format(key, field))

        return sub_config


Loader.set_logger(logger=logging.getLogger(Loader.__name__))

