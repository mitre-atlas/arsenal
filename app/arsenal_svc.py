import os
import sys
import subprocess
from typing import List
from venv import EnvBuilder
from subprocess import check_call, DEVNULL, STDOUT
from aiohttp_jinja2 import template
from app.utility.base_service import BaseService

COUNTERFIT_MODULE = 'counterfit'
COUNTERFIT_VERSION = '1.1.0'
COUNTERFIT_BRANCH = 'main'
COUNTERFIT_EXTRAS = 'dev'

class ArsenalService(BaseService):

    def __init__(self, services):
        self.auth_svc = services.get('auth_svc')
        self.file_svc = services.get('file_svc')
        self.data_svc = services.get('data_svc')
        self.contact_svc = services.get('contact_svc')
        self.log = self.add_service('arsenal_svc', self)
        self.arsenal_dir = os.path.join('plugins', 'arsenal')
        self.venv_dir = os.path.join(os.environ['HOME'], 'venv')


    @template('arsenal.html')
    async def splash(self, request):
        return dict()


    async def populate_venv(self, env_name: str='arsenal_venv',
                            with_counterfit: bool=True) -> None:
        """
        Functionality to create and populates a virtual environment with specified name.

        If with_counterfit == True, the newly created virtual environment will be
        populated with the "counterfit" module and it's required dependencies.
        
        Args: 
            env_name: Specifies which sub-directory to create the environment 
                        in. By convention, all environments are stored in the same directory,
                        so the sub-directory name is used to differentiate each environment.

            with_counterfit: Indicates if the "counterfit" module should automatically
                                be installed into the newly created virtual environment.
                                
        Returns:
            None
        """
        # ensure env_name venv exists
        await self._create_venv(env_name=env_name)

        # if desired, auto-install counterfit into the env_name virtual environment
        # NOTE: cfit install downloads nltk data to ~/nltk_data, which is outside
        # of .../plugins/arsenal dir; resolve later
        if with_counterfit:
            await self._install_counterfit(env_name)

    
    async def _install_counterfit(self, env_name: str) -> None:
        """
        Functionality to check if counterfit module exists in specified virtual
            environment, and if not, install module.
            
        Arguments:
            env_name: virtual environment name
            
        Returns:
            None
        """
        cmd1 = [await self._get_venv_exe_path(env_name=env_name)]
        cmd1.extend(['-m', 'pip', 'list'])
        cmd2 = ['grep', COUNTERFIT_MODULE]
        p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
        # Allow p1 to receive a SIGPIPE if p2 exits.    
        p1.stdout.close()  
        out = p2.communicate()[0]
        if out:
            out_dict = dict(zip(['name', 'version'], out.decode('utf-8').split()))
            self.log.debug('\nout_dict:\n{}'.format(out_dict))
            assert out_dict['version'] == COUNTERFIT_VERSION
            assert out_dict['name'] == COUNTERFIT_MODULE
        else:
            await self._pip_install_modules(
                env_name=env_name, 
                modules=[
                    f'counterfit[{COUNTERFIT_EXTRAS}] @ git+https://github.com/Azure/counterfit.git@{COUNTERFIT_BRANCH}'
                    ])


    async def _create_venv(self, 
                           env_name: str = 'arsenal_venv',
                           clear: bool = False,
                           with_pip: bool = True,
                           core_venv_deps: List[str] = ['pip', 'wheel', 'setuptools'],
                           upgrade_core_deps: bool = True) -> None:
        """
        Functionality to create a virtual environment using the venv package for Python. 

        Arguments:
            env_name: Specifies which sub-directory to create the environment 
                        in. By convention, all environments are stored in the same directory,
                        so the sub-directory name is used to differentiate each environment. 

            clear: If True, delete the contents of the environment directory if it
                    already exists, before environment creation.

            with_pip: If True, ensure pip is installed in the virtual environment.
                        Caldera lists pip3 as a core requirement, so we expect pip to already
                        be installed... but it doesn't hurt to make sure.

            core_venv_deps: A list containing the base venv modules that will be
                                installed in the virutal environment.

            upgrade_core_deps: If True, the base venv modules will be updated to the 
                                  latest on PyPI.
                                  
        Returns:
            None
        """
        self.log.debug('\nBuilding %s...', env_name)
        # get relative path, create() will convert env_dir to an abspath 
        env_dir = os.path.join(self.venv_dir, env_name)
        # check if desired env_name already exists
        if os.path.exists(env_dir): 
            msg = 'will' if clear else 'will not'
            self.log.warning('env_name: %s already exists. The contents of the ' + 
                             'environment %s be deleted.', env_name, msg)
        # Only call EnvBuilder if the venv dir doesn't exist. Post-demo, error checking
        # should be thorough (ex: venv dir could exist and be empty, not have pip, etc.) 
        else:
            # create the builder object and configure using provided input arguments
            builder = EnvBuilder(clear=clear, with_pip=with_pip)
            # create the venv
            builder.create(env_dir=env_dir)
            self.log.debug('\nVirtual environment has been created at:\n%s', env_dir)

        # ensure proper usage of function args
        if not with_pip and 'pip' in core_venv_deps:
            # NOTE: This won't "kill" the C2 server, but it will "disable" arsenal.
            # A descriptive log message is needed with level ERROR.
            self.log.error(f'pip is a required dependency to build {env_name},'
                               'but build errored with the following error:\n')

        # install desired base venv modules as needed
        if len(core_venv_deps) > 0:
            await self._pip_install_modules(env_name=env_name, 
                                            modules=core_venv_deps, 
                                            upgrade=upgrade_core_deps
                                            )


    async def _pip_install_modules(self, 
                                   env_name: str = 'ml_venv',
                                   modules: List[str] = None, 
                                   upgrade: bool = False) -> bool:
        """
        Functionality to install specified modules in the given virtual environment

        Arguments: 
            env_name: name of virtual environment to install packages into
            modules: packages to install
            upgrade: whether to upgrade packages at install
            
        Returns:
            the status of command output
        """
        # using pip as a python module (-m), instead of directly executing "pip ..."
        env_py_exe = await self._get_venv_exe_path(env_name=env_name)

        cmd = [env_py_exe] + ['-m', 'pip', 'install']
        if upgrade:
            cmd.extend(['-U'])
        if modules:
            cmd.extend(modules)

        # once correct command is built, run it in a subprocess
        check_call(cmd, stdout=DEVNULL, stderr=STDOUT)


    async def _get_venv_exe_path(self, 
                                 env_name: str='ml_venv',
                                 out_path: str='env_exe') -> str:
        """
        Functionality to get the executable path of the virtual environment
        
        For out_path == 'env_exe', the name of the Python interpreter in the virtual
        environment is returned. For out_path == 'bin_path', the script path for the 
        virtual environment is returned.
        
        NOTE: Assume linux is only supported platform, which ensures bin_name == 'bin'.

        Args:
            env_name: Specifies which sub-directory to create the environment 
                        in. By convention, all environments are stored in the same directory,
                        so the sub-directory name is used to differentiate each environment. 
            out_path: Specifies which virtual environment executable path will be
                        returned. Choose between 'env_exe' and 'bin_path'.

        Return:
            desired executable used by the virtual environment.
        """
        # check for invalid usage
        if out_path not in ['env_exe', 'bin_path']:
            self.log.error('Invalid value of %s has been passed for the out_path ' +
                           'argument. Valid values: env_exe, bin_path.', out_path)
            raise ValueError
        
        _, exename = os.path.split(os.path.abspath(sys.executable))
        binpath = os.path.join(self.venv_dir, env_name, 'bin')
        # log certain attributes of the "context" object (used in EnvBuilder class)
        self.log.debug('\nexecutable: %s\nbin_path: %s\npython_exe: %s',
                       sys.executable, binpath, exename)
        
        # return path to desired executable
        if out_path != 'bin_path':
            binpath = os.path.join(binpath, exename)
        return binpath