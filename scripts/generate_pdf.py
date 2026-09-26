"""Gera um PDF de compartilhamento com a documentação e diagramas do projeto."""
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "controle-frota-modelagem.pdf"
IMAGES = ROOT / "tmp" / "pdfs" / "png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BLUE = HexColor("#17365D")
MID_BLUE = HexColor("#2F75B5")
TEXT = HexColor("#25313C")
MUTED = HexColor("#667585")
LIGHT = HexColor("#EAF1F8")


def fit_image(c, image_path, x, y, width, height):
    image = ImageReader(str(image_path))
    image_width, image_height = image.getSize()
    scale = min(width / image_width, height / image_height)
    drawn_width = image_width * scale
    drawn_height = image_height * scale
    c.drawImage(
        image,
        x + (width - drawn_width) / 2,
        y + (height - drawn_height) / 2,
        drawn_width,
        drawn_height,
        preserveAspectRatio=True,
        mask="auto",
    )


def footer(c, page, width):
    c.setStrokeColor(HexColor("#D9E2F3"))
    c.line(36, 28, width - 36, 28)
    c.setFont("DejaVu", 8)
    c.setFillColor(MUTED)
    c.drawString(36, 16, "Controle de Frota - Documentação de Modelagem")
    c.drawRightString(width - 36, 16, f"Página {page}")


