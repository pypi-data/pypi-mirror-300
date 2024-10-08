from setuptools import setup, find_packages

setup(
    name='PanchIDE',  # Nombre del paquete
    version='0.1.0',  # Versión del paquete
    py_modules=["IDE2"],  # Encuentra los paquetes automáticamente
    install_requires=[
        # Lista de dependencias
        # 'numpy',  # Ejemplo de dependencia
        'pyperclip'
    ],
    author='Pancho MN',
    author_email='programarcomands@gmail.com',
    description='Por si necesitas un IDE sin necesidad de permisos',
    #long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url='https://github.com/tu_usuario/mi_paquete',  # URL del repositorio
)
