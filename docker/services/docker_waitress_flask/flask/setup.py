from setuptools import setup

setup(
    name="thesr_flask_app",
    packages=["thesr_flask_app"],
    package_data={"thesr_flask_app": ["static/*", "templates/*"]},
    # https://stackoverflow.com/questions/56208727/setuptools-not-including-flask-templates-when-creating-distribution
    # https://stackoverflow.com/questions/7522250/how-to-include-package-data-with-setuptools-distutils
    include_package_data=True,
    install_requires=["flask", "thesr"],
)
