#!/home/debauer/utils/.venv/bin/python3
from __future__ import annotations

import sys

from argparse import ArgumentParser
from dataclasses import dataclass

import pulsectl

from pulsectl import PulseClientInfo
from pulsectl import PulseOperationFailed
from pulsectl import PulseSinkInfo
from pulsectl import PulseSinkInputInfo


pulse = pulsectl.Pulse("my-client-name")


@dataclass
class SinkDefinition:
    name: str
    description: str


class Sinks:
    sinks = [
        SinkDefinition("internal", "Family 17h/19h HD Audio Controller"),
        SinkDefinition("boxen", "Sound Blaster Play!"),
        SinkDefinition("bayer", "USB HIFI Audio"),
        SinkDefinition("bose", "Bose David"),
    ]

    def get_sink_names(self):
        return [s.name for s in self.sinks]

    def get_sink_by_name(self, name: str) -> SinkDefinition:
        for s in self.sinks:
            if s.name == name:
                return s
        raise ValueError(f"sink not found {name=}")

    def get_sink_by_description(self, description: str) -> SinkDefinition:
        for s in self.sinks:
            if s.description == description:
                return s
        return SinkDefinition("NOT DEFINED", "NOT DEFINED")
        # raise ValueError(f"sink not found {description=}")


my_sinks = Sinks()


def find_sink(name: str, verbose: bool = False) -> PulseSinkInfo:
    sinks: list[PulseSinkInfo] = pulse.sink_list()
    for s in sinks:
        if s.proplist["device.description"] == my_sinks.get_sink_by_name(name).description:
            if verbose:
                print("found sink:")
                print(" ", s)
            return s


def default_sink(verbose: bool = False) -> None:
    sinks: list[PulseSinkInfo] = pulse.sink_list()
    for s in sinks:
        if verbose:
            if s.proplist["node.name"] == pulse.server_info().default_sink_name:
                print("default sink:")
                print(" ", my_sinks.get_sink_by_description(s.proplist["device.description"]))


def active_sink(verbose: bool = False) -> PulseSinkInfo:
    sinks: list[PulseSinkInfo] = pulse.sink_list()
    for s in sinks:
        if s.state._value == "running":
            if verbose:
                print("active sink:")
                print(" ", my_sinks.get_sink_by_description(s.proplist["device.description"]))
            return s


def available_sinks(verbose: bool = False) -> list[PulseSinkInfo]:
    sinks: list[PulseSinkInfo] = pulse.sink_list()
    if verbose:
        print("available sinks:")
        print()
        print("nr long name                                     || name          || state        || device.id")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        for i, s in enumerate(sinks):
            print(
                f'{i:<2} {s.proplist["device.description"]:<45} || {my_sinks.get_sink_by_description(s.proplist["device.description"]).name:<13} || {s.state._value:<12} || device.id: {s.proplist["device.id"]}',
            )
    return sinks


def available_input_sinks(verbose: bool = False) -> list[PulseSinkInputInfo]:
    sinks: list[PulseSinkInputInfo] = pulse.sink_input_list()
    if verbose:
        print("available input sinks:")
        for s in sinks:
            print(" ", s.proplist["application.name"])
    return sinks


def available_clients(verbose: bool = False) -> list[PulseClientInfo]:
    playbacks: list[PulseClientInfo] = pulse.client_list()
    if verbose:
        print("available clients:")
        for p in playbacks:
            print(f' {p.proplist["application.name"]} (id:{p.index})')
    return playbacks


def menue_item():
    return my_sinks


def parse():
    parser = ArgumentParser(description="System to record the data on a trimodal crane")
    parser.add_argument("-d", "--device", type=str, help="device", choices=my_sinks.get_sink_names())
    parser.add_argument("-v", "--verbose", action="store_const", const="verbose", help="verbose")
    parser.add_argument("-a", "--active", action="store_const", const="active", help="get active sink")
    return parser.parse_args()


def switch(device: str, verbose: bool):
    if verbose:
        print(pulse.sink_input_list())
    sink = find_sink(device)
    input_sinks = available_input_sinks()
    pulse.sink_default_set(sink)
    for input_sink in input_sinks:
        try:
            pulse.sink_input_move(input_sink.index, sink.index)
        except PulseOperationFailed:
            print(f"failed {input_sink.proplist['application.name']}")
        except AttributeError:
            available_sinks(verbose=True)
            print("NO SINK FOUND")
            return
    print("DONE")


def main():
    if len(sys.argv) != 1:  # bit hacky because of positional argument in argparse
        args = parse()
        verbose = args.verbose
        device = args.device
        active = args.active
        if active:
            sink = active_sink(verbose)
            name = my_sinks.get_sink_by_description(sink.proplist["device.description"]).name
            print(name, "")
            exit()
    else:
        verbose = False
        sinks = available_sinks(verbose=True)
        sink_id = int(input("choose sink: "))
        device = my_sinks.get_sink_by_description(sinks[sink_id].proplist["device.description"]).name

    active_sink(verbose)
    available_sinks(verbose)
    available_clients(verbose)
    default_sink(verbose)

    if device is not None:
        switch(device, verbose)
    else:
        available_sinks(verbose=True)
    exit()


if __name__ == "__main__":
    main()
