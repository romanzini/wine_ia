"""
Rotina para processar imagens de uma pasta, converter para Base64,
chamar a API da Perplexity e salvar o resultado em um arquivo Markdown.
"""

import base64
import requests
from pathlib import Path

def convert_image_to_base64(image_path: Path) -> str:
    """
    Converte uma imagem para uma string Base64.
    
    Args:
        image_path (Path): Caminho da imagem.
    
    Returns:
        str: String codificada em Base64.
    """

    try:
        with image_path.open("rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")
        image_data_uri = f"data:image/png;base64,{base64_image}" # Ensure correct MIME type
    except FileNotFoundError:
        print("Error: Image file not found.")
        exit()
    return image_data_uri

def call_perplexity_api(image_base64: str) -> str:
    """
    Chama a API da Perplexity para processar a imagem em Base64 e retorna o texto em Markdown.
    
    Args:
        image_base64 (str): String da imagem codificada em Base64.
    
    Returns:
        str: Texto retornado pela API em formato Markdown.
    """
    api_url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "accept": "application/json",
        "content-type": "application/json"
    }

    payload = {
        "model": "sonar",
        "temperature": 0.0,
        "messages": [
            {
                "role": "system",
                "content": "Você é um assistente especializado em transcrição de texto de imagens."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Esta imagem pode conter texto que precisa ser trasncrito. "
                    "Por favor:"
                    "1. Execute o OCR na imagem cuidadosamente em todos os elementos visíveis;"
                    "2. Certifique-se de que nenhum texto seja omitido ou mal interpretado;"
                    "3. Verifique novamente o texto extraído para garantir precisão."
                    "4. Retorne o texto extraído em formato Markdown."},
                    {"type": "image_url", "image_url": {"url": image_base64}}
                ]
            }
        ],
        "stream": False
    }

    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")


def process_images(input_dir: Path, output_file: Path):
    """
    Processa todas as imagens de um diretório, chama a API da Perplexity e salva os resultados em um arquivo Markdown.
    
    Args:
        input_dir (Path): Diretório contendo as imagens.
        output_file (Path): Caminho do arquivo onde os resultados serão salvos.
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"Diretório de entrada não encontrado: {input_dir}")
    
    image_exts = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
    image_files = sorted([p for p in input_dir.iterdir() if p.suffix.lower() in image_exts])

    if not image_files:
        print(f"Nenhuma imagem encontrada no diretório: {input_dir}")
        return

    with output_file.open("w", encoding="utf-8") as f:
        for img_path in image_files:
            try:
                print(f"[INFO] Processando imagem: {img_path.name}")
                image_base64 = convert_image_to_base64(img_path)
                markdown_text = call_perplexity_api(image_base64)
                f.write(f"# {markdown_text['choices'][0]['message']['content']}\n\n")
                print(f"[OK] Texto extraído para: {img_path.name}")
            except Exception as e:
                print(f"[ERRO] Falha ao processar {img_path.name}: {e}")

    print(f"[FINALIZADO] Resultados salvos em: {output_file}")


def main():
    # Diretório de entrada
    project_root = Path(__file__).resolve().parents[2]
    input_dir = project_root / "data" / "raw_img" / "revista_nov_21" / "01_winepedia"
    
    # Arquivo de saída
    output_file = project_root / "data" / "processed" / "revista_nov_21_winepedia.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Processar imagens e salvar resultados
    process_images(input_dir, output_file)


if __name__ == "__main__":
    main()