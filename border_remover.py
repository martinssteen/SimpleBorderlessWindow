import os
from pathlib import Path

import math

import win32api
import win32con
import win32gui

old_style = {}

BORDER_OFFSET = 30


def get_window_handle(title):
    return win32gui.FindWindow(None, title)


def resize_window(title):
    window = get_window_handle(title)
    if window:
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        # Desired window size
        window_width = 2560 + BORDER_OFFSET
        window_height = 1440 + BORDER_OFFSET
        # Calculate the position to center the window
        x = math.ceil((screen_width - window_width) / 2)
        y = -BORDER_OFFSET

        print("Setting position x/y:" + str(x) + "/" + str(y) + " and size: " + str(window_width) + "/" + str(window_height))

        # Set the window position and size
        win32gui.SetWindowPos(window, None, x, y, window_width, window_height,
                              win32con.SWP_NOZORDER | win32con.SWP_NOOWNERZORDER | win32con.SWP_FRAMECHANGED)

        # Force window to repaint to apply changes
        win32gui.RedrawWindow(window, None, None, win32con.RDW_INVALIDATE | win32con.RDW_UPDATENOW | win32con.RDW_FRAME)


def remove_window_border(title):
    window = get_window_handle(title)

    if window:
        # Get current window style
        style = win32gui.GetWindowLong(window, win32con.GWL_STYLE)
        # Save the original style to restore it later
        old_style[window] = style

        print(str(style))

        # Remove title bar and borders but keep the thick frame for resizing
        style &= ~win32con.WS_CAPTION
        style &= ~win32con.WS_BORDER
        style &= ~win32con.WS_DLGFRAME
        # Keep WS_THICKFRAME to allow resizing with hotkeys
        style |= win32con.WS_THICKFRAME


        # Set new window style
        win32gui.SetWindowLong(window, win32con.GWL_STYLE, style)

        # Remove extended window styles that could cause the border
        ex_style = win32gui.GetWindowLong(window, win32con.GWL_EXSTYLE)
        ex_style &= ~win32con.WS_EX_WINDOWEDGE
        ex_style &= ~win32con.WS_EX_DLGMODALFRAME
        ex_style &= ~win32con.WS_EX_CLIENTEDGE
        ex_style &= ~win32con.WS_EX_STATICEDGE

        # Set new extended window style
        win32gui.SetWindowLong(window, win32con.GWL_EXSTYLE, ex_style)

        # Update window position and style
        win32gui.SetWindowPos(window, None, 0, 0, 0, 0,
                              win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOOWNERZORDER)

        print("Window style updated successfully!")
    else:
        print("Window not found!")


def remove_window_border_v2(title):
    window = get_window_handle(title)

    if window:
        # Get current window style
        style = win32gui.GetWindowLong(window, win32con.GWL_STYLE)
        # Save the original style to restore it later
        old_style[window] = style

        style &= ~win32con.WS_CAPTION
        style &= ~win32con.WS_THICKFRAME
        style &= ~win32con.WS_MINIMIZEBOX
        style &= ~win32con.WS_MAXIMIZEBOX

        # Set new window style
        win32gui.SetWindowLong(window, win32con.GWL_STYLE, style)

        ext_style = win32gui.GetWindowLong(window, win32con.GWL_EXSTYLE)
        ext_style &= ~win32con.WS_EX_DLGMODALFRAME
        ext_style &= ~win32con.WS_EX_CLIENTEDGE
        ext_style &= ~win32con.WS_EX_STATICEDGE
        win32gui.SetWindowLong(window, win32con.GWL_EXSTYLE, ext_style)

        win32gui.SetWindowPos(window, None, 0, 0, 0, 0,
                              win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOOWNERZORDER)

        print("Window style updated successfully!")
    else:
        print("Window not found!")


def remove_window_border_v3(title):
    window = get_window_handle(title)

    if window:
        win32gui.SetWindowLong(window, win32con.GWL_STYLE, win32con.WS_POPUP)


def restore_window_border(title):
    window = get_window_handle(title)

    if window and old_style[window]:
        # Restore original window style
        win32gui.SetWindowLong(window, win32con.GWL_STYLE, old_style[window])

        # Update window position and style
        win32gui.SetWindowPos(window, None, 0, 0, 0, 0,
                              win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOOWNERZORDER)

        print("Window style restored successfully!")
    else:
        print("Window not found!")


def get_all_window_names():
    def callback(hwnd, strings):
        if win32gui.IsWindowVisible(hwnd):
            strings.append(win32gui.GetWindowText(hwnd))

    windows = []
    win32gui.EnumWindows(callback, windows)

    # read from IGNORED_WINDOWS.txt and verify no windows sent back is in the file
    with open(get_ignored_windows_file_path(), 'r') as f:
        ignored_windows = f.read().splitlines()
        filteredList = list(filter(lambda x: x != '' and x not in ignored_windows, set(windows)))
        filteredList.sort()
        return filteredList


def get_ignored_windows_file_path():
    localappdata = os.getenv('LOCALAPPDATA')
    path = Path(localappdata + "\\SimpleBorderlessWindow")
    path.mkdir(exist_ok=True)
    path.joinpath('IGNORED_WINDOWS.txt').touch(exist_ok=True)
    return path.joinpath('IGNORED_WINDOWS.txt')
