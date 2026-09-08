from pathlib import Path
import sys

# Permite importar o pacote dentro de src/
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pdi_lab.core import (
    load_grayscale,
    save_image,
    convolution,
    mean_kernel,
    weighted_mean_kernel,
    laplacian_kernel,
    laplacian_enhance,
    sobel,
)


ROOT = Path(__file__).parent
INPUT = ROOT / "images" / "input" / "test.png"
OUTPUT = ROOT / "images" / "output"

OUTPUT.mkdir(parents=True, exist_ok=True)

print("======================================")
print("       TESTES COMPLETOS - M1.3")
print("======================================")

image = load_grayscale(str(INPUT))

# 1. Identidade
print("\n[1/10] Convolução - identidade...")
identity = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
]
result = convolution(image, identity, border="copy")
save_image(result, str(OUTPUT / "teste_identidade.png"))

# 2. Média 3x3
print("[2/10] Média 3x3...")
result = convolution(image, mean_kernel(3), border="replicate")
save_image(result, str(OUTPUT / "teste_media3.png"))

# 3. Média ponderada 3x3
print("[3/10] Média ponderada 3x3...")
result = convolution(image, weighted_mean_kernel(), border="replicate")
save_image(result, str(OUTPUT / "teste_ponderada.png"))

# 4. Média 5x5
print("[4/10] Média 5x5...")
result = convolution(image, mean_kernel(5), border="replicate")
save_image(result, str(OUTPUT / "teste_media5.png"))

# 5. Laplaciano
print("[5/10] Laplaciano...")
laplacian = convolution(image, laplacian_kernel(), border="replicate")
save_image(laplacian, str(OUTPUT / "teste_laplaciano.png"))

# 6. Laplaciano + realce
print("[6/10] Laplaciano + realce...")
enhanced = laplacian_enhance(image, laplacian, amount=1.0)
save_image(enhanced, str(OUTPUT / "teste_realce.png"))

# 7, 8, 9 e 10. Sobel
print("[7/10] Sobel Gx...")
print("[8/10] Sobel Gy...")
print("[9/10] Sobel magnitude aproximada...")
print("[10/10] Sobel magnitude Euclidiana...")

gx, gy, magnitude_approx, magnitude_euclidean = sobel(
    image,
    border="replicate"
)

save_image(gx, str(OUTPUT / "teste_sobel_gx.png"))
save_image(gy, str(OUTPUT / "teste_sobel_gy.png"))
save_image(magnitude_approx, str(OUTPUT / "teste_sobel_aprox.png"))
save_image(magnitude_euclidean, str(OUTPUT / "teste_sobel_euclidiano.png"))

print("\n======================================")
print("       TODOS OS TESTES CONCLUÍDOS!")
print("======================================")
print(f"\nResultados salvos em:")
print(OUTPUT)