# SPDX-License-Identifier: MIT

import pathlib
import re
import sys
import textwrap

import packaging.specifiers
import packaging.version
import pytest


if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

import pyproject_metadata


DIR = pathlib.Path(__file__).parent.resolve()


@pytest.mark.parametrize(
    ('data', 'error'),
    [
        ('', 'Section "project" missing in pyproject.toml'),
        # name
        ('[project]', 'Field "project.name" missing'),
        (
            """
                [project]
                name = true
                version = '0.1.0'
            """,
            (
                'Field "project.name" has an invalid type, expecting a string (got "True")'
            ),
        ),
        # dynamic
        (
            """
                [project]
                name = true
                version = '0.1.0'
                dynamic = [
                    'name',
                ]
            """,
            ('Unsupported field "name" in "project.dynamic"'),
        ),
        # version
        (
            """
                [project]
                name = 'test'
                version = true
            """,
            (
                'Field "project.version" has an invalid type, expecting a string (got "True")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
            """,
            (
                'Field "project.version" missing and "version" not specified in "project.dynamic"'
            ),
        ),
        # license
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                license = true
            """,
            (
                'Field "project.license" has an invalid type, expecting a dictionary of strings (got "True")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                license = {}
            """,
            (
                'Invalid "project.license" value, expecting either "file" or "text" (got "{}")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                license = { file = '...', text = '...' }
            """,
            (
                'Invalid "project.license" value, expecting either "file" '
                "or \"text\" (got \"{'file': '...', 'text': '...'}\")"
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                license = { made-up = ':(' }
            """,
            ('Unexpected field "project.license.made-up"'),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                license = { file = true }
            """,
            (
                'Field "project.license.file" has an invalid type, expecting a string (got "True")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                license = { text = true }
            """,
            (
                'Field "project.license.text" has an invalid type, expecting a string (got "True")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                license = { file = 'this-file-does-not-exist' }
            """,
            ('License file not found ("this-file-does-not-exist")'),
        ),
        # readme
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                readme = true
            """,
            (
                'Field "project.readme" has an invalid type, expecting either, '
                'a string or dictionary of strings (got "True")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                readme = {}
            """,
            (
                'Invalid "project.readme" value, expecting either "file" or "text" (got "{}")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                readme = { file = '...', text = '...' }
            """,
            (
                'Invalid "project.readme" value, expecting either "file" or '
                "\"text\" (got \"{'file': '...', 'text': '...'}\")"
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                readme = { made-up = ':(' }
            """,
            ('Unexpected field "project.readme.made-up"'),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                readme = { file = true }
            """,
            (
                'Field "project.readme.file" has an invalid type, expecting a string (got "True")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                readme = { text = true }
            """,
            (
                'Field "project.readme.text" has an invalid type, expecting a string (got "True")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                readme = { file = 'this-file-does-not-exist', content-type = '...' }
            """,
            ('Readme file not found ("this-file-does-not-exist")'),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                readme = { file = 'README.md' }
            """,
            ('Field "project.readme.content-type" missing'),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                readme = { text = '...' }
            """,
            ('Field "project.readme.content-type" missing'),
        ),
        # description
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                description = true
            """,
            (
                'Field "project.description" has an invalid type, expecting a string (got "True")'
            ),
        ),
        # dependencies
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                dependencies = 'some string!'
            """,
            (
                'Field "project.dependencies" has an invalid type, expecting a list of strings (got "some string!")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                dependencies = [
                    99,
                ]
            """,
            (
                'Field "project.dependencies" contains item with invalid type, expecting a string (got "99")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                dependencies = [
                    'definitely not a valid PEP 508 requirement!',
                ]
            """,
            (
                'Field "project.dependencies" contains an invalid PEP 508 requirement '
                'string "definitely not a valid PEP 508 requirement!" '
            ),
        ),
        # optional-dependencies
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                optional-dependencies = true
            """,
            (
                'Field "project.optional-dependencies" has an invalid type, '
                'expecting a dictionary of PEP 508 requirement strings (got "True")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                [project.optional-dependencies]
                test = 'some string!'
            """,
            (
                'Field "project.optional-dependencies.test" has an invalid type, '
                'expecting a dictionary PEP 508 requirement strings (got "some string!")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                [project.optional-dependencies]
                test = [
                    true,
                ]
            """,
            (
                'Field "project.optional-dependencies.test" has an invalid type, '
                'expecting a PEP 508 requirement string (got "True")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                [project.optional-dependencies]
                test = [
                    'definitely not a valid PEP 508 requirement!',
                ]
            """,
            (
                'Field "project.optional-dependencies.test" contains an invalid '
                'PEP 508 requirement string "definitely not a valid PEP 508 requirement!" '
            ),
        ),
        # requires-python
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                requires-python = true
            """,
            (
                'Field "project.requires-python" has an invalid type, expecting a string (got "True")'
            ),
        ),
        # keywords
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                keywords = 'some string!'
            """,
            (
                'Field "project.keywords" has an invalid type, expecting a list of strings (got "some string!")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                keywords = [
                    true,
                ]
            """,
            (
                'Field "project.keywords" contains item with invalid type, expecting a string (got "True")'
            ),
        ),
        # authors
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                authors = {}
            """,
            (
                'Field "project.authors" has an invalid type, expecting a list of '
                'dictionaries containing the "name" and/or "email" keys (got "{}")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                authors = [
                    true,
                ]
            """,
            (
                'Field "project.authors" has an invalid type, expecting a list of '
                'dictionaries containing the "name" and/or "email" keys (got "[True]")'
            ),
        ),
        # maintainers
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                maintainers = {}
            """,
            (
                'Field "project.maintainers" has an invalid type, expecting a list of '
                'dictionaries containing the "name" and/or "email" keys (got "{}")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                maintainers = [
                    10
                ]
            """,
            (
                'Field "project.maintainers" has an invalid type, expecting a list of '
                'dictionaries containing the "name" and/or "email" keys (got "[10]")'
            ),
        ),
        # classifiers
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                classifiers = 'some string!'
            """,
            (
                'Field "project.classifiers" has an invalid type, expecting a list of strings (got "some string!")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                classifiers = [
                    true,
                ]
            """,
            (
                'Field "project.classifiers" contains item with invalid type, expecting a string (got "True")'
            ),
        ),
        # homepage
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                [project.urls]
                homepage = true
            """,
            (
                'Field "project.urls.homepage" has an invalid type, expecting a string (got "True")'
            ),
        ),
        # documentation
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                [project.urls]
                documentation = true
            """,
            (
                'Field "project.urls.documentation" has an invalid type, expecting a string (got "True")'
            ),
        ),
        # repository
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                [project.urls]
                repository = true
            """,
            (
                'Field "project.urls.repository" has an invalid type, expecting a string (got "True")'
            ),
        ),
        # changelog
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                [project.urls]
                changelog = true
            """,
            (
                'Field "project.urls.changelog" has an invalid type, expecting a string (got "True")'
            ),
        ),
        # scripts
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                scripts = []
            """,
            (
                'Field "project.scripts" has an invalid type, expecting a dictionary of strings (got "[]")'
            ),
        ),
        # gui-scripts
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                gui-scripts = []
            """,
            (
                'Field "project.gui-scripts" has an invalid type, expecting a dictionary of strings (got "[]")'
            ),
        ),
        # entry-points
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                entry-points = []
            """,
            (
                'Field "project.entry-points" has an invalid type, '
                'expecting a dictionary of entrypoint sections (got "[]")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                entry-points = { section = 'something' }
            """,
            (
                'Field "project.entry-points.section" has an invalid type, '
                'expecting a dictionary of entrypoints (got "something")'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                [project.entry-points.section]
                entrypoint = []
            """,
            (
                'Field "project.entry-points.section.entrypoint" has an invalid type, expecting a string (got "[]")'
            ),
        ),
        # invalid name
        (
            """
                [project]
                name = '.test'
                version = '0.1.0'
            """,
            (
                'Invalid project name ".test". A valid name consists only of ASCII letters and '
                'numbers, period, underscore and hyphen. It must start and end with a letter or number'
            ),
        ),
        (
            """
                [project]
                name = 'test'
                version = '0.1.0'
                [project.entry-points.bad-name]
            """,
            (
                'Field "project.entry-points" has an invalid value, expecting a name containing only '
                'alphanumeric, underscore, or dot characters (got "bad-name")'
            ),
        ),
    ],
)
def test_load(data: str, error: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(DIR / 'packages/full-metadata')
    with pytest.raises(pyproject_metadata.ConfigurationError, match=re.escape(error)):
        pyproject_metadata.StandardMetadata.from_pyproject(
            tomllib.loads(textwrap.dedent(data))
        )


@pytest.mark.parametrize('after_rfc', [False, True])
def test_value(after_rfc: bool, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(DIR / 'packages/full-metadata')
    with open('pyproject.toml', 'rb') as f:
        metadata = pyproject_metadata.StandardMetadata.from_pyproject(tomllib.load(f))

    if after_rfc:
        metadata.as_rfc822()

    assert metadata.dynamic == []
    assert metadata.name == 'full_metadata'
    assert metadata.canonical_name == 'full-metadata'
    assert metadata.version == packaging.version.Version('3.2.1')
    assert metadata.requires_python == packaging.specifiers.Specifier('>=3.8')
    assert isinstance(metadata.license, pyproject_metadata.License)
    assert metadata.license.file is None
    assert metadata.license.text == 'some license text'
    assert isinstance(metadata.readme, pyproject_metadata.Readme)
    assert metadata.readme.file == pathlib.Path('README.md')
    assert metadata.readme.text == pathlib.Path('README.md').read_text(encoding='utf-8')
    assert metadata.readme.content_type == 'text/markdown'
    assert metadata.description == 'A package with all the metadata :)'
    assert metadata.authors == [
        ('Unknown', 'example@example.com'),
        ('Example!', None),
    ]
    assert metadata.maintainers == [
        ('Other Example', 'other@example.com'),
    ]
    assert metadata.keywords == ['trampolim', 'is', 'interesting']
    assert metadata.classifiers == [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
    ]
    assert metadata.urls == {
        'changelog': 'github.com/some/repo/blob/master/CHANGELOG.rst',
        'documentation': 'readthedocs.org',
        'homepage': 'example.com',
        'repository': 'github.com/some/repo',
    }
    assert metadata.entrypoints == {
        'custom': {
            'full-metadata': 'full_metadata:main_custom',
        },
    }
    assert metadata.scripts == {
        'full-metadata': 'full_metadata:main_cli',
    }
    assert metadata.gui_scripts == {
        'full-metadata-gui': 'full_metadata:main_gui',
    }
    assert list(map(str, metadata.dependencies)) == [
        'dependency1',
        'dependency2>1.0.0',
        'dependency3[extra]',
        'dependency4; os_name != "nt"',
        'dependency5[other-extra]>1.0; os_name == "nt"',
    ]
    assert list(metadata.optional_dependencies.keys()) == ['test']
    assert list(map(str, metadata.optional_dependencies['test'])) == [
        'test_dependency',
        'test_dependency[test_extra]',
        'test_dependency[test_extra2]>3.0; os_name == "nt"',
    ]


def test_read_license(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(DIR / 'packages/full-metadata2')
    with open('pyproject.toml', 'rb') as f:
        metadata = pyproject_metadata.StandardMetadata.from_pyproject(tomllib.load(f))

    assert isinstance(metadata.license, pyproject_metadata.License)
    assert metadata.license.file == pathlib.Path('LICENSE')
    assert metadata.license.text == 'Some license! 👋\n'


@pytest.mark.parametrize(
    ('package', 'content_type'),
    [
        ('full-metadata', 'text/markdown'),
        ('full-metadata2', 'text/x-rst'),
    ],
)
def test_readme_content_type(
    package: str, content_type: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(DIR / 'packages' / package)
    with open('pyproject.toml', 'rb') as f:
        metadata = pyproject_metadata.StandardMetadata.from_pyproject(tomllib.load(f))

    assert isinstance(metadata.readme, pyproject_metadata.Readme)
    assert metadata.readme.content_type == content_type


def test_readme_content_type_unknown(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(DIR / 'packages/unknown-readme-type')
    with pytest.raises(
        pyproject_metadata.ConfigurationError,
        match=re.escape(
            'Could not infer content type for readme file "README.just-made-this-up-now"'
        ),
    ), open('pyproject.toml', 'rb') as f:
        pyproject_metadata.StandardMetadata.from_pyproject(tomllib.load(f))


def test_as_rfc822(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(DIR / 'packages/full-metadata')

    with open('pyproject.toml', 'rb') as f:
        metadata = pyproject_metadata.StandardMetadata.from_pyproject(tomllib.load(f))
    core_metadata = metadata.as_rfc822()
    assert core_metadata.headers == {
        'Metadata-Version': ['2.1'],
        'Name': ['full_metadata'],
        'Summary': ['A package with all the metadata :)'],
        'Version': ['3.2.1'],
        'Keywords': ['trampolim,is,interesting'],
        'Home-page': ['example.com'],
        'Author': ['Example!'],
        'Author-Email': ['Unknown <example@example.com>'],
        'Maintainer-Email': ['Other Example <other@example.com>'],
        'License': ['some license text'],
        'Classifier': [
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
        ],
        'Project-URL': [
            'Homepage, example.com',
            'Documentation, readthedocs.org',
            'Repository, github.com/some/repo',
            'Changelog, github.com/some/repo/blob/master/CHANGELOG.rst',
        ],
        'Requires-Python': ['>=3.8'],
        'Provides-Extra': ['test'],
        'Requires-Dist': [
            'dependency1',
            'dependency2>1.0.0',
            'dependency3[extra]',
            'dependency4; os_name != "nt"',
            'dependency5[other-extra]>1.0; os_name == "nt"',
            'test_dependency; extra == "test"',
            'test_dependency[test_extra]; extra == "test"',
            'test_dependency[test_extra2]>3.0; os_name == "nt" and ' 'extra == "test"',
        ],
        'Description-Content-Type': ['text/markdown'],
    }
    assert core_metadata.body == 'some readme 👋\n'


def test_as_rfc822_dynamic(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(DIR / 'packages/dynamic-description')

    with open('pyproject.toml', 'rb') as f:
        metadata = pyproject_metadata.StandardMetadata.from_pyproject(tomllib.load(f))
    core_metadata = metadata.as_rfc822()
    assert dict(core_metadata.headers) == {
        'Metadata-Version': ['2.2'],
        'Name': ['dynamic-description'],
        'Version': ['1.0.0'],
        'Dynamic': ['description'],
    }


@pytest.mark.parametrize('metadata_version', ['2.1', '2.2', '2.3'])
def test_as_rfc822_set_metadata(metadata_version: str) -> None:
    metadata = pyproject_metadata.StandardMetadata.from_pyproject(
        {
            'project': {
                'name': 'hi',
                'version': '1.2',
                'optional-dependencies': {
                    'under_score': ['some_package'],
                    'da-sh': ['some-package'],
                    'do.t': ['some.package'],
                    'empty': [],
                },
            }
        },
        metadata_version=metadata_version,
    )
    assert metadata.metadata_version == metadata_version

    rfc822 = str(metadata.as_rfc822())

    assert f'Metadata-Version: {metadata_version}' in rfc822

    assert 'Provides-Extra: under-score' in rfc822
    assert 'Provides-Extra: da-sh' in rfc822
    assert 'Provides-Extra: do-t' in rfc822
    assert 'Provides-Extra: empty' in rfc822
    assert 'Requires-Dist: some_package; extra == "under-score"' in rfc822
    assert 'Requires-Dist: some-package; extra == "da-sh"' in rfc822
    assert 'Requires-Dist: some.package; extra == "do-t"' in rfc822


def test_as_rfc822_set_metadata_invalid() -> None:
    with pytest.raises(
        pyproject_metadata.ConfigurationError,
        match='The metadata_version must be one of',
    ) as err:
        pyproject_metadata.StandardMetadata.from_pyproject(
            {
                'project': {
                    'name': 'hi',
                    'version': '1.2',
                },
            },
            metadata_version='2.0',
        )
    assert '2.1' in str(err.value)
    assert '2.2' in str(err.value)
    assert '2.3' in str(err.value)


def test_as_rfc822_invalid_dynamic() -> None:
    metadata = pyproject_metadata.StandardMetadata(
        name='something',
        version=packaging.version.Version('1.0.0'),
    )
    metadata.dynamic = ['name']
    with pytest.raises(
        pyproject_metadata.ConfigurationError, match='Field cannot be dynamic: name'
    ):
        metadata.as_rfc822()
    metadata.dynamic = ['version']
    with pytest.raises(
        pyproject_metadata.ConfigurationError, match='Field cannot be dynamic: version'
    ):
        metadata.as_rfc822()


def test_as_rfc822_missing_version() -> None:
    metadata = pyproject_metadata.StandardMetadata(name='something')
    with pytest.raises(
        pyproject_metadata.ConfigurationError, match='Missing version field'
    ):
        metadata.as_rfc822()


def test_stically_defined_dynamic_field() -> None:
    with pytest.raises(
        pyproject_metadata.ConfigurationError,
        match='Field "project.version" declared as dynamic in "project.dynamic" but is defined',
    ):
        pyproject_metadata.StandardMetadata.from_pyproject(
            {
                'project': {
                    'name': 'example',
                    'version': '1.2.3',
                    'dynamic': [
                        'version',
                    ],
                },
            }
        )


@pytest.mark.parametrize(
    'value',
    [
        '<3.10',
        '>3.7,<3.11',
        '>3.7,<3.11,!=3.8.4',
        '~=3.10,!=3.10.3',
    ],
)
def test_requires_python(value: str) -> None:
    pyproject_metadata.StandardMetadata.from_pyproject(
        {
            'project': {
                'name': 'example',
                'version': '0.1.0',
                'requires-python': value,
            },
        }
    )


def test_version_dynamic() -> None:
    metadata = pyproject_metadata.StandardMetadata.from_pyproject(
        {
            'project': {
                'name': 'example',
                'dynamic': [
                    'version',
                ],
            },
        }
    )
    metadata.version = packaging.version.Version('1.2.3')
    assert 'version' not in metadata.dynamic
