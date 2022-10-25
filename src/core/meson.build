pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
coredir = join_paths(pkgdatadir, 'vanilla_updater/core')

sources = [
  '__init__.py',
  'distro.py',
  'updates_repository.py',
]

install_data(sources, install_dir: coredir)