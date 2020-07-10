# niveles_prima

This script get the Cablevisión-Fibertel prima levels and show them in a table.

    ╒═════════════╤═════════════════════════════════════╤═════════╕
    │ TAG         │ Value                               │  State  │
    ╞═════════════╪═════════════════════════════════════╪═════════╡
    │ Tx          │ 45,5 dBmV                           │ CORRECT │
    ├─────────────┼─────────────────────────────────────┼─────────┤
    │ Freq Tx     │ 36600 MHz                           │         │
    ├─────────────┼─────────────────────────────────────┼─────────┤
    │ Rx          │ -2,5 dBmV                           │ CORRECT │
    ├─────────────┼─────────────────────────────────────┼─────────┤
    │ Freq Rx     │ 879000 MHz                          │         │
    ├─────────────┼─────────────────────────────────────┼─────────┤
    │ Mer         │ 35,4 dB                             │         │
    ├─────────────┼─────────────────────────────────────┼─────────┤
    │ Equipo      │ FAST3686                            │         │
    ├─────────────┼─────────────────────────────────────┼─────────┤
    │ Descripción │ F@ST3686 Wireless Voice Gateway <>  │         │
    ├─────────────┼─────────────────────────────────────┼─────────┤
    │ Versión Os  │ "FAST3686_CVA-SIP_3.601.0-20190521" │         │
    ╘═════════════╧═════════════════════════════════════╧═════════╛

## Level State

The important levels are `TX` and `RX`, so the script just evaluate them.

Each level has its own range of acceptance:

    TX: CORRECT between 35 dBmV and 47 dBmV
        INCORRECT outside the previous range
    
    RX: CORRECT between -7 dBmV and 7 dBmV
        WARNING between -15 dBmV and 15 dBmV
        INCORRECT outside the previous ranges

## Log

The script keep a log file with the retrieved values for `RX` and `TX`:

    2020-07-09 19:00:24 | SUCCESS | tx: 46,2 dBmV
    2020-07-09 19:00:24 | SUCCESS | rx: -2,3 dBmV
    2020-07-10 10:34:26 | SUCCESS | tx: 45,5 dBmV
    2020-07-10 10:34:26 | SUCCESS | rx: -2,5 dBmV

# Requirements

**IMPORTANT**: This script requires Python >= 3.8

## Install requirements

    $ pip install -r requirements.txt

# Execution

    $ python niveles_prima.py
    
## Monitoring

A way to monitoring a connection could be using the `watch` command.

For example, to check the levels (and store them in the log file) every minute:

    $ watch -cn 60 python niveles_prima.py
