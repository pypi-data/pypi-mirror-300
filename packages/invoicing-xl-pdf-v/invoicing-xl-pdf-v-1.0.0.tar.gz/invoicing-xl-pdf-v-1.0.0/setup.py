from setuptools import setup


setup(
  name='invoicing-xl-pdf-v',
  packages=['invoicing'],
  version='1.0.0',
  license='MIT',
  description='Convert Excel invoices to PDF invoices using this package.',
  author='Vedasree R',
  author_email='vedaraja17@gmail.com',
  url='https://example.com',
  keywords=['invoice', 'excel', 'pdf'],
  install_requires=['pandas', 'fpdf', 'openpyxl'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)
