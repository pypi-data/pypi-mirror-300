from setuptools import setup, find_packages

setup(
    name='dissentty_vk',
    version='0.3',
    author='dissentty',
    description='Удобная библиотека для создания VK ботов',
    packages=find_packages(),
    install_requires=[
        'vk-api',
    ],
    entry_points={
        'console_scripts': [
            'dissentty_vk=dissentty_vk.bot:main',
        ],
    },
)