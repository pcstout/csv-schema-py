import pytest
import os
import shutil
import tempfile
import uuid
from src.csv_schema.core.models import SchemaConfig, StringColumn


@pytest.fixture
def config_path(mk_tempfile):
    return mk_tempfile(suffix='.json')


@pytest.fixture
def mk_valid_csv(mk_tempdir):
    def _mk(filename='test.csv'):
        tmpdir = mk_tempdir()
        path = os.path.join(tmpdir, filename)

        lines = ['col1,col2,col3']
        lines.append('a1,b1,c1')
        lines.append('a2,b2,c2')
        lines.append('a3,b3,c3')

        with open(path, mode='w') as f:
            f.writelines(lines)

        return path

    yield _mk


@pytest.fixture
def valid_csv_path(mk_valid_csv):
    return mk_valid_csv()


@pytest.fixture
def invalid_csv_path(mk_tempfile):
    path = mk_tempfile(suffix='.csv')

    lines = ['col1,col2,colX']
    lines.append('a1,b1,c1')
    lines.append('a2,b2,c2')
    lines.append('a3,b3,')

    with open(path, mode='w') as f:
        f.writelines(lines)

    return path


@pytest.fixture
def valid_config_path(populated_config):
    assert populated_config.is_valid() is True
    populated_config.save()
    return populated_config.path


@pytest.fixture
def invalid_config_path(populated_config):
    populated_config.properties[0].value = None
    assert populated_config.is_valid() is False
    populated_config.save()
    return populated_config.path


@pytest.fixture
def empty_config(config_path):
    return SchemaConfig(config_path)


@pytest.fixture
def populated_config(config_path):
    columns = [
        StringColumn('col1'),
        StringColumn('col2'),
        StringColumn('col3')
    ]
    config = SchemaConfig(config_path,
                          name='Populated Config',
                          description='A Description',
                          columns=columns)
    config.save()
    return config


@pytest.fixture()
def mk_tempdir():
    created = []

    def _mk():
        path = tempfile.mkdtemp()
        created.append(path)
        return path

    yield _mk

    for path in created:
        if os.path.isdir(path):
            shutil.rmtree(path)


@pytest.fixture()
def mk_tempfile(mk_tempdir):
    temp_dir = mk_tempdir()

    def _mk(content=uuid.uuid4().hex, suffix=None):
        fd, tmp_filename = tempfile.mkstemp(dir=temp_dir, suffix=suffix)
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(content)
        return tmp_filename

    yield _mk

    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
