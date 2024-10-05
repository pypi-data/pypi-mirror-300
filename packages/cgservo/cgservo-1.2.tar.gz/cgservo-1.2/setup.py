from setuptools import setup

setup(
    name='cgservo',
    version='1.2',
    description='Control servo or BLDC ESC via PCA9685 PWM driver',
    author='Indoor Corgi',
    author_email='indoorcorgi@gmail.com',
    url='https://github.com/IndoorCorgi/cgservo',
    license='Apache License 2.0',
    packages=['cgservo'],
    install_requires=['smbus2'],
    python_requires='>=3.9',
)
