from distutils.core import setup


# sudo aptitude install python-pyqt5.qtopengl

setup(
    name='old_labjournal',
    version='0.1beta',
    packages=['docs.source.templates_themes.sphinx_rtd_theme.docs.demo.test_py_module',
              'docs.source.templates_themes.sphinx_rtd_theme.tests',
              'docs.source.templates_themes.sphinx_rtd_theme.sphinx_rtd_theme', 'examples.setup_db.micha',
              'examples.setup_db.micha.create_database', 'old_labjournal', 'old_labjournal.gui', 'old_labjournal.gui.tabs',
              'old_labjournal.gui.tabs.InfoEntry', 'old_labjournal.gui.tabs.InfoEntry.LAMMPS',
              'old_labjournal.gui.tabs.InfoEntry.GROMACS', 'old_labjournal.gui.popups', 'old_labjournal.gui.popups.DialogSettings',
              'old_labjournal.gui.QtExtensions', 'old_labjournal.core', 'old_labjournal.utils', 'old_labjournal.analysis',
              'old_labjournal.analysis.LAMMPS', 'old_labjournal.templates', 'old_labjournal.templates.LAMMPS',
              'old_labjournal.workflows', 'old_labjournal.workflows.tasks', 'old_labjournal.workflows.tasks.VMD',
              'old_labjournal.workflows.tasks.LAMMPS', 'old_labjournal.external_libs', 'old_labjournal.external_libs.pizza',
              'old_labjournal.user_specific', 'old_labjournal.user_specific.micha', 'old_labjournal.user_specific.micha.mediawiki'],
    # url='',
    # license='',
    author='Michael King, Andrej Berg',  # FixMe: geht hier ne liste?
    author_email='michael.king@uni-konstanz.de, andrej.berg@uni-konstanz.de',  # FixMe: geht hier ne liste?
    description='LabJournal',  # FixMe: Bessere Beschreibung
    install_requires=[
        'numpy',
        'matplotlib',
        'sqlalchemy',
        'qdarkstyle',
        'PyOpenGL',
      ]
)
