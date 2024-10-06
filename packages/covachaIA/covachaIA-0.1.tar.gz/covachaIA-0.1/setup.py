from setuptools import setup, find_packages

setup(
    name='covachaIA',
    version='0.1',
    description='Libraria para implementacion de OpenIA dentro de baatdigital',
    author='Cesar Sulbaran',
    author_email='support@baatdigital.com',
    url='https://github.com:baatdigital/covachaIA.git',
    packages=find_packages(),
    install_requires=[
        'openai>=1.34.0',  # Añade la versión mínima requerida de openai
        'python-dotenv>=1.0.1',  # Añade dotenv para la gestión de variables de entorno
    ],
    tests_require=[
        'pytest>=7.4.2',  # Dependencia de pytest para pruebas
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='==3.11.4',  # Especifica que requiere Python 3.11.4
    license='MIT',
)
