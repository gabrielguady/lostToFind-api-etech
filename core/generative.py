import google.generativeai as genai
import json

from core import models

GOOGLE_API_KEY = 'AIzaSyBP8LAMQrYw0uryVy0tqYV5dmSZ4iqxlsQ'


class GoogleGenerativeFilter:
    def __init__(self, lost_description):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.generation_config = self.gemini_configure()
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.lost_description = lost_description
        self.list_category = list(models.Category.objects.all().values('id', 'name'))

    @staticmethod
    def gemini_configure():
        return genai.GenerationConfig(
            temperature=0.2,
            max_output_tokens=1024,
            top_p=0.95,
            top_k=40,
            response_mime_type="application/json"
        )

    def get_prompt(self):
        return f"""
                Você é um especialista em extração de palavras-chave para um sistema de busca de itens perdidos. Sua tarefa é analisar a "Descrição de perda" fornecida por um usuário e extrair informações relevantes, classificando-as nos campos especificados.
            
                **Objetivo:** Gerar palavras-chave e IDs de categoria que otimizem a busca em um banco de dados de itens perdidos.
            
                **Campos para Extração:**
            
                * **title:** (Lista de strings) Extraia o nome principal ou a identificação mais clara do item. Pense no que alguém digitaria se soubesse exatamente o que procura. Inclua variações e sinônimos curtos. Ex: ["celular", "iphone 15 pro", "smartphone", "fone de ouvido jbl"].
                * **description:** (Lista de strings) Extraia detalhes descritivos sobre o item, suas características, estado, cores, o que ele continha (se aplicável), e o local mais específico onde foi encontrado ou as circunstâncias da perda. Inclua marcas, modelos, cores, materiais e descrições do estado (ex: "tela trincada", "com capa preta"). Evite palavras genéricas ou stop words, a menos que sejam cruciais para o significado.
                * **date_found:** (String ou null) Se a "Descrição de perda" mencionar uma data **em que o item foi encontrado ou a data aproximada da perda**, extraia essa data. O formato deve ser "YYYY-MM-DD". Se nenhuma data for explicitamente mencionada ou inferível, retorne `null`.
                * **city:** (Lista de strings) Extraia o nome da cidade mencionada na descrição onde o item foi encontrado ou perdido. Inclua sinônimos se houver (ex: "Manaus", "Manaus AM").
                * **category:** (Lista de inteiros) Com base na "Descrição de perda" e na lista de categorias fornecida, identifique e retorne **apenas os IDs das categorias que mais se encaixam** no item descrito. Se mais de uma categoria for aplicável, inclua todas. Se nenhuma categoria se encaixar, retorne uma lista vazia.
            
                **Lista de Categorias Disponíveis:**
                {json.dumps(self.list_category, indent=2)}
            
                **Regras de Retorno:**
                * Se um campo não puder ser preenchido com base na descrição, retorne uma lista vazia `[]` para os campos de lista, ou `null` para `date_found`.
                * O retorno deve ser **EXATAMENTE** no formato JSON abaixo, sem informações adicionais ou explicações:
            
                ```json
                {{
                  "title": ["palavra1", "palavra2"],
                  "description": ["detalhe1", "detalhe2"],
                  "date_found": "YYYY-MM-DD" ou null,
                  "city": ["cidade1"],
                  "category": [id1, id2]
                }}
                ```
                **Descrição de perda:**
                {self.lost_description}
                """

    def get_filters(self):
        response = None
        try:
            response = self.model.generate_content(
                self.get_prompt(),
                generation_config=self.generation_config
            )
        except Exception as e:
            print(f"Ocorreu um erro ao chamar a API ou parsear a resposta: {e}")
            raise RuntimeError(f"Erro ao chamar a API ou parsear a resposta: {e}") from e

        if 'response' in locals() and hasattr(response, 'text'):
            parsed_response = json.loads(response.text)
            print(json.dumps(parsed_response, indent=2, ensure_ascii=False))
            return parsed_response
        return None

    def get_found_items(self):
        filters = self.get_filters()
        if not filters:
            return models.FoundItem.objects.none()

        lookup = {}
        if filters.get('title'):
            lookup['title__incontains'] = filters['title']
        if filters.get('description'):
            lookup['description__incontains'] = filters['description']
        if filters.get('city'):
            lookup['city__incontains'] = filters['city']
        if filters.get('category'):
            lookup['category__in'] = filters['category']
        if filters.get('date_found'):
            lookup['date_found__gte'] = filters['date_found']

        return models.FoundItem.objects.filter(**lookup)

    def run(self):
        return self.get_found_items()
