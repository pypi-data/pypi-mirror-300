# -*- coding: utf-8 -*-
"""
Utilities to manipulate the workflow input protocols.
Most functionality comes from the AiiDA-QE plugin.
"""
import pathlib
from typing import Optional, Union
import yaml
from aiida import orm


class ProtocolMixin:
    """
    Utility class for processes to build input mappings for a given protocol 
    based on a YAML configuration file.
    """

    @classmethod
    def get_protocol_filepath(cls) -> pathlib.Path:
        """Return the ``pathlib.Path`` to the ``.yaml`` file that defines the protocols."""
        raise NotImplementedError

    @classmethod
    def get_default_protocol(cls) -> str:
        """Return the default protocol for a given workflow class.

        :param cls: the workflow class.
        :return: the default protocol.
        """
        return cls._load_protocol_file()['default_protocol']

    @classmethod
    def get_available_protocols(cls) -> dict:
        """Return the available protocols for a given workflow class.

        :param cls: the workflow class.
        :return: dictionary of available protocols, where each key is a protocol and value is another dictionary that
            contains at least the key `description` and optionally other keys with supplementary information.
        """
        data = cls._load_protocol_file()
        return {protocol: {'description': values['description']} for protocol, values in data['protocols'].items()}

    @classmethod
    def get_protocol_inputs(
        cls,
        protocol: Optional[dict] = None,
        overrides: Union[dict, pathlib.Path, None] = None,
    ) -> dict:
        """Return the inputs for the given workflow class and protocol.

        :param cls: the workflow class.
        :param protocol: optional specific protocol, if not specified, the default will be used
        :param overrides: dictionary of inputs that should override those specified by the protocol. The mapping should
            maintain the exact same nesting structure as the input port namespace of the corresponding workflow class.
        :return: mapping of inputs to be used for the workflow class.
        """
        data = cls._load_protocol_file()
        protocol = protocol or data['default_protocol']

        try:
            protocol_inputs = data['protocols'][protocol]
        except KeyError as exception:
            raise ValueError(
                f'`{protocol}` is not a valid protocol. Call ``get_available_protocols`` to show available protocols.'
            ) from exception
        inputs = recursive_merge(data['default_inputs'], protocol_inputs)
        inputs.pop('description')

        if isinstance(overrides, pathlib.Path):
            with overrides.open() as file:
                overrides = yaml.safe_load(file)

        if overrides:
            inputs = recursive_merge(inputs, overrides)

        return inputs

    @classmethod
    def _load_protocol_file(cls) -> dict:
        """Return the contents of the protocol file for workflow class."""
        with cls.get_protocol_filepath().open() as file:
            return yaml.safe_load(file)
        

def suggested_energy_cutoff(
    structure,
    inputs,
    protocol = 'moderate'
) -> float:
    """
    Return a suggested energy cutoff based on the provided protocol
    and pseudo_set designated.
    """
    from importlib_resources import files
    from . import pseudos # type: ignore
    pseudos_path = files(pseudos) / 'pseudos.yaml'
    pseudo_set = inputs['pseudo_set']

    if protocol is None:
        protocol = 'moderate'

    with open(pseudos_path, 'r') as infile:
        pseudo_info = yaml.safe_load(infile)

    values = pseudo_info.get(pseudo_set, None)

    atoms = structure.get_ase()

    symbols = set(atoms.get_chemical_symbols())

    cutoff = 0
    for atom in symbols:
        c = values[atom][protocol]
        if c > cutoff:
            cutoff = c

    return int(cutoff)


def recursive_merge(left: dict, right: dict) -> dict:
    """Recursively merge two dictionaries into a single dictionary.

    If any key is present in both ``left`` and ``right`` dictionaries, the value from the ``right`` dictionary is
    assigned to the key.

    :param left: first dictionary
    :param right: second dictionary
    :return: the recursively merged dictionary
    """
    import collections

    # Note that a deepcopy is not necessary, since this function is called recusively.
    right = right.copy()

    for key, value in left.items():
        if key in right:
            if isinstance(value, collections.abc.Mapping) and isinstance(right[key], collections.abc.Mapping):
                right[key] = recursive_merge(value, right[key])

    merged = left.copy()
    merged.update(right)

    return merged

