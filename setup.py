from distutils.core import setup

setup(
        name='rocketleaguereplayanalysis',
        version='1.1.2',
        url='https://enzanki-ars.github.io/rocket-league-replay-analysis',
        license='GNU AGPLv3',
        author='Alex Shafer',
        author_email='enzanki.ars@gmail.com',
        description='Parses Rocket League replay json files and '
                    'creates a minimap video',
        requires=['cairosvg',
                  'tqdm',
                  'ruamel.yaml']
)
