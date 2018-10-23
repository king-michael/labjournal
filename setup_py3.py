from distutils.core import setup

setup(
    name='labjournal',
    version='0.1beta',
    packages=['docs.source.templates_themes.sphinx_rtd_theme.docs.demo.test_py_module',
              'docs.source.templates_themes.sphinx_rtd_theme.tests',
              'docs.source.templates_themes.sphinx_rtd_theme.sphinx_rtd_theme', 'examples.setup_db.micha',
              'examples.setup_db.micha.create_database', 'labjournal', 'labjournal.gui', 'labjournal.gui.tabs',
              'labjournal.gui.tabs.InfoEntry', 'labjournal.gui.tabs.InfoEntry.LAMMPS',
              'labjournal.gui.tabs.InfoEntry.GROMACS', 'labjournal.gui.popups', 'labjournal.gui.popups.DialogSettings',
              'labjournal.gui.QtExtensions', 'labjournal.core', 'labjournal.utils', 'labjournal.analysis',
              'labjournal.analysis.LAMMPS', 'labjournal.templates', 'labjournal.templates.LAMMPS',
              'labjournal.workflows', 'labjournal.workflows.tasks', 'labjournal.workflows.tasks.VMD',
              'labjournal.workflows.tasks.LAMMPS', 'labjournal.external_libs', 'labjournal.external_libs.pizza',
              'labjournal.user_specific', 'labjournal.user_specific.micha', 'labjournal.user_specific.micha.mediawiki'],
    # url='',
    # license='',
    author='Michael King, Andrej Berg',  # FixMe: geht hier ne liste?
    author_email='michael.king@uni-konstanz.de, andrej.berg@uni-konstanz.de',  # FixMe: geht hier ne liste?
    description='LabJournal',  # FixMe: Bessere Beschreibung
    install_requires=[
        'numpy',
        'matplotlib',
        'sqlalchemy',
        'PyQt5',
        'PyOpenGL',
        'qdarkstyle',
      ]
)
