from setuptools import setup, find_packages

def main():
  """Main function to set up the project."""
  setup(
    name='askpdf',
    version='0.0.2',
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your project',
    packages=find_packages(),
    install_requires=[
      'python-dotenv',
      'tqdm',
      'openai>=1.43.0',
      'numpy>=1.24.4',
      'PyPDF2',
      'pymupdf',
      'pyyaml',
      'click',
    ],
    package_data={
      '': ['src/data/*.json'],  ## Including all JSON files in the src/data/ directory
    },
    include_package_data=True,
    classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
      'console_scripts':[
        'genai=src.__main__:cmd'
      ]
    },
  )

if __name__ == "__main__":
  main()
