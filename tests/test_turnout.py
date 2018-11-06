#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# test_turnout.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------
import logging
import pytest

from hw_railroad import Turnout

from .fake_servo import FakeServo
from .fake_gpo_provider import FakeGPOProvider

#-------------------------------------------------------------------------------
# Test constants
#-------------------------------------------------------------------------------
ANGLE_MAIN = 45
ANGLE_DIV = 135

#-------------------------------------------------------------------------------
# Test fixtures
#-------------------------------------------------------------------------------
@pytest.fixture
def servo():
    """Servo test double"""
    return FakeServo()

@pytest.fixture
def gpo_provider():
    """GPO provider test double"""
    return FakeGPOProvider()

@pytest.fixture
def turnout_main(servo, gpo_provider):
    """Create a turnout set to the main route"""
    gpo_provider.disable()

    turnout = Turnout(servo, gpo_provider, ANGLE_MAIN, ANGLE_DIV)

    time = 0

    while(turnout.state != 'main'):
        time += 0.1
        turnout.operate(time)

    # Check that the route was set to the diverging route
    assert(servo.get_angle() == ANGLE_MAIN)
    assert(not gpo_provider.is_enabled())

    return turnout

#-------------------------------------------------------------------------------
# Route tests
#-------------------------------------------------------------------------------
def test_main_to_diverging_route(turnout_main, servo, gpo_provider):
    time = 0

    turnout_main.change_route(time) # sneaky way to set time to 0 for distance
                                    # calculation

    while(turnout_main.state != 'diverging'):
        time += 0.1
        turnout_main.operate(time)

    # Check that the route was set to the diverging route
    assert(servo.get_angle() == ANGLE_DIV)
    assert(gpo_provider.is_enabled())