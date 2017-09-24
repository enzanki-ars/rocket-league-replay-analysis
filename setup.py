from distutils.core import setup

setup(
        name='rocketleagueminimapgenerator',
        version='1.0.0',
        url='https://enzanki-ars.github.io/rocket-league-minimap-generator',
        license='GNU AGPLv3',
        author='Alex Shafer',
        author_email='enzanki.ars@gmail.com',
        description='Parses Rocket League replay json files and '
                    'creates a minimap video',
        requires=['cairosvg',
                  'tqdm']
)
