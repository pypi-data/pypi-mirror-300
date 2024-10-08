# -*- coding: utf-8 -*-
import os
from collections import defaultdict
import numpy as np
from aiida import orm # type: ignore
from aiida.engine import CalcJob # type: ignore
from aiida.common.datastructures import CalcInfo, CodeInfo # type: ignore


class InqCalculation(CalcJob):
    """
    Base calculation class for the INQ code.
    """

    # Default input and output files
    _DEFAULT_INPUT_FILE  = 'aiida.in'
    _DEFAULT_OUTPUT_FILE = 'aiida.out'
    _DEFAULT_STDOUT_FILE = 'std.out'
    _DEFAULT_ERROR_FILE  = 'std.err'
    _DEFAULT_RESULTS_FILE = 'aiida.results'
    _DEFAULT_INQ_SUBFOLDER = './.inq/'

    # When restarting, will copy the contents of this folder
    _restart_copy_from = os.path.join(_DEFAULT_INQ_SUBFOLDER, '*')

    # Where to copy files to from a parent_folder
    _restart_copy_to = _DEFAULT_INQ_SUBFOLDER
 
    @classmethod
    def define(cls, spec):
        """Define the process specification."""
        # yapf: disable
        super().define(spec)
        spec.input(
            'parameters', 
            valid_type=orm.Dict, 
            required=True,
            help='Input parameters for the input file.'
        )
        spec.input(
            'structure', 
            valid_type=orm.StructureData, 
            required=True,
            help='The input structure.'
        )
        spec.input(
            'settings', 
            valid_type=orm.Dict, 
            required=False,
            help=(
                'Optional parameters to affect the way the calculation job '
                'is performed.'
            )
        )
        spec.input(
            'parent_folder',
            valid_type=orm.RemoteData,
            required=False,
            help=(
                'Optional working directory of a previous calculation to '
                'restart from.'
            )
        )
        spec.input(
            'metadata.options.input_filename', 
            valid_type=str, 
            default=cls._DEFAULT_INPUT_FILE
        )
        spec.input(
            'metadata.options.output_filename', 
            valid_type=str, 
            default=cls._DEFAULT_OUTPUT_FILE
        )
        spec.input(
            'metadata.options.results_filename',
            valid_type=str,
            default=cls._DEFAULT_RESULTS_FILE
        )
        spec.input(
            'metadata.options.scheduler_stdout',
            valid_type=str,
            default=cls._DEFAULT_STDOUT_FILE
        )
        spec.input(
            'metadata.options.scheduler_stderr',
            valid_type=str,
            default=cls._DEFAULT_ERROR_FILE
        )
        spec.input(
            'metadata.options.parser_name', 
            valid_type=str, 
            default='inq.inq'
        )

        spec.output(
            'output_parameters', 
            valid_type=orm.Dict
        )
        spec.output(
            'output_structure', 
            valid_type=orm.StructureData, 
            required=False,
            help='The relaxed output structure.'
        )

        spec.default_output_node = 'output_parameters'

        spec.exit_code(201, 'NO_ENERGY_CUTOFF_SPECIFIED',
            message='At minimum the energy cutoff must be specified.')
        spec.exit_code(202, 'NO_RUN_TYPE_SPECIFIED',
            message='No run type was specified in the input parameters.')
        spec.exit_code(203, 'PARAMETER_NOT_REQUESTED',
            message='Input parameter was not specified for this result.')

        # yapf: enable

    def prepare_for_submission(self, folder):
        """
        Prepare the calculation job for submission by transforming input nodes
        into input files. In addition to the input files being written to the
        sandbox folder, a `CalcInfo` instance will be returned that contains 
        lists of files that need to be copied to the remote machine before 
        job submission, as well as file lists that are to be retrieved after 
        job completion. 
        
        :param folder: a sandbox folder to temporarily write files on disk. 
        
        :return: `aiida.common.datastructures.CalcInfo` instance.
        """

        # Verify inputs
        #self.verify_inputs()

        # Initialize settings if set
        if 'settings' in self.inputs:
            settings = self.inputs.settings.get_dict() # Might to make a check for this
        else:
            settings = {}

        # Initiate variables
        parameters = self.inputs.parameters.get_dict()
        results = parameters.pop('results', {})

        # Check if the cutoff has been given.
        energy = parameters.get('electrons', {})
        cutoff = energy.get('cutoff', None)
        if not cutoff:
            self.report('The energy cutoff was not specified.')
            self.exit_codes.NO_ENERGY_CUTOFF_SPECIFIED

        structure = self.inputs.structure
        atoms = structure.get_ase()

        # Create subfolders for scratch and permanent data
        folder.get_subfolder(self._DEFAULT_INQ_SUBFOLDER, create=True)

        input_filename = folder.get_abs_path(self._DEFAULT_INPUT_FILE)
        f = open(input_filename, 'w')
        # Initiate the initial settings
        f.write("""#!/bin/bash

set -e
set -x

""")
        # Initiate the cell
        cell = atoms.cell
        scale = np.max(cell)
        sc = cell/scale
        f.write(f"inq cell {' '.join(sc[0].astype('str'))} {' '.join(sc[1].astype('str'))} {' '.join(sc[2].astype('str'))} scale {scale} angstrom\n")

        # Add the atoms
        for atom in atoms:
            f.write(f"inq ions insert fractional {atom.symbol} {' '.join(atom.scaled_position.astype('str'))}\n")

        # Iterate through the parameters
        run_type = parameters.pop('run', None)
        if run_type is None:
            self.report(f'There was no run type specified.')
            self.exit_codes.NO_RUN_TYPE_SPECIFIED
        else:
            if type(run_type) is dict:
                run_type = list(run_type.keys())[0]
        for key, val in parameters.items():
            for k, v in val.items():
                if type(v) is list:
                    for item in v:
                        f.write(f"inq {key} {k} {item}\n")
                else:
                    f.write(f"inq {key} {k} {v}\n")

        f.write(f'inq run {run_type}\n')

        # Print out the final structure
        f.write(f'inq cell >> {self._DEFAULT_RESULTS_FILE}\n')
        f.write(f'inq ions >> {self._DEFAULT_RESULTS_FILE}\n')

        # Set any requested results to print to the results file
        for key, val in results.items():
            for k, v in val.items():
                if str(k).lower() in ['forces', 'dipole', 'current', 'total-energy', 'time']:
                    # Check if dipole and current were set in the input parameters.
                    if str(k).lower() in ['dipole', 'current']:
                        real_time = parameters.get('real-time', None)
                        if real_time is None:
                            self.report(f'Input parameter not set for `{k}` results.')
                            self.exit_codes.PARAMETER_NOT_REQUESTED
                    f.write(f'echo ""\necho "{k.capitalize()}:" >> {self._DEFAULT_RESULTS_FILE}\n')
                f.write(f"inq results {key} {k} {v} >> {self._DEFAULT_RESULTS_FILE}\n")

        # Echo that AiiDA finished.
        # Will be used to determine if a job finished.
        f.write(f'\necho "AiiDA DONE"')

        f.flush()

        local_copy_list = []
        remote_copy_list = []
        remote_symlink_list = []

        # Setting a parent folder from previous calculation
        symlink = settings.pop('PARENT_FOLDER_SYMLINK', True)
        if symlink:
            if 'parent_folder' in self.inputs:
                # Put the folder from the previous calculation
                remote_symlink_list.append((
                    self.inputs.parent_folder.computer.uuid,
                    os.path.join(self.inputs.parent_folder.get_remote_path(),
                                 self._restart_copy_from), self._restart_copy_to
                ))
        else:
            if 'parent_folder' in self.inputs:
                remote_copy_list.append((
                    self.inputs.parent_folder.computer.uuid,
                    os.path.join(self.inputs.parent_folder.get_remote_path(),
                                 self._restart_copy_from), self._restart_copy_to
                ))

        _default_commandline_params = [self._DEFAULT_INPUT_FILE]
        codeinfo =  CodeInfo()
        codeinfo.cmdline_params = _default_commandline_params
        codeinfo.stdout_name = self._DEFAULT_OUTPUT_FILE
        codeinfo.stderr_name = self._DEFAULT_ERROR_FILE
        codeinfo.code_uuid = self.inputs.code.uuid

        calcinfo = CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.stdin_name = self._DEFAULT_INPUT_FILE
        calcinfo.stdout_name = self._DEFAULT_OUTPUT_FILE
        calcinfo.local_copy_list = local_copy_list
        calcinfo.remote_copy_list = remote_copy_list
        calcinfo.remote_symlink_list = remote_symlink_list
        calcinfo.retrieve_list = []
        calcinfo.retrieve_temporary_list = [self._DEFAULT_OUTPUT_FILE,
                                            self._DEFAULT_ERROR_FILE,
                                            self._DEFAULT_RESULTS_FILE]

        calcinfo.retrieve_singlefile_list = []

        return calcinfo