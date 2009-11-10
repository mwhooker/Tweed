import daemon
import lockfile
import signal

from dispatch import (
        initial_program_setup,
        do_tweed_loop,
        program_cleanup,
        reload_program_config,
        )


context = daemon.DaemonContext(
        working_directory='./',
        pidfile=lockfile.FileLock('./tweed.pid'),
        )


context.signal_mnap = {
        signal.SIGTERM: program_cleanup,
        signal.SIGHUP: 'terminate',
        signal.SIGUSR1: reload_program_config,
        }


initial_program_setup()

with context:
    do_tweed_loop()
