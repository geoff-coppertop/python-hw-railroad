#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# fake_gpo_provider.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------
class FakeGPOProvider(object):
    """GPO provider test double"""

    def __init__(self):
        """Create a GPO provider test double"""
        self.__is_enabled = False

    def enable(self):
        """Enable output"""
        self.__is_enabled = True

    def disable(self):
        """Disable output"""
        self.__is_enabled = False

    def is_enabled(self):
        """Return output status"""
        return self.__is_enabled

