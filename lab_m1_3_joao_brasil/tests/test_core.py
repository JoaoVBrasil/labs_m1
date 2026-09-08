import numpy as np
import pytest
from pdi_lab.core import convolution, mean_kernel, weighted_mean_kernel, laplacian_kernel, sobel, validate_kernel


def test_identity_copy_reproduces_image():
    img = np.arange(25, dtype=np.uint8).reshape(5, 5)
    out = convolution(img, np.array([[0,0,0],[0,1,0],[0,0,0]], dtype=float), "copy")
    np.testing.assert_array_equal(out, img)


def test_identity_replicate_reproduces_image():
    img = np.arange(25, dtype=np.uint8).reshape(5, 5)
    out = convolution(img, np.array([[0,0,0],[0,1,0],[0,0,0]], dtype=float), "replicate")
    np.testing.assert_array_equal(out, img)


def test_constant_mean_is_constant():
    img = np.full((7, 7), 100, dtype=np.uint8)
    out = convolution(img, mean_kernel(3), "replicate")
    np.testing.assert_allclose(out, 100)


def test_weighted_mean_kernel_sums_one():
    assert np.isclose(weighted_mean_kernel().sum(), 1.0)


def test_invalid_even_kernel():
    with pytest.raises(ValueError):
        validate_kernel(np.ones((4, 4)))


def test_invalid_non_square_kernel():
    with pytest.raises(ValueError):
        validate_kernel(np.ones((3, 5)))


def test_invalid_border():
    with pytest.raises(ValueError):
        convolution(np.zeros((3, 3), dtype=np.uint8), np.array([[0,0,0],[0,1,0],[0,0,0]], dtype=float), "zero")


def test_laplacian_can_be_negative():
    img = np.zeros((3, 3), dtype=np.uint8)
    img[1, 1] = 255
    out = convolution(img, laplacian_kernel(), "replicate")
    assert out[1, 1] < 0


def test_sobel_shapes():
    img = np.zeros((8, 9), dtype=np.uint8)
    gx, gy, approx, euclidean = sobel(img, "replicate")
    assert gx.shape == gy.shape == approx.shape == euclidean.shape == img.shape
