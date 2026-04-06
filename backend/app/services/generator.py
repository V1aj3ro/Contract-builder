from docxtpl import DocxTemplate
from pathlib import Path
from num2words import num2words
import datetime
import io

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "contract_template.docx"


def format_date(d: datetime.date) -> str:
    months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]
    return f"{d.day} {months[d.month - 1]} {d.year}"


def amount_to_words(amount: int) -> str:
    words = num2words(amount, lang='ru')
    return words


def pct_to_words(pct: int) -> str:
    words = {
        10: "десяти", 15: "пятнадцати", 20: "двадцати",
        25: "двадцати пяти", 30: "тридцати", 40: "сорока",
        50: "пятидесяти", 60: "шестидесяти", 70: "семидесяти",
        80: "восьмидесяти", 90: "девяноста", 100: "ста"
    }
    return words.get(pct, str(pct))


def tranch_text(pct, condition, final=False):
    if not condition:
        return ""
    if final:
        return (
            f"Заказчик в течение 5 (пяти) рабочих дней {condition} "
            f"производит окончательную оплату выполненных работ"
        )
    if not pct:
        return ""
    pct_words = pct_to_words(pct)
    return (
        f"Заказчик в течение 5 (пяти) рабочих дней {condition} "
        f"производит авансовый платеж в размере {pct} ({pct_words}) % "
        f"от стоимости работ по договору."
    )


def short_name(full_name: str) -> str:
    name = full_name.strip()
    if name.upper().startswith("ИП "):
        name = name[3:].strip()
    parts = name.split()
    if len(parts) >= 3:
        return f"{parts[1][0]}.{parts[2][0]}. {parts[0]}"
    elif len(parts) == 2:
        return f"{parts[1][0]}. {parts[0]}"
    return name


def generate_contract(contract, customer) -> bytes:
    tpl = DocxTemplate(TEMPLATE_PATH)

    # Преамбула заказчика
    if customer.is_individual:
        customer_preamble = (
            f"{customer.full_name}, именуемый в дальнейшем «Заказчик»,"
        )
    else:
        signer_genitive = customer.signer_name_genitive or customer.signer_name
        display_name = customer.full_name_extended or customer.full_name
        customer_preamble = (
            f"{display_name}, именуемое в дальнейшем «Заказчик», "
            f"в лице {customer.signer_role} {signer_genitive}, "
            f"действующего на основании Устава,"
        )

    
    if contract.basis_enabled and contract.basis_type and contract.basis_number:
        basis_text = (
            f"Работы выполняются во исполнение {contract.basis_type} "
            f"{contract.basis_number} от {format_date(contract.basis_date)} г. "
            f"по объекту «{contract.object_full_name}» с учетом всех требований "
            f"Технического задания, являющихся неотъемлемой частью "
            f"{contract.basis_type} {contract.basis_number} и настоящего договора "
            f"(Приложение №1 к настоящему договору)."
        )
    else:
        basis_text = ""

    
    vat_text = "НДС включён" if contract.vat_included else "НДС не предусмотрен"

    
    amount_int = int(contract.amount)

    
    customer_kpp_line = f"КПП {customer.kpp}" if customer.kpp else ""

    
    signer_role_cap = (customer.signer_role or "").capitalize()

    context = {
        "contract_number": contract.number,
        "contract_day": contract.date.day,
        "contract_month_year": format_date(contract.date).split(" ", 1)[1],
        "city": contract.city,

        "customer_preamble": customer_preamble,
        "customer_full_name": customer.full_name,
        "customer_short_name": customer.short_name,
        "customer_short_name_upper": customer.full_name.upper(),
        "customer_full_name_upper": customer.full_name.upper(),
        "customer_inn": customer.inn,
        "customer_ogrn": customer.ogrn,
        "customer_kpp_line": customer_kpp_line,
        "customer_legal_address": customer.legal_address,
        "customer_bank_name": customer.bank_name,
        "customer_bik": customer.bik,
        "customer_account": customer.account,
        "customer_corr_account": customer.corr_account,
        "customer_signer_name": customer.signer_name,
        "customer_signer_name_short": short_name(customer.signer_name),
        "customer_signer_role": customer.signer_role_nominative or signer_role_cap,

        "contractor_full_name": contract.contractor_full_name,
        "contractor_inn": contract.contractor_inn,
        "contractor_ogrn": contract.contractor_ogrn,
        "contractor_legal_address": contract.contractor_legal_address,
        "contractor_bank_name": contract.contractor_bank_name,
        "contractor_bik": contract.contractor_bik,
        "contractor_account": contract.contractor_account,
        "contractor_corr_account": contract.contractor_corr_account,
        "contractor_signer_short": short_name(contract.contractor_full_name),
        "contractor_phone": f"Тел. {contract.contractor_phone}" if contract.contractor_phone else "",

        "object_full_name": contract.object_full_name,
        "basis_enabled": contract.basis_enabled,
        "basis_text": basis_text,

        "works_text": contract.works_text,

        "date_start": format_date(contract.date_start),
        "date_end": format_date(contract.date_end),

        "amount_num": f"{amount_int:,}".replace(",", " "),
        "amount_words": amount_to_words(amount_int),
        "vat_text": vat_text,

        "tranch1_text": tranch_text(contract.tranch1_pct, contract.tranch1_condition),
        "tranch2_text": tranch_text(contract.tranch2_pct, contract.tranch2_condition),
        "tranch3_text": tranch_text(None, contract.tranch3_condition or "с момента подписания акта сдачи-приемки выполненных работ", final=True),
        "has_tranch3": True,
        "has_tranch2": bool(contract.tranch2_pct and contract.tranch2_condition),
        "has_tranch3": bool(contract.tranch3_condition),
        "works_stages": f"Стадийность проектирования: {contract.works_stages}" if contract.works_stages else "",
        "works_results_header": "Результаты работ в пределах указанного выше объёма работ:" if contract.works_results else "",
        "works_results": contract.works_results or "",
    }

    tpl.render(context)
    tpl.render(context)

    from docx.oxml.ns import qn
    doc = tpl.docx
    for para in doc.paragraphs:
        if para.text.strip() == '' and any(
            run.text.strip() == '' for run in para.runs
        ) and len(para.runs) > 0:
            numPr = para._element.find('.//' + qn('w:numPr'))
            if numPr is not None:
                p = para._element
                p.getparent().remove(p)

    buf = io.BytesIO()
    tpl.save(buf)
    return buf.getvalue()

