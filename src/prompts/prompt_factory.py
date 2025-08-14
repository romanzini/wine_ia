from typing import List, Dict, Any

class PromptFactory:
    @staticmethod
    def winepedia_ocr_messages(image_base64: str) -> List[Dict[str, Any]]:
        """
        OCR para páginas da revista (ex.: winepedia). Retorna Markdown fiel ao texto.
        """
        return [
            {
                "role": "system",
                "content": (
                    "Você é um assistente especializado em transcrição de texto de imagens. "
                    "Faça OCR preciso e devolva apenas o conteúdo em Markdown, sem inventar informações."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Transcreva cuidadosamente TODO o texto da imagem. "
                            "Regras:\n"
                            "- Não invente texto.\n"
                            "- Não sumarize.\n"
                            "- Preserve títulos, listas e estrutura em Markdown.\n"
                            "- Responda somente com o Markdown."
                        ),
                    },
                    {"type": "image_url", "image_url": {"url": image_base64}},
                ],
            },
        ]

    @staticmethod
    def experiencia_mes_messages(image_base64: str) -> List[Dict[str, Any]]:
        """
        Extrai todos os atributos da Experiência do Mês. Responda somente com JSON.
        """
        return [
            {
                "role": "system",
                "content": (
                    "Você é um extrator de dados altamente preciso. "
                    "Extraia somente os campos solicitados a partir da imagem fornecida."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "A partir da imagem, extraia EXCLUSIVAMENTE os seguintes atributos:\n"
                            "1) Nome do vinho (exemplos: EL TOQUI RESERVA ESPECIAL)\n"
                            "2) Tipo (exemplos: Tinto, Branco, Rosé, Espumante, Fortificado)\n"
                            "3) Região (exemplos: D.O. Vale Central)\n"
                            "4) Vinícula (exemplos: Casas del Toqui)\n"
                            "5) Uva (exemplos: Cabernet Sauvignon, Merlot)\n"
                            "6) Amadurecimento (exemplos: Estágio de 8 meses em barricas de carvalho)\n"
                            "7) Potencial de Guarda (exemplos: 5 anos)\n"
                            "8) Visual (exemplos: Rubi Intenso)\n"
                            "9) Olfativo (exemplos: Aroma de frutas negras, especiarias)\n"
                            "10) Gustativo (exemplos: Redondo, com taninos aveludados e boa acidez)\n"
                            "11) Temperatura de serviço (exemplos: 18 C)\n"
                            "12) Harmonização (exemplos: pratos sugeridos)\n\n"
                            "Instruções:\n"
                            "- Se um atributo não estiver visível, retorne null nesse campo.\n"
                            "- Não invente informações.\n"
                            "- Responda SOMENTE com um JSON válido, sem comentários, sem Markdown, sem bloco de código.\n"
                            "- Execute o OCR cuidadosamente e verifique a precisão.\n"
                            "Formato exato da resposta:\n"
                            '{\"nome_vinho\": string|null, \"tipo\": string|null, \"regiao\": string|null, \"vinicula\": string|null, '
                            '\"uva\": string|null, \"amadurecimento\": string|null, \"potencial_guarda\": string|null, '
                            '\"visual\": string|null, \"olfativo\": string|null, \"gustativo\": string|null, '
                            '\"temperatura_servico\": string|null, \"harmonizacao\": string|null}'
                        ),
                    },
                    {"type": "image_url", "image_url": {"url": image_base64}},
                ],
            },
        ]