import pytest
import os
import shutil
import tempfile
import uuid


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
