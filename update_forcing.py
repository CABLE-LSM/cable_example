import argparse
import os
from pathlib import Path

import yaml
import f90nml

config_path = Path("config.yaml")
archive_path = Path("archive")
work_path = Path("work")
work_input_path = work_path / "INPUT"
cable_nml_file_name = "cable.nml"
restart_calendar_file_name = "cable.res.yaml"
met_forcing_vars = [
    "Rainf",
    "Snowf",
    "LWdown",
    "SWdown",
    "PSurf",
    "Qair",
    "Tair",
    "Wind",
]


def get_prior_restart():
    """Return the path to the prior restart file as inferred by payu."""
    if archive_path.is_dir():
        restart_dirs = sorted(archive_path.glob("restart*"))
        if restart_dirs:
            return restart_dirs[-1]
    with config_path.open("r") as file:
        config = yaml.safe_load(file)
    return config.get("restart")


def get_year(restart_dir):
    """Return the year value of a payu restart."""
    restart_calendar_file = Path(restart_dir, restart_calendar_file_name)
    with restart_calendar_file.open("r") as calendar_file:
        restart_info = yaml.safe_load(calendar_file)
    return restart_info["year"]


def get_forcing_path(variable, year):
    """Return the met forcing file path for a given variable and year."""
    for path in work_input_path.glob(f"*{variable}*{year}*.nc"):
        return path
    msg = f"Unable to infer met forcing path for variable {variable} for year {year}."
    raise FileNotFoundError(msg)


def update_forcing(offset=None, repeat=None):
    """Update the namelist file to use the correct met forcing."""
    cable_nml = f90nml.read(work_path / cable_nml_file_name)

    prior_restart = get_prior_restart()
    year = get_year(prior_restart) if prior_restart else cable_nml["cable"]["ncciy"]

    if offset:
        year += offset[1] - offset[0]

    if repeat:
        year = repeat[0] + ((year - repeat[0]) % (repeat[1] - repeat[0] + 1))

    for var in met_forcing_vars:
        path = get_forcing_path(var, year)
        cable_nml["cable"]["gswpfile"][var] = str(path.relative_to(work_path))

    f90nml.write(cable_nml, work_path / cable_nml_file_name, force=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--offset", required=False, type=int, nargs=2)
    parser.add_argument("--repeat", required=False, type=int, nargs=2)
    args = parser.parse_args()
    update_forcing(offset=args.offset, repeat=args.repeat)
