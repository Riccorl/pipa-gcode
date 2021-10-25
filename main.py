import decimal
from pathlib import Path
from typing import Union
from decimal import *
import PySimpleGUI as sg
import os.path


def main(
    file_path: str,
    x_delta: Union[int, float] = 0.0,
    y_delta: Union[int, float] = 0.0,
    precision: int = 4,
) -> None:
    getcontext().prec = precision
    x_delta = Decimal(x_delta)
    y_delta = Decimal(y_delta)
    file_path = Path(file_path)
    output_file_path = file_path.parent / (file_path.stem + "_translated" + file_path.suffix)
    with open(file_path, "r") as f:
        with open(output_file_path, "w") as f_out:
            for line in f:
                line = line.split()
                edited_line = []
                for coordinate in line:

                    if coordinate.lower().startswith("x"):
                        coordinate_n = Decimal(coordinate[1:])
                        coordinate_n += x_delta
                        coordinate = "{}{}".format(coordinate[0], coordinate_n)

                    elif coordinate.lower().startswith("y"):
                        coordinate_n = Decimal(coordinate[1:])
                        coordinate_n += y_delta
                        coordinate = "{}{}".format(coordinate[0], coordinate_n)

                    edited_line.append(coordinate)
                f_out.write(" ".join(edited_line) + "\n")


if __name__ == "__main__":

    import PySimpleGUI as sg

    layout = [
        [
            sg.Text("GCode File"),
            sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse(),
        ],
        [sg.Text("X"), sg.In(size=(5, 1), enable_events=True, key="-X-", default_text="0.0")],
        [sg.Text("Y"), sg.In(size=(5, 1), enable_events=True, key="-Y-", default_text="0.0")],
        [sg.Button("Compute")],
    ]

    # Create the window
    window = sg.Window("GCode", layout)

    # Create an event loop
    file_path, x_delta, y_delta = None, 0.0, 0.0
    while True:
        event, values = window.read()
        if event == "-X-":
            x_delta = values["-X-"]
        if event == "-Y-":
            y_delta = values["-Y-"]
        if event == "-FILE-":
            file_path = values["-FILE-"]
        if event == "Compute":
            if file_path:
                main(file_path, x_delta, y_delta)
                sg.popup("Done!")
                break
            else:
                sg.popup("Please provide a file")
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

    window.close()
