"""This module provides wrapper for the Flame graph visualization"""

from __future__ import annotations

# Standard Imports
from typing import TYPE_CHECKING
import os
import tempfile

# Third-Party Imports

# Perun Imports
from perun.profile import convert
from perun.utils import mapping
from perun.utils.common import script_kit
from perun.utils.external import commands

if TYPE_CHECKING:
    from perun.profile.factory import Profile


def draw_flame_graph_difference(
    lhs_profile: Profile,
    rhs_profile: Profile,
    width: int = 1200,
    title: str = "",
    profile_key: str = "amount",
    minimize: bool = False,
) -> str:
    """Draws difference of two flame graphs from two profiles

    :param lhs_profile: baseline profile
    :param rhs_profile: target_profile
    :param width: width of the graph
    :param profile_key: key for which we are constructing profile
    :param title: if set to empty, then title will be generated
    """
    # First we create two flamegraph formats
    lhs_flame = convert.to_flame_graph_format(
        lhs_profile, profile_key=profile_key, minimize=minimize
    )
    with open("lhs.flame", "w") as lhs_handle:
        lhs_handle.write("".join(lhs_flame))
    rhs_flame = convert.to_flame_graph_format(
        rhs_profile, profile_key=profile_key, minimize=minimize
    )
    with open("rhs.flame", "w") as rhs_handle:
        rhs_handle.write("".join(rhs_flame))

    header = lhs_profile["header"]
    profile_type = header["type"]
    cmd, workload = (header["cmd"], header["workload"])
    title = title if title != "" else f"{profile_type} consumption of {cmd} {workload}"
    # TODO: Make better
    units = header["units"].get(profile_type, "samples")

    diff_script = script_kit.get_script("difffolded.pl")
    flame_script = script_kit.get_script("flamegraph.pl")
    difference_script = (
        f"{diff_script} -n lhs.flame rhs.flame "
        f"| {flame_script} --title '{title}' --countname {units} --reverse "
        f"--width {width * 2}"
    )
    out, _ = commands.run_safely_external_command(difference_script)
    os.remove("lhs.flame")
    os.remove("rhs.flame")

    return out.decode("utf-8")


def draw_flame_graph(
    profile: Profile,
    width: int = 1200,
    max_trace: int = 0,
    max_resource: float = 0.0,
    title: str = "",
    profile_key: str = "amount",
    minimize: bool = False,
) -> str:
    """Draw Flame graph from profile.

        To create Flame graphs we use perl script created by Brendan Gregg.
        https://github.com/brendangregg/FlameGraph/blob/master/flamegraph.pl

    :param profile: the memory profile
    :param width: width of the graph
    :param profile_key: key for which we are constructing profile
    :param title: if set to empty, then title will be generated
    """
    # converting profile format to format suitable to Flame graph visualization
    flame = convert.to_flame_graph_format(profile, profile_key=profile_key, minimize=minimize)

    header = profile["header"]
    profile_type = header["type"]
    cmd, workload = (header["cmd"], header["workload"])
    title = title if title != "" else f"{profile_type} consumption of {cmd} {workload}"
    units = mapping.get_unit(mapping.get_readable_key(profile_key))

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write("".join(flame).encode("utf-8"))
        tmp.close()
        cmd = " ".join(
            [
                script_kit.get_script("flamegraph.pl"),
                tmp.name,
                "--cp",
                "--title",
                f'"{title}"',
                "--countname",
                f"{units}",
                "--reverse",
                "--width",
                str(width),
                "--maxtrace",
                f"{max_trace}",
                "--minwidth",
                "1",
            ]
        )
        if max_resource > 0.0:
            cmd += f' --total {max_resource} --rootnode "Maximum (Baseline, Target)"'
        out, _ = commands.run_safely_external_command(cmd)
        os.remove(tmp.name)
    return out.decode("utf-8")
