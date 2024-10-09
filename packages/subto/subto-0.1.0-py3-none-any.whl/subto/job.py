import os
from . import utils as ut
from abc import ABC, abstractmethod


class Job(ABC):
    '''
    Abstract class on which all submission/job scripts classes are based.
    '''

    @property
    @abstractmethod
    def EXTENSION() -> str:
        'Default extension for submission/job script file'
        raise NotImplementedError

    @property
    @abstractmethod
    def SUBMIT_COMMAND() -> str:
        'Submission command for this scheduler'
        raise NotImplementedError


class SlurmJob(Job):
    '''
    Class to generate Slurm submission/job scripts\n

    Submission script format is \n

    ...............\n
    SCHEDULER BLOCK\n
    ...............\n
    CONTENT BLOCK
    ...............\n

    Attributes
    ----------
    job_file: str
        Submission script name
    job_name: str
        --job-name value, default is taken from job_file
    account: str
        --account value
    partition: str
        --partition value
    error: str
        --error value
    output: str
        --output value
    mem_per_cpu: str
        --mem-per-cpu value
    cpus_per_task: str
        --cpus-per-task value
    ntasks_per_node: str
        --ntasks-per-node value
    ntasks: str
        --ntasks value
    nodes: str
        --nodes value
    signal: str
        --signal value
    qos: str
        --qos value
    gpus_per_node: str
        --gpus-per-node
    time: str
        --time value
    content_block: str
        Commands to include in jobscript after scheduler block
    '''

    #: Submission/job script file extension
    EXTENSION: str = '.slm'

    #: Submission command for this scheduler
    SUBMIT_COMMAND: str = 'sbatch'

    __slots__ = [
        'job_file',
        'job_name',
        'account',
        'partition',
        'error',
        'output',
        'mem_per_cpu',
        'cpus_per_task',
        'ntasks',
        'ntasks_per_node',
        'nodes',
        'signal',
        'qos',
        'gpus_per_node',
        'time',
        'content_block',
        'mail_user',
        'mail_type',
    ]

    def __init__(self, job_file, **kwargs) -> None:

        # Slurm flag defaults
        self.job_file = job_file
        self.job_name = os.path.splitext(self.job_file)[0]
        self.account = ''
        self.partition = ''
        self.error = ''
        self.output = ''
        self.mem_per_cpu = ''
        self.cpus_per_task = ''
        self.ntasks = ''
        self.ntasks_per_node = ''
        self.nodes = ''
        self.signal = ''
        self.qos = ''
        self.gpus_per_node = ''
        self.time = ''
        self.mail_user = ''
        self.mail_type = ''
        self.interpreter_directive = '#!/bin/bash -l'

        self.content_block = ''

        for key, value in kwargs.items():
            setattr(self, key, value)

        return

    def apply_template_file(self, file_name: str):
        '''
        Sets attributes using file containing slurm configuration commands\n

        File is formatted as either\n
        #SBATCH FLAG=VALUE or FLAG=VALUE\n
        Flag does not have to contain -- at start.

        Parameters
        ----------
        file_name: str
            Template file to read
        '''

        config = self.read_template_file(file_name)

        for key, value in config.items():
            setattr(self, key, value)

        return

    @staticmethod
    def read_template_file(file_name: str):
        '''
        Reads file containing slurm configuration commands\n

        File is formatted as either\n
        #SBATCH FLAG=VALUE or FLAG=VALUE\n
        Flag does not have to contain -- at start.

        Parameters
        ----------
        file_name: str
            Template file to read

        Returns
        -------
        dict
            Keys are flags, values are values
        '''

        template = {}
        with open(file_name, 'r') as f:
            for line in f:
                if len(line):
                    if '#SBATCH ' in line:
                        line = line[8:]
                    key = line.split('=')[0]
                    val = line.split('=')[1]

                    if key[0:2] == '--':
                        key = key[2:]

                    key = key.replace('-', '_')

                    val = val.rstrip('\n')
                    template[key] = val

        return template

    def write_script(self, verbose: bool = True):
        '''
        Writes submission script to file

        Parameters
        ----------
        verbose: bool, default True
            If True, jobscript location is written to screen
        '''

        with open(self.job_file, 'w') as f:
            f.write('{} \n\n'.format(self.interpreter_directive))
            for attribute in self.__slots__:
                if attribute not in ['content_block', 'job_file'] and len(str(getattr(self, attribute))): # noqa
                    f.write(
                        '#SBATCH --{}={}\n'.format(
                            attribute.replace('_', '-'),
                            getattr(self, attribute)
                        )
                    )
            f.write('\n')
            f.write(self.content_block)

        if verbose:
            ut.cprint(f'Jobscript written to {self.job_file}', 'blue')

        return