def wrapped_lines(text, font_name, font_size, max_width):
    """Quebra texto preservando palavras para não cortar conteúdo na margem."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(c, text, x, y, max_width, font_name="DejaVu", font_size=10.5, leading=15):
    c.setFont(font_name, font_size)
    for line in wrapped_lines(text, font_name, font_size, max_width):
        c.drawString(x, y, line)
        y -= leading
    return y


def cover(c, page):
    width, height = A4
    c.setPageSize(A4)
    c.setFillColor(BLUE)
    c.rect(0, height - 225, width, 225, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DejaVu-Bold", 28)
    c.drawString(48, height - 92, "Sistema de Controle de Frota")
    c.setFont("DejaVu", 14)
    c.drawString(48, height - 122, "Documentação de modelagem UML e banco de dados")
    c.setFillColor(MID_BLUE)
    c.rect(48, height - 170, 144, 4, fill=1, stroke=0)

    c.setFillColor(TEXT)
    c.setFont("DejaVu-Bold", 15)
    c.drawString(48, height - 290, "Conteúdo deste documento")
    c.setFont("DejaVu", 11)
    items = [
        "Diagrama de casos de uso e permissões",
        "Diagrama de classes do domínio",
        "Diagrama UML de pacotes - arquitetura da aplicação",
        "Diagrama de sequência - abertura e retorno do veículo",
        "Modelo entidade-relacionamento e estrutura MySQL",
    ]
    y = height - 322
    for item in items:
        c.setFillColor(MID_BLUE)
        c.circle(55, y + 3, 3, fill=1, stroke=0)
        c.setFillColor(TEXT)
        c.drawString(70, y, item)
        y -= 28

    c.setFillColor(LIGHT)
    c.roundRect(48, 130, width - 96, 90, 8, fill=1, stroke=0)
    c.setFillColor(TEXT)
    c.setFont("DejaVu-Bold", 10)
    c.drawString(64, 194, "Identificação do grupo")
    c.setFont("DejaVu", 10)
    c.drawString(64, 172, "Integrantes: preencher antes da entrega")
    c.drawString(64, 152, "Repositório GitHub: inserir a URL do projeto")
    footer(c, page, width)
    c.showPage()


def overview(c, page):
    width, height = A4
    c.setPageSize(A4)
    c.setFillColor(BLUE)
    c.setFont("DejaVu-Bold", 19)
    c.drawString(42, height - 55, "Visão geral e regras de negócio")
    c.setStrokeColor(MID_BLUE)
    c.setLineWidth(2)
    c.line(42, height - 68, width - 42, height - 68)

    c.setFillColor(TEXT)
    lines = [
        "O sistema registra a saída e o retorno de carros, caminhões e motos da empresa.",
        "O Porteiro realiza os lançamentos da portaria; o Administrador gerencia cadastros e relatórios.",
        "Uma saída armazena motorista, veículo, placa, destino, data/hora e quilometragem de saída.",
        "No retorno, são registrados data/hora e quilometragem final; a saída é encerrada e o veículo é liberado.",
    ]
    y = height - 105
    for line in lines:
        y = draw_wrapped(c, line, 52, y, width - 104)
        y -= 6

    c.setFont("DejaVu-Bold", 13)
    c.setFillColor(BLUE)
    c.drawString(42, y - 14, "Regras modeladas")
    y -= 48
    rules = [
        "1. O veículo só pode sair quando estiver disponível.",
        "2. O motorista deve estar ativo, com CNH válida e categoria compatível.",
        "3. Um veículo só pode possuir uma saída aberta simultaneamente.",
        "4. A quilometragem de retorno não pode ser menor que a quilometragem de saída.",
        "5. Abrir a saída muda o veículo para EM_USO; encerrá-la o devolve a DISPONIVEL.",
        "6. Veículos em manutenção ou inativos não podem ser liberados.",
    ]
    c.setFont("DejaVu", 10.5)
    c.setFillColor(TEXT)
    for rule in rules:
        c.setFillColor(LIGHT)
        c.roundRect(42, y - 7, width - 84, 23, 4, fill=1, stroke=0)
        c.setFillColor(TEXT)
        c.drawString(52, y, rule)
        y -= 34

    c.setFont("DejaVu-Bold", 11)
    c.setFillColor(BLUE)
    c.drawString(42, 102, "Observação técnica")
    c.setFont("DejaVu", 9.5)
    c.setFillColor(TEXT)
    c.drawString(42, 83, "O esquema MySQL implementa chaves estrangeiras, índices e uma chave única")
    c.drawString(42, 68, "para reforçar a regra de somente uma saída aberta por veículo.")
    footer(c, page, width)
    c.showPage()


def diagram_page(c, page, title, explanation, image_name, portrait=False):
    size = A4 if portrait else landscape(A4)
    width, height = size
    c.setPageSize(size)
    c.setFillColor(BLUE)
    c.setFont("DejaVu-Bold", 17)
    c.drawString(36, height - 42, title)
    c.setStrokeColor(MID_BLUE)
    c.setLineWidth(2)
    c.line(36, height - 54, width - 36, height - 54)
    c.setFont("DejaVu", 9.2)
    c.setFillColor(TEXT)
    c.drawString(36, height - 73, explanation)
    fit_image(c, IMAGES / image_name, 36, 42, width - 72, height - 137)
    footer(c, page, width)
    c.showPage()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont("DejaVu", FONT))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_BOLD))
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("Controle de Frota - Modelagem UML e Banco de Dados")
    c.setAuthor("Grupo da Prática Extensionista IV")

    cover(c, 1)
    overview(c, 2)
    diagram_page(c, 3, "1. Diagrama de Casos de Uso", "Atores, permissões e validações obrigatórias do sistema.", "01-casos-de-uso.png", portrait=True)
    diagram_page(c, 4, "2. Diagrama de Classes", "Entidades de domínio, atributos, operações e multiplicidades.", "02-diagrama-de-classes.png")
    diagram_page(c, 5, "3. Diagrama UML de Pacotes", "Arquitetura lógica da aplicação PHP em camadas e dependências.", "03-diagrama-de-pacotes.png")
    diagram_page(c, 6, "4. Diagrama de Sequência", "Transação de abertura de saída e encerramento no retorno do veículo.", "04-sequencia-saida-retorno.png", portrait=True)
    diagram_page(c, 7, "5. Modelo Entidade-Relacionamento", "Estrutura relacional correspondente ao script MySQL 8+.", "05-modelo-entidade-relacionamento.png")
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
