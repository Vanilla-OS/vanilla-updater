pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
utilsdir = join_paths(pkgdatadir, 'vanilla_updater/utils')

sources = [
  '__init__.py',
  'run_async.py',
]

install_data(sources, install_dir: utilsdir)