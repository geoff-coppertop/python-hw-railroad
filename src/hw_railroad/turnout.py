#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# turnout.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging

from axel import Event
from transitions.extensions import LockedMachine as Machine

class Turnout(Machine):
    '''
    '''
    ROUTE_CHANGE_SPEED = 20.0       # degrees/second

    def __init__(self, servo, gpo_provider, main_angle, diverging_angle):
        '''
        Create a turnout

        This is only able to create electro frog turnouts
        '''
        self.__logger = logging.getLogger('turnout')

        self.__end_angles = {
            'transition_main':      main_angle,
            'transition_diverging': diverging_angle
            }
        self.__gpo = gpo_provider
        self.__servo = servo
        self.__motion_time = 0

        self.__min_angle = min(main_angle, diverging_angle)
        self.__max_angle = max(main_angle, diverging_angle)

        self.__init_state_machine()

        self.state_changed = Event()

    def operate(self, time):
        '''
        Move the turnout to the requested position

        Time is provided so that the turnout can be moved at a constant speed

        The servo used by the turnout is turned off after the movement
        '''
        if self.__is_idle():
            self.__logger.debug('No motion in progress')

            return
        else:
            current_angle = self.__servo.get_angle()
            end_angle = self.__end_angles[self.state]

            self.__logger.debug(f'Servo currently at: {current_angle} , moving to: {end_angle}')

            if current_angle == end_angle:
                # This will turn the servo off
                self.__servo.set_angle(end_angle)

                # Kick the state machine to indicate that we have
                # TODO: There probably needs to be a way to configure the
                #       control of the frog
                if self.state == 'transition_main':
                    self.__gpo.disable()

                    self._motion_complete_main()
                else:
                    self.__gpo.enable()

                    self._motion_complete_diverging()

            else:
                # Calculate the required motion
                speed = Turnout.ROUTE_CHANGE_SPEED

                if current_angle > end_angle:
                    speed = -Turnout.ROUTE_CHANGE_SPEED

                time_delta = time - self.__motion_time

                new_angle = speed * time_delta
                new_angle += current_angle

                if new_angle < self.__min_angle:
                    new_angle = self.__min_angle

                if new_angle > self.__max_angle:
                    new_angle = self.__max_angle

                self.__logger.debug(f'Servo moved to: {new_angle}')

                self.__servo.set_angle(new_angle)

                self.__motion_time += time_delta

    def change_route(self, time):
        '''
        Toggles the current state of the turnout if it isn't already in motion
        '''
        if not self.__is_idle:
            return
        else:
            # Set the first motion time
            self.__motion_time = time

            # Kick the state machine so that we start moving
            if self.state == 'main':
                self._set_diverging()
            else:
                self._set_main()

    def _update_state(self):
        '''
        Emit the current state of the turnout
        '''
        self.state_changed(self.state)

    def __init_state_machine(self):
        '''
        Build the state machine
        '''
        states = [
            { 'name': 'transition_main' },
            { 'name': 'transition_diverging' },
            { 'name': 'diverging' },
            { 'name': 'main' },
        ]

        transitions = [
            { 'trigger': '_set_main',
                'source': 'diverging',
                'dest': 'transition_main' },
            { 'trigger': '_set_diverging',
                'source': 'main',
                'dest': 'transition_diverging' },
            { 'trigger': '_motion_complete_main',
                'source': 'transition_main',
                'dest' : 'main' },
            { 'trigger': '_motion_complete_diverging',
                'source': 'transition_diverging',
                'dest' : 'diverging' },
        ]

        Machine.__init__(
            self,
            states=states,
            transitions=transitions,
            initial='transition_main',
            auto_transitions=False,
            after_state_change='_update_state',
            ignore_invalid_triggers=True)

    def __is_idle(self):
        '''
        Check whether the Turnout is moving
        '''
        if 'transition' in self.state:
            return False
        else:
            return True
