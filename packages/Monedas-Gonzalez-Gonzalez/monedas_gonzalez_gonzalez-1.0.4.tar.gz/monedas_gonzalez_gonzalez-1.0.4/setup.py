from setuptools import setup, find_packages

setup(
    name='Monedas_Gonzalez_Gonzalez',
    version='1.0.4',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'krakenex',
        'pandas',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'analizador-bandas-bollinger=src.main:main',
        ],
    },
    test_suite='tests',
    author='Luis González',
    author_email='lgg2002419@gmail.com',
    description='Soporte para análisis de bandas de Bollinger en criptomonedas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LuisGonzalez2002/ProyectoGonzalez_Gonzalez',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.12',
)
