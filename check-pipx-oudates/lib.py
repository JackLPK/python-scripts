"""
    Synchronous check
    todo:
        check injected packages?
"""
import subprocess
import sys
import time

from typing import List


class CMD:
    _pipx = 'pipx'
    _list = 'list'
    _runpip = 'runpip'
    _flag_oudated = '-o'
    
    @staticmethod
    def pipx_list(): 
        return [CMD._pipx, CMD._list]

    @staticmethod
    def pipx_runpip_pkg_list_oudate(pkg: str):
        return [CMD._pipx, CMD._runpip, pkg, CMD._list, CMD._flag_oudated]


def shell_response(cmd: List):
    """ uses subprocess.run() """
    process = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    output = process.stdout.split('\n')
    if process.returncode != 0:
        print(process.stderr)
        sys.exit(1)
    return output


def get_top_lvl_pkgs():
    """ Return a list of names of installed packages """
    lines = shell_response(CMD.pipx_list())

    # select only top level packages
    top_lvl_pkgs = [line for line in lines if line.startswith('   package')]

    # clean: strip left space; right versions, etc
    top_lvl_pkgs = [line.lstrip() for line in top_lvl_pkgs]
    top_lvl_pkgs = [line.split(' ')[1] for line in top_lvl_pkgs]
    return top_lvl_pkgs


def pkg_is_od(top_lvl_pkg: str, lines: List[str]):
    """ check if pkg's name is in 'pip list -o' """
    for line in lines:    # pkg and dependencies
        if top_lvl_pkg in line:    # text contain pkg's name
            _pkg, version, latest, type_ = line.split()
            return f'    {top_lvl_pkg:<20}{version:>8}{"->":^4}{latest} ({type_})'
    return False


def check_pkg(pkg: str):
    """ Check(display) if this package has new version """
    lines = shell_response(CMD.pipx_runpip_pkg_list_oudate(pkg))
    od_pkgs = pkg_is_od(pkg, lines)
    if od_pkgs:
        print(f'{pkg}:')
        print(od_pkgs)


def main():
    """ Simple Synchronous main """
    print('Outdated Top Level packages:')
    top_lvl_pkgs = get_top_lvl_pkgs()

    for pkg in top_lvl_pkgs:
        check_pkg(pkg)


if __name__ == "__main__":
    START = time.time()
    main()
    STOP = time.time()
    print(f'Total time used: {STOP - START:02f} s')
