import subprocess
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def run_cli(input_path: Path, output_path: Path, operation: str, levels: int | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [
        "python",
        "-m",
        "pdi_lab",
        "--input",
        str(input_path),
        "--output",
        str(output_path),
        "--operation",
        operation,
    ]
    if levels is not None:
        cmd.extend(["--levels", str(levels)])
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)


def create_synthetic_color_image(path: Path) -> Path:
    image = np.array(
        [
            [[10, 20, 30], [40, 50, 60]],
            [[70, 80, 90], [100, 110, 120]],
        ],
        dtype=np.uint8,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)
    return path


def test_manual_copy_preserves_pixels_exactly():
    input_path = ROOT / "images" / "input" / "synthetic_copy.png"
    output_path = ROOT / "images" / "output" / "pytest_copy.png"
    create_synthetic_color_image(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    result = run_cli(input_path, output_path, "copy")

    assert result.returncode == 0, result.stderr
    output = cv2.imread(str(output_path), cv2.IMREAD_UNCHANGED)
    expected = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)
    assert output is not None
    assert np.array_equal(output, expected)


def test_channel_order_and_zero_fill():
    input_path = ROOT / "images" / "input" / "synthetic_channels.png"
    create_synthetic_color_image(input_path)

    b_out = ROOT / "images" / "output" / "pytest_channel_b.png"
    g_out = ROOT / "images" / "output" / "pytest_channel_g.png"
    r_out = ROOT / "images" / "output" / "pytest_channel_r.png"

    for task, output in [("channel_b", b_out), ("channel_g", g_out), ("channel_r", r_out)]:
        proc = run_cli(input_path, output, task)
        assert proc.returncode == 0, proc.stderr

    b_img = cv2.imread(str(b_out), cv2.IMREAD_UNCHANGED)
    g_img = cv2.imread(str(g_out), cv2.IMREAD_UNCHANGED)
    r_img = cv2.imread(str(r_out), cv2.IMREAD_UNCHANGED)

    expected = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)

    assert np.array_equal(b_img[:, :, 0], expected[:, :, 0])
    assert np.all(b_img[:, :, 1:] == 0)
    assert np.array_equal(g_img[:, :, 1], expected[:, :, 1])
    assert np.all(g_img[:, :, [0, 2]] == 0)
    assert np.array_equal(r_img[:, :, 2], expected[:, :, 2])
    assert np.all(r_img[:, :, :2] == 0)


def test_grayscale_formulas_are_correct():
    input_path = ROOT / "images" / "input" / "synthetic_gray.png"
    create_synthetic_color_image(input_path)

    avg_out = ROOT / "images" / "output" / "pytest_gray_average.png"
    weighted_out = ROOT / "images" / "output" / "pytest_gray_weighted.png"

    proc_avg = run_cli(input_path, avg_out, "grayscale_average")
    proc_w = run_cli(input_path, weighted_out, "grayscale_weighted")

    assert proc_avg.returncode == 0, proc_avg.stderr
    assert proc_w.returncode == 0, proc_w.stderr

    image = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)
    avg_img = cv2.imread(str(avg_out), cv2.IMREAD_UNCHANGED)
    weighted_img = cv2.imread(str(weighted_out), cv2.IMREAD_UNCHANGED)

    expected_avg = np.zeros((2, 2), dtype=np.uint8)
    expected_weighted = np.zeros((2, 2), dtype=np.uint8)

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            b, g, r = image[y, x]
            expected_avg[y, x] = int(round((int(b) + int(g) + int(r)) / 3.0))
            expected_weighted[y, x] = int(round(0.299 * int(r) + 0.587 * int(g) + 0.114 * int(b)))

    assert np.array_equal(avg_img, expected_avg)
    assert np.array_equal(weighted_img, expected_weighted)


def test_quantization_generates_levels_16_8_4_2_and_keeps_range():
    input_path = ROOT / "images" / "input" / "synthetic_quant.png"
    image = np.array(
        [
            [[0, 0, 0], [64, 64, 64], [128, 128, 128], [255, 255, 255]],
            [[32, 32, 32], [96, 96, 96], [160, 160, 160], [224, 224, 224]],
        ],
        dtype=np.uint8,
    )
    cv2.imwrite(str(input_path), image)

    for levels in (16, 8, 4, 2):
        output = ROOT / "images" / "output" / f"pytest_{levels}.png"
        proc = run_cli(input_path, output, "quantize", levels=levels)
        assert proc.returncode == 0, proc.stderr
        result = cv2.imread(str(output), cv2.IMREAD_UNCHANGED)
        assert result is not None
        assert result.min() >= 0 and result.max() <= 255
        unique_values = np.unique(result)
        assert len(unique_values) <= levels


def test_quantization_handles_boundary_values():
    input_path = ROOT / "images" / "input" / "synthetic_bounds.png"
    image = np.array(
        [[
            [0, 0, 0], [127, 127, 127], [128, 128, 128], [255, 255, 255],
        ]],
        dtype=np.uint8,
    )
    cv2.imwrite(str(input_path), image)

    output = ROOT / "images" / "output" / "pytest_bounds_2.png"
    proc = run_cli(input_path, output, "quantize", levels=2)
    assert proc.returncode == 0, proc.stderr

    result = cv2.imread(str(output), cv2.IMREAD_UNCHANGED)
    assert result is not None
    assert result.min() >= 0 and result.max() <= 255
    assert np.unique(result).tolist() in ([0, 255], [0, 127, 255], [0, 128, 255])


def test_all_operation_generates_expected_output_set():
    input_path = ROOT / "images" / "input" / "synthetic_all.png"
    create_synthetic_color_image(input_path)

    output_dir = ROOT / "images" / "output" / "all_expected"
    if output_dir.exists():
        for file in output_dir.iterdir():
            if file.is_file():
                file.unlink()

    proc = run_cli(input_path, output_dir, "all")
    assert proc.returncode == 0, proc.stderr

    expected = [
        "copy.png",
        "channel_b.png",
        "channel_g.png",
        "channel_r.png",
        "gray_average.png",
        "gray_weighted.png",
        "quant_16.png",
        "quant_8.png",
        "quant_4.png",
        "quant_2.png",
    ]

    for filename in expected:
        assert (output_dir / filename).exists(), f"Arquivo ausente: {filename}"
