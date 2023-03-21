"""The entry point for the program."""

import PySimpleGUI as sg

import sys
import os
from time import sleep
from threading import Thread

import installer

# The title for the GUI window.
TITLE = 'Minecraft Mod Installer'

# The keys for the GUI window elements.
MSG_KEY = '-MSG-'
BUTTON_KEY = '-BUTTON-'
OUTCOME_KEY = '-OUTCOME-'

# The icon file to use for the window.
ICON_FILE_NAME = 'minecraft.ico'

# The layout of the GUI window.
LAYOUT = [
    [sg.Text('Installing...', key=MSG_KEY)],
    [sg.Button('OK', key=BUTTON_KEY, visible=False)]
]

# The GUI window.
WINDOW = sg.Window(
    TITLE,
    LAYOUT,
    element_justification='c',
    icon=os.path.join(
        getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),
        ICON_FILE_NAME
    ),
    finalize=True
)


def install_and_update():
    """Run the installer and update the GUI window with the outcome."""

    # Run the installer.
    outcome = installer.run()

    # Make the window invisible.
    WINDOW.disappear()

    # Sleep for 100ms to give the window time to disappear.
    sleep(0.1)

    # Update the text element with the outcome.
    WINDOW[MSG_KEY].update(value=outcome)

    # Make the 'Ok' button visible.
    WINDOW[BUTTON_KEY].update(visible=True)

    # Refresh the window.
    WINDOW.refresh()

    # Make the window visible again.
    WINDOW.reappear()

    # Move the window back to the center of the screen, since the
    # new text in the text element might expand it on the right side.
    WINDOW.move_to_center()


def main() -> None:
    # Run the installer and GUI window updater in another thread.
    Thread(target=install_and_update).start()

    # Create an event loop for the GUI window.
    while True:
        event, values = WINDOW.read()

        # Stop the event loop if the user
        # presses 'Ok' or closes the window.
        if event == BUTTON_KEY or event == sg.WIN_CLOSED:
            break

    WINDOW.close()


if __name__ == '__main__':
    main()
