"""Rewrite pyproject.toml to use minimum dependency versions.

This is a script because it is broadly applicable beyond bloom. As such, this
file is placed in the public domain. No warranty is provided.

Originally written by A5rocks.
"""

try:
    import tomli
except ImportError:
    import pip._vendor.tomli as tomli

import pathlib

import tomli_w

try:
    from packaging.requirements import Requirement
    from packaging.version import Version
except ImportError:
    from pip._vendor.packaging.requirements import Requirement
    from pip._vendor.packaging.version import Version

if __name__ == '__main__':
    # this relies on file ordering
    project = pathlib.Path(__file__) / '..' / '..'
    pyproject = project / 'pyproject.toml'
    pyproject = pyproject.resolve()

    with open(pyproject, 'rb') as f:
        toml = tomli.load(f)

    dependencies = toml['project']['dependencies']

    requirements = [Requirement(dep) for dep in dependencies]

    for requirement in requirements:
        current_lowest = None
        for spec in requirement.specifier:
            if spec.operator not in ('==', '>=', '~=', '>', '==='):
                # version provided is not a minimum bound
                continue

            # currently the program has a specifier.
            # it should find the one that supports the lowest version!
            version = Version(spec.version)
            if current_lowest is None or version < current_lowest:
                current_lowest = version

        assert current_lowest, f'should have a minimum bound on "{requirement.name}".'

        # pin to current_lowest
        requirement.specifier &= f'=={current_lowest}'

    toml['project']['dependencies'] = [str(req) for req in requirements]

    with open(pyproject, 'wb') as f:
        tomli_w.dump(toml, f)
