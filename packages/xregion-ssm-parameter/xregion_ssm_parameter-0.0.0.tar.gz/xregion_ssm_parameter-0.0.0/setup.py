import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "xregion-ssm-parameter",
    "version": "0.0.0",
    "description": "xregion-ssm-parameter",
    "license": "Apache-2.0",
    "url": "https://github.com/cmorgia/xregion-ssm-parameter.git",
    "long_description_content_type": "text/markdown",
    "author": "Claudio Morgia<cmorgia@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cmorgia/xregion-ssm-parameter.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "xregion_ssm_parameter",
        "xregion_ssm_parameter._jsii"
    ],
    "package_data": {
        "xregion_ssm_parameter._jsii": [
            "xregion-ssm-parameter@0.0.0.jsii.tgz"
        ],
        "xregion_ssm_parameter": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.103.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<5.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
