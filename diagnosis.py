from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[2]
PDF_PATH = ROOT / "output" / "pdf" / "mock-diagnosis-certificate-demo.pdf"
PDF_PATH.parent.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = A4

pdfmetrics.registerFont(TTFont("Malgun", r"C:\Windows\Fonts\malgun.ttf"))
pdfmetrics.registerFont(TTFont("Malgun-Bold", r"C:\Windows\Fonts\malgunbd.ttf"))


def draw_page(c: canvas.Canvas, _doc):
    c.saveState()
    c.setStrokeColor(colors.HexColor("#2F3A45"))
    c.setLineWidth(1.1)
    c.rect(16 * mm, 14 * mm, PAGE_W - 32 * mm, PAGE_H - 28 * mm, stroke=1, fill=0)

    c.setFont("Malgun-Bold", 36)
    c.setFillColor(colors.Color(0.78, 0.80, 0.83, alpha=0.28))
    c.translate(PAGE_W / 2, PAGE_H / 2)
    c.rotate(34)
    c.drawCentredString(0, 0, "DEMO - 실제 진단서 아님")
    c.rotate(-34)
    c.translate(-PAGE_W / 2, -PAGE_H / 2)

    c.setFillColor(colors.HexColor("#8B1E1E"))
    c.setFont("Malgun-Bold", 8.5)
    c.drawCentredString(
        PAGE_W / 2,
        20 * mm,
        "시연용 모의 문서 | 의료기관, 행정기관, 보험사 제출 불가 | 실제 의료진 발급 문서 아님",
    )
    c.restoreState()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="KRTitle",
        fontName="Malgun-Bold",
        fontSize=22,
        leading=29,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1F2933"),
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="KRSub",
        fontName="Malgun-Bold",
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#8B1E1E"),
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="KRBody",
        fontName="Malgun",
        fontSize=10.5,
        leading=16,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1F2933"),
    )
)
styles.add(
    ParagraphStyle(
        name="KRBodyBold",
        fontName="Malgun-Bold",
        fontSize=10.5,
        leading=16,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1F2933"),
    )
)
styles.add(
    ParagraphStyle(
        name="KRSection",
        fontName="Malgun-Bold",
        fontSize=12.5,
        leading=18,
        alignment=TA_LEFT,
        textColor=colors.white,
    )
)
styles.add(
    ParagraphStyle(
        name="KRNotice",
        fontName="Malgun-Bold",
        fontSize=10,
        leading=15,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#8B1E1E"),
    )
)


def p(text: str, style: str = "KRBody") -> Paragraph:
    return Paragraph(text, styles[style])


def section(title: str) -> Table:
    table = Table([[p(title, "KRSection")]], colWidths=[166 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#2F3A45")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


story = [
    Paragraph("모의진단서", styles["KRTitle"]),
    Paragraph("시연용 모의 문서 - 실제 진단서 아님 - 제출 불가", styles["KRSub"]),
]

notice = Table(
    [
        [
            p(
                "본 문서는 앱 OCR/AI 인식 기능 시연을 위한 가상 데이터입니다. "
                "실제 진단서, 소견서, 보험 청구 서류, 행정 제출 서류로 사용할 수 없습니다.",
                "KRNotice",
            )
        ]
    ],
    colWidths=[166 * mm],
)
notice.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF1F1")),
            ("BOX", (0, 0), (-1, -1), 1.1, colors.HexColor("#B42318")),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
story.extend([notice, Spacer(1, 9 * mm), section("1. 기본 정보")])

t1 = Table(
    [
        [p("문서 종류", "KRBodyBold"), p("모의진단서 (시연용)"), p("발급일자", "KRBodyBold"), p("2026.06.23")],
        [p("환자명", "KRBodyBold"), p("김모의"), p("생년월일", "KRBodyBold"), p("1958.04.12")],
        [p("성별", "KRBodyBold"), p("여"), p("진단일자", "KRBodyBold"), p("2026.06.10")],
        [p("발급기관", "KRBodyBold"), p("모의대학교병원 시연센터"), p("담당자", "KRBodyBold"), p("시연용 담당자")],
    ],
    colWidths=[27 * mm, 56 * mm, 27 * mm, 56 * mm],
    rowHeights=[12 * mm] * 4,
)
t1.setStyle(
    TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#C7CED6")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F4F7")),
            ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#F1F4F7")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
story.extend([t1, Spacer(1, 7 * mm), section("2. 진단 관련 정보")])

t2 = Table(
    [
        [p("주요 진단명", "KRBodyBold"), p("척수성 근위축증 의심")],
        [p("질병코드", "KRBodyBold"), p("G12.1")],
        [p("현재 상태", "KRBodyBold"), p("보행에 어려움이 있으며 일상생활 보조가 필요할 수 있음.")],
        [
            p("추가 확인", "KRBodyBold"),
            p("희귀질환 산정특례 및 희귀질환자 의료비 지원사업 대상 여부는 병원, 국민건강보험공단, 관할 보건소에서 확인 필요."),
        ],
    ],
    colWidths=[33 * mm, 133 * mm],
    rowHeights=[13 * mm, 13 * mm, 18 * mm, 24 * mm],
)
t2.setStyle(
    TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#C7CED6")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F4F7")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
story.extend([t2, Spacer(1, 7 * mm), section("3. 앱 인식 시연용 추출 대상")])

t3 = Table(
    [
        [
            p("AI/OCR 추출 후보", "KRBodyBold"),
            p(
                "문서 종류: 모의진단서 / 진단명: 척수성 근위축증 의심 / 질병코드: G12.1 / "
                "진단일자: 2026.06.10 / 일상생활 보조 필요 가능성"
            ),
        ]
    ],
    colWidths=[38 * mm, 128 * mm],
    rowHeights=[22 * mm],
)
t3.setStyle(
    TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#C7CED6")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F4F7")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
story.append(t3)

doc = SimpleDocTemplate(
    str(PDF_PATH),
    pagesize=A4,
    rightMargin=22 * mm,
    leftMargin=22 * mm,
    topMargin=22 * mm,
    bottomMargin=25 * mm,
)
doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
print(PDF_PATH)
