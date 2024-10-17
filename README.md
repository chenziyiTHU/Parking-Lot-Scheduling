# Parking-Lot-Scheduling
This repository contains the midterm project for the "Principles of Artificial Intelligence" course offered by the Department of Automation at Tsinghua University. This project focuses on the implementation of a parking lot scheduling problem, covering two main components: UI design and automatic solving.

## Running the Program and UI Usage

There are 3 code files in this directory. 
- `custom.py` contains the `CustomParkingLot` class, which defines the window of customizing parking lot
- `game.py` contains the `ParkingGame` class, which defines the window of parking lot scheduling game
- `main.py` contains the `ParkingLot` class, which defines the initialization of parking lot scheduling problem, and contains the A\* searching solution algorithm `ParkingLot.a_star()`

To run the program, execute `custom.py`, which depends on the `tkinter` library. You can install it with:

```bash
pip install tkinter
```

The execution of the program have following options:

1. Customize the parking lot scheduling problem through UI, play the game and see the answer

```bash
python custom.py
```

2. Run an example of parking lot scheduling problem and play through UI

```bash
python game.py
```

3. Customize the parking lot scheduling problem through terminal and see the answer

```bash
python main.py
```
