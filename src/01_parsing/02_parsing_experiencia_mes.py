"""
Rotina para processar imagens de uma pasta, converter para Base64,
chamar a API da Perplexity e salvar o resultado em um arquivo Markdown.
"""

import os
import base64
import mimetypes
import json
import re
import requests
from pathlib import Path
from dotenv import load_dotenv
import sys

here = Path(__file__).resolve()
src_dir = here.parent.parent
project_root = src_dir.parent

# Torna 'src' importável (para importar prompts)
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

from prompts.prompt_factory import PromptFactory

dotenv_path = project_root / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    print(f"⚠️ Warning: .env not found at {dotenv_path}")


def convert_image_to_base64(image_path: Path) -> str:
    """
    Converte uma imagem para uma string Base64.

    Args:
        image_path (Path): Caminho da imagem.

    Returns:
        str: String codificada em Base64 como Data URI.
    """
    try:
        with image_path.open("rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")
        mime, _ = mimetypes.guess_type(image_path.name)
        mime = mime or "application/octet-stream"
        image_data_uri = f"data:{mime};base64,{base64_image}"
    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
        raise
    return image_data_uri

def call_perplexity_api(image_base64: str) -> dict:
    """
    Chama a API da Perplexity para processar a imagem em Base64 e retorna o texto.

    Chama a LLM com um prompt restrito para extrair apenas:
    - nome_vinho
    - tipo
    - etc...
    Retorna um dicionário com essas chaves (ou None).

    Args:
        image_base64 (str): String da imagem codificada em Base64.

    Returns:
        dict: JSON retornado pela API.
    """
    api_key = os.getenv("PPLX_API_KEY")
    if not api_key:
        raise EnvironmentError("Defina a variável de ambiente PPLX_API_KEY com sua chave da Perplexity.")

    api_url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
        "content-type": "application/json",
    }

    payload = {
        "model": "sonar",
        "temperature": 0.0,
        "messages": PromptFactory.experiencia_mes_messages(image_base64),
        "stream": False,
    }

    response = requests.post(api_url, json=payload, headers=headers, timeout=60)
    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")

    resp_json = response.json()
    content = resp_json["choices"][0]["message"]["content"]

    # Tenta fazer parse seguro do JSON retornado
    def _parse_to_dict(text: str) -> dict:
        try:
            return json.loads(text)
        except Exception:
            match = re.search(r"\{.*\}", text, flags=re.S)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception:
                    pass
        return {"nome_vinho": None, "tipo": None}

    data = _parse_to_dict(content)
    # Garante apenas as chaves esperadas
    return {
        "nome_vinho": data.get("nome_vinho"),
        "tipo": data.get("tipo"),
        "regiao": data.get("regiao"),
        "vinicula": data.get("vinicula"),
        "uva": data.get("uva"),
        "amadurecimento": data.get("amadurecimento"),
        "potencial_guarda": data.get("potencial_guarda"),
        "visual": data.get("visual"),
        "olfativo": data.get("olfativo"),
        "gustativo": data.get("gustativo"),
        "temperatura_servico": data.get("temperatura_servico"),
        "harmonizacao": data.get("harmonizacao"),
    }

