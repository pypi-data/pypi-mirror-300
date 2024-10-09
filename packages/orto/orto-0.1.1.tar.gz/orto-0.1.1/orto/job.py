import os
import subto.job as sjob
import copy


class OrcaJob():
    '''
    Class to generate submission scripts for ORCA calculation\n\n

    Submission script format is \n

    ...............\n
    SCHEDULER BLOCK\n
    ...............\n
    LOAD_BLOCK\n
    ...............\n
    PRE-ORCA_BLOCK\n
    ...............\n
    $(which orca) input_file > output_file\n
    ...............\n
    POST-ORCA_BLOCK\n
    ...............\n

    Attributes
    ----------
    input_file: str
        Orca input file for which a submission script is created
    output_file: str
        Orca output file name. Default is same as input with extension \n
        replaced by .out
    job_file: str
        Submission script name. Default is same as input with extension \n
        replaced by scheduler job file extension e.g. '.slm'
    job_name: str
        Job name. Default is same as input without extension
    scheduler_name: str {'slurm'}
        Scheduler system name
    pre_orca: str
        Commands for pre-orca block
    post_orca: str
        Commands for post-orca block
    '''

    SCHEDULER_TO_CLASS: dict[str, sjob.Job] = {
        'slurm': sjob.SlurmJob
    }
    SUPPORTED_SCHEDULERS = list(SCHEDULER_TO_CLASS.keys())

    def __init__(self, input_file, scheduler='slurm', **kwargs) -> None:

        self.input_file = input_file
        self.scheduler_name = scheduler

        # Set defaults
        self.output_file = 'from_head'
        self.job_file = 'from_head'
        self.job_name = 'from_head'
        self.load = ''
        self.pre_orca = ''
        self.post_orca = ''

        # If provided set attrs using kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

        return

    @property
    def job_file(self):
        return self._job_file

    @job_file.setter
    def job_file(self, value: str):
        if value == 'from_head':
            self._job_file = '{}{}'.format(
                os.path.splitext(self.input_file)[0],
                self.scheduler_job_class.EXTENSION
            )
        else:
            self._job_file = value

    @property
    def job_name(self):
        return self._job_name

    @job_name.setter
    def job_name(self, value: str):
        if value == 'from_head':
            self._job_name = os.path.splitext(self.input_file)[0]
        else:
            self._job_name = value

    @property
    def input_file(self):
        return self._input_file

    @input_file.setter
    def input_file(self, value: str):
        self._input_file = value

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, value: str):
        if value == 'from_head':
            self._output_file = os.path.splitext(self.input_file)[0] + '.out'
        else:
            self._output_file = value

    @property
    def pre_orca(self):
        rvalue = copy.copy(self._pre_orca)
        rvalue = rvalue.replace('<input>', self.input_file)
        rvalue = rvalue.replace('<output>', self.output_file)
        rvalue = rvalue.replace('<head>', os.path.splitext(self.input_file)[0])
        return rvalue

    @pre_orca.setter
    def pre_orca(self, value: str):
        self._pre_orca = value

    @property
    def post_orca(self):
        rvalue = copy.copy(self._post_orca)
        rvalue = rvalue.replace('<input>', self.input_file)
        rvalue = rvalue.replace('<output>', self.output_file)
        rvalue = rvalue.replace('<head>', os.path.splitext(self.input_file)[0])
        return rvalue

    @post_orca.setter
    def post_orca(self, value: str):
        self._post_orca = value

    @property
    def scheduler_name(self):
        return self._scheduler_name

    @scheduler_name.setter
    def scheduler_name(self, value: str):
        if value in self.SUPPORTED_SCHEDULERS:
            self._scheduler_name = value
        else:
            raise ValueError(
                f'Specified scheduler_name {value} is unsupported'
            )

    @property
    def scheduler_job_class(self) -> sjob.Job:
        return self.SCHEDULER_TO_CLASS[self.scheduler_name]

    @property
    def orca_command(self):
        return f'$(which orca) {self.input_file} > {self.output_file}'

    def write_script(self, verbose: bool = True, **kwargs):
        '''
        Writes submission script to file

        Parameters
        ----------
        verbose: bool, default True
            If True, jobscript location is written to screen
        '''

        if len(self.load):
            self.load += '\n\n'
        if len(self.pre_orca):
            self.pre_orca += '\n\n'
        if len(self.post_orca):
            self.post_orca = '\n' + self.post_orca + '\n\n'

        # Generate content of script
        content = '{}{}{}\n{}'.format(
            self.load,
            self.pre_orca,
            self.orca_command,
            self.post_orca
        )

        # And use scheduler object to submission system job object
        job = self.scheduler_job_class(
            job_file=self.job_file,
            job_name=self.job_name,
            content_block=content,
            **kwargs
        )

        # Write script
        job.write_script(verbose=verbose)

        return
