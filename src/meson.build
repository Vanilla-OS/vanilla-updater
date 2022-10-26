pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'vanilla_updater')
gnome = import('gnome')

gnome.compile_resources('vanilla-updater',
  'vanilla-updater.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'vanilla-updater.in',
  output: 'vanilla-updater',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

configure_file(
  output: 'vanilla-updater-cli',
  input: 'vanilla-updater-cli.in',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

subdir('core')
subdir('utils')

vanilla_updater_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(vanilla_updater_sources, install_dir: moduledir)