def process_images(input_dir: Path, output_file: Path, recursive: bool = False):
    """
    Processa todas as imagens de um diretório, chama a API da Perplexity e salva os resultados em um arquivo Markdown.

    Args:
        input_dir (Path): Diretório contendo as imagens.
        output_file (Path): Caminho do arquivo onde os resultados serão salvos.
        recursive (bool): Se True, busca imagens recursivamente em subpastas.
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"Diretório de entrada não encontrado: {input_dir}")

    image_exts = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
    if recursive:
        image_files = sorted(
            [p for p in input_dir.rglob("*") if p.is_file() and p.suffix.lower() in image_exts]
        )
    else:
        image_files = sorted([p for p in input_dir.iterdir() if p.suffix.lower() in image_exts])

    if not image_files:
        print(f"Nenhuma imagem encontrada no diretório: {input_dir}")
        return

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        f.write(f"# Arquivo - {output_file}\n\n")
        for img_path in image_files:
            try:
                print(f"[INFO] Processando imagem: {img_path}")
                image_base64 = convert_image_to_base64(img_path)
                dados = call_perplexity_api(image_base64)
                #f.write(f"## {img_path.name}\n")
                f.write(f"- Nome do vinho: {dados.get('nome_vinho')}\n")
                f.write(f"- Tipo: {dados.get('tipo')}\n")
                f.write(f"- Região: {dados.get('regiao')}\n")
                f.write(f"- Vinícula: {dados.get('vinicula')}\n")
                f.write(f"- Uva: {dados.get('uva')}\n")
                f.write(f"- Amadurecimento: {dados.get('amadurecimento')}\n")
                f.write(f"- Potencial de Guarda: {dados.get('potencial_guarda')}\n")
                f.write(f"- Visual: {dados.get('visual')}\n")
                f.write(f"- Olfativo: {dados.get('olfativo')}\n")
                f.write(f"- Gustativo: {dados.get('gustativo')}\n")
                f.write(f"- Temperatura de Serviço: {dados.get('temperatura_servico')}\n")
                f.write(f"- Harmonização: {dados.get('harmonizacao')}\n\n")
                print(f"[OK] Texto extraído para: {img_path.name}")
            except Exception as e:
                print(f"[ERRO] Falha ao processar {img_path.name}: {e}")

    print(f"[FINALIZADO] Resultados salvos em: {output_file}")

def process_second_level_dirs(root_input_dir: Path, output_root_dir: Path):
    """
    Para cada subpasta imediata de root_input_dir (nível 1), percorre as subpastas de nível 2
    (ex.: 02_experiencia_mes) e agrega TODAS as imagens existentes abaixo delas (níveis inferiores)
    em um único arquivo .md nomeado com o nome da subpasta de nível 2.

    Exemplo:
      data/raw_img/revista_ago_24/02_experiencia_mes/** -> data/processed/revista_ago_24/02_experiencia_mes.md
    """
    if not root_input_dir.exists():
        raise FileNotFoundError(f"Pasta raiz não encontrada: {root_input_dir}")

    level1_dirs = sorted([p for p in root_input_dir.iterdir() if p.is_dir()])
    if not level1_dirs:
        print(f"Nenhuma subpasta encontrada em: {root_input_dir}")
        return

    for lvl1 in level1_dirs:
        # Filtra somente a subpasta de nível 2 chamada "02_experiencia_mes"
        level2_dirs = sorted([p for p in lvl1.iterdir() if p.is_dir() and p.name == "02_experiencia_mes"])
        if not level2_dirs:
            print(f"[AVISO] '{lvl1.name}' não contém a subpasta '02_experiencia_mes'.")
            continue

        for lvl2 in level2_dirs:
            output_dir = output_root_dir / lvl1.name
            output_file = output_dir / f"{lvl2.name}.md"
            print(f"\n[PASTA] {lvl1.name}/{lvl2.name} -> {output_file}")
            # Busca recursivamente abaixo de lvl2
            process_images(lvl2, output_file, recursive=True)

def process_all_subdirs(root_input_dir: Path, output_root_dir: Path):
    """
    Itera por todas as subpastas imediatas de root_input_dir e gera um .md
    com o nome de cada subpasta dentro de output_root_dir.

    Args:
        root_input_dir (Path): Pasta raíz contendo subpastas com imagens.
        output_root_dir (Path): Pasta onde os arquivos .md serão salvos.
    """
    if not root_input_dir.exists():
        raise FileNotFoundError(f"Pasta raiz não encontrada: {root_input_dir}")

    subdirs = sorted([p for p in root_input_dir.iterdir() if p.is_dir()])
    if not subdirs:
        print(f"Nenhuma subpasta encontrada em: {root_input_dir}")
        return

    for subdir in subdirs:
        output_file = output_root_dir / f"{subdir.name}.md"
        print(f"\n[PASTA] {subdir} -> {output_file.name}")
        process_images(subdir, output_file)

def main():
    # Diretórios de entrada e saída
    project_root = Path(__file__).resolve().parents[2]
    input_root_dir = project_root / "data" / "raw_img"
    output_root_dir = project_root / "data" / "processed"

    # Percorrer: raw_img/<nivel1>/<nivel2>/** e gerar um .md por <nivel2>
    process_second_level_dirs(input_root_dir, output_root_dir)

if __name__ == "__main__":
    main()