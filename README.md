# python-hw-railroad

Railroad specific hardware objects

## Turnout

The Turnout class models the motion of a single powered frog model railroad turnout. The class emits a single event (state_changed) that contains the current device state (main, transition_(main/diverging), diverging). The class follows the state diagram presented below,

![Turnout State Diagram](<./src/hw_railroad/turnout-state-diagram.png>)
