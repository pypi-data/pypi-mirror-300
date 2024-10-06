from setuptools_scm.version import get_local_node_and_date
import re


def local_scheme(version):
    version.node = re.sub(
        r'.',
        lambda match: str(ord(match.group(0))),
        version.node
    )
    return get_local_node_and_date(version).replace('+', '').replace('.d', '')
