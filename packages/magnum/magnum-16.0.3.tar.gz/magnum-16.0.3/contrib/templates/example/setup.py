#!/usr/bin/env python
# Copyright (c) 2015 Rackspace Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

setuptools.setup(
    name="ExampleTemplate",
    version="0.1",
    packages=['example_template'],
    install_requires=['magnum'],
    package_data={
        'example_template': ['example.yaml']
    },
    author="Me",
    author_email="me@example.com",
    description="This is an Example Template",
    license="Apache",
    keywords="magnum template example",
    entry_points={
        'magnum.template_definitions': [
            'example_template = example_template:ExampleTemplate'
        ]
    }
)
