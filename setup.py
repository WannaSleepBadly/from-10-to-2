from cx_Freeze import setup, Executable

executables = [Executable('TheGame.py',
                          targetName='TheGame.exe',
                          base='Win32GUI',
                          icon='profilepic.ico')]

includes = ['PyQt5', 'csv', 'sys', 'random', 'datetime']

zip_include_packages = ['PyQt5', 'PyQt5.QtWidgets', 'PyQt5.QtGui', 'PyQt5.QtCore', 'csv', 'sys', 'random', 'datetime']

include_files = ['gamerules.png',
                 'transrules.png',
                 'Главная_игра.ui',
                 'Главное_меню.ui',
                 'Конец.ui',
                 'Правила.ui',
                 'Правила_игры.ui',
                 'Правила_перевода.ui',
                 'Рекорды.csv',
                 'Таблица_рекордов.ui',
                 'Уровни_сложности.ui']

options = {
    'build_exe': {
        'include_msvcr': True,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
        'include_files': include_files,
    }
}

setup(name='TheGame',
      version='0.0.3',
      description='Боже уже час ночи, помоги сделать этот тупой .exe файл',
      executables=executables,
      options=options)