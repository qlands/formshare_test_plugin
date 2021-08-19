import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    README = f.read()
with open(os.path.join(here, "CHANGES.txt")) as f:
    CHANGES = f.read()

requires = ["formshare"]

tests_require = ["WebTest >= 1.3.1", "pytest", "pytest-cov"]  # py3 compat

setup(
    name="formshare_test_plugin",
    version="1.0",
    description="Testing plugin",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="QLands Technology Consultants",
    author_email="cquiros@qlands.com",
    url="https://formshare.org",
    keywords="formshare plugin",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={"testing": tests_require},
    install_requires=requires,
    entry_points={
        "formshare.plugins": [
            "formshare_test_plugin = formshare_test_plugin.plugin:FormShareTestPlugin",
            "formshare_test_api_plugin = formshare_test_plugin.plugin:FormShareTestAPIPlugin",
            "formshare_assistant_plugin = formshare_test_plugin.plugin:FormShareTestAssistantPlugin",
            "formshare_group_plugin = formshare_test_plugin.plugin:FormShareTestAssistantGroupPlugin",
            "formshare_user_plugin = formshare_test_plugin.plugin:FormShareTestUserPlugin",
            "formshare_observer_plugin = formshare_test_plugin.plugin:FormShareTestObserverPlugin",
            "formshare_partner_plugin =  formshare_test_plugin.plugin:FormShareTestPartnerPlugin",
        ],
        "formshare.tasks": [
            "formshare_test_plugin = formshare_test_plugin.celerytasks"
        ],
    },
)
