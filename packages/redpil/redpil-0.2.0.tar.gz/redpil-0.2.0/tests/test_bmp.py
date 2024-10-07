from redpil.bmp import imwrite, imread

import numpy as np
import pytest
from PIL import Image
from numpy.testing import assert_array_equal

# Pathlib doesn't work well in python 3.5
# from pathlib import Path
import os

def test_failers(tmpdir):
    tmpfile = os.path.join(str(tmpdir), 'test.bmp')
    img = np.zeros((4, 4), dtype=np.float32)
    with pytest.raises(NotImplementedError):
        imwrite(tmpfile, img)


@pytest.mark.parametrize('shape', [(4, 4), (7, 7), (21, 7)])
@pytest.mark.parametrize('backend', ['pillow', 'redpil'])
def test_uint8_image(tmpdir, shape, backend):
    tmpfile = os.path.join(str(tmpdir), 'test.bmp')

    img = np.random.randint(255, size=shape, dtype=np.uint8)
    imwrite(tmpfile, img)

    if backend == 'pillow':
        img_read = np.asarray(Image.open(tmpfile).convert('L'))
    else:
        img_read = imread(tmpfile)

    assert img.dtype == img_read.dtype
    assert_array_equal(img, img_read)


@pytest.mark.parametrize('shape', [(4, 4, 3), (7, 7, 3), (21, 7, 3)])
@pytest.mark.parametrize('backend', ['pillow', 'redpil'])
def test_uint8_rgb_image(tmpdir, shape, backend):
    tmpfile = os.path.join(str(tmpdir), 'test.bmp')

    img = np.random.randint(255, size=shape, dtype=np.uint8)
    imwrite(tmpfile, img)

    if backend == 'pillow':
        img_read = np.asarray(Image.open(tmpfile).convert('RGB'))
    else:
        img_read = imread(tmpfile)

    assert img.dtype == img_read.dtype
    assert_array_equal(img, img_read)


@pytest.mark.parametrize('shape', [(4, 4, 4), (7, 7, 4), (21, 7, 4)])
@pytest.mark.parametrize('backend', ['pillow', 'redpil'])
def test_uint8_rgba_image(tmpdir, shape, backend):
    tmpfile = os.path.join(str(tmpdir), 'test.bmp')

    img = np.random.randint(255, size=shape, dtype=np.uint8)

    if backend == 'pillow':
        imwrite(tmpfile, img)
        img_read = np.asarray(Image.open(tmpfile).convert('RGBA'))
        assert img.dtype == img_read.dtype
        assert_array_equal(img, img_read)
    else:
        for write_order in ['RGBA', 'BGRA']:
            imwrite(tmpfile, img, write_order=write_order)
            img_read = imread(tmpfile)
            assert img.dtype == img_read.dtype
            assert_array_equal(img, img_read)


@pytest.mark.parametrize('shape', [(4, 4), (7, 7), (21, 7),
                                   (121, 121), (128, 128)])
@pytest.mark.parametrize('backend', ['pillow', 'redpil'])
def test_bool_image(tmpdir, shape, backend):
    tmpfile = os.path.join(str(tmpdir), 'test.bmp')

    img = np.random.randint(2, size=shape, dtype=np.bool_)
    img[0, 0] = False
    img[-1, -1] = True
    print(img)
    imwrite(tmpfile, img)

    if backend == 'pillow':
        img_read = np.asarray(Image.open(tmpfile).convert('L'))
    else:
        img_read = imread(tmpfile)
    print(img_read)
    assert img_read[0, 0] == 0
    assert img_read[-1, -1] == 255

    color_pallet = np.asarray([0, 255], dtype=np.uint8)
    assert_array_equal(color_pallet[img.astype(np.uint8)], img_read)
