"""Genera Guion_Detectives_Continuidad.docx a partir del guion de las 6 escenas."""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

PERSON_COLORS = {
    "Sofía Cabrera": RGBColor(0x0E, 0x7A, 0xB4),   # celeste oscuro
    "Micaela Cubilla": RGBColor(0x6D, 0x28, 0xD9),   # violeta
    "Fabrizio Riquelme": RGBColor(0xB4, 0x7B, 0x0E),   # ámbar oscuro
    "Jerónimo Lovera": RGBColor(0xC2, 0x41, 0x0C),   # rosa/rojo oscuro
    "Todos": RGBColor(0x0E, 0x7A, 0xB4),
}


def fmt_time(s):
    m = int(s) // 60
    sec = int(s) % 60
    return f"{m}:{sec:02d}"


SCENES = [
    dict(num=1, title="Introducción", dur=25, speaker="Sofía Cabrera",
         text=[
             "¡Hola a todos! Hoy vamos a explicar qué es la continuidad de una función "
             "y cómo podemos identificar los diferentes tipos de discontinuidad.",
         ]),
    dict(num=2, title="Concepto de continuidad", dur=50, speaker="Sofía Cabrera",
         text=[
             "Primero, ¿qué significa que una función sea continua?",
             "Podemos imaginar una gráfica que podemos recorrer sin interrupciones. Pero en "
             "Matemática, para comprobar que una función es continua en un punto, tenemos "
             "que verificar tres condiciones.",
             "Primera: la función debe estar definida en ese punto, es decir, f(a) tiene "
             "que existir.",
             "Segunda: el límite de la función cuando x se acerca a ese punto debe existir.",
             "Tercera: el valor del límite debe ser igual al valor de la función.",
             "Veamos un ejemplo sencillo: f(x) = x², en x = 2.",
             "Primero, f(2) = 4. Después, calculamos el límite cuando x tiende a 2, que "
             "también es 4.",
             "Como el límite y el valor de la función coinciden, y se cumplen las tres "
             "condiciones, podemos concluir que la función es continua en x = 2.",
         ]),
    dict(num=3, title="Discontinuidad evitable", dur=50, speaker="Micaela Cubilla",
         text=[
             "Ahora vamos a ver el primer tipo de discontinuidad: la evitable.",
             "Se llama así porque podemos eliminarla cambiando o definiendo el valor de "
             "la función en un solo punto.",
             "Para entenderlo, vamos a utilizar uno de los ejercicios que resolvimos en clase.",
             "Tenemos una función por tramos: 3x menos 1 cuando x es menor que 1; 4 cuando "
             "x es igual a 1; y x al cuadrado más 1 cuando x es mayor que 1.",
             "Queremos analizar qué ocurre en x = 1.",
             "Primero, el valor de la función es 4.",
             "Después, calculamos los límites laterales. Por la izquierda obtenemos 2, y "
             "por la derecha también obtenemos 2.",
             "Esto significa que el límite existe y es igual a 2.",
             "Sin embargo, el valor de la función es 4, por lo que no se cumple la tercera "
             "condición de continuidad.",
             "En la gráfica podemos observar un círculo abierto en el punto (1,2) y un "
             "punto cerrado en (1,4).",
             "Por eso, concluimos que tenemos una discontinuidad evitable. Si cambiáramos "
             "el valor de la función en x = 1 a 2, la función sería continua en ese punto.",
         ]),
    dict(num=4, title="Discontinuidad inevitable finita (de salto)", dur=45,
         speaker="Fabrizio Riquelme",
         text=[
             "El segundo tipo es la discontinuidad inevitable finita, también conocida "
             "como discontinuidad de salto.",
             "Esta ocurre cuando los límites laterales existen y son números finitos, "
             "pero tienen valores diferentes.",
             "Por ejemplo, imaginemos una función que vale 1 cuando x es menor que 0 y "
             "que vale 3 cuando x es mayor o igual que 0.",
             "Si nos acercamos a cero desde la izquierda, la función se aproxima a 1.",
             "Pero, si nos acercamos desde la derecha, se aproxima a 3.",
             "Como ambos resultados son diferentes, el límite general no existe.",
             "En la gráfica podemos ver claramente un salto entre los dos valores.",
             "Por eso se llama discontinuidad de salto y no podemos solucionarla cambiando "
             "solamente el valor de la función en un punto.",
         ]),
    dict(num=5, title="Discontinuidad inevitable infinita", dur=55, speaker="Jerónimo Lovera",
         text=[
             "Por último, tenemos la discontinuidad inevitable infinita.",
             "Para explicarla, vamos a utilizar el ejercicio que presentamos en nuestro cartel.",
             "La función es h(x) = 2 dividido entre x más 3, y queremos analizarla en x = −3.",
             "Primero, reemplazamos x por −3 y obtenemos 2 dividido entre 0.",
             "Como no podemos dividir entre cero, la función no está definida en ese punto.",
             "Ahora analizamos sus límites laterales.",
             "Cuando nos acercamos a −3 por la izquierda, los valores de la función "
             "disminuyen sin límite, es decir, tienden a menos infinito.",
             "En cambio, cuando nos acercamos por la derecha, los valores aumentan sin "
             "límite y tienden a más infinito.",
             "En la gráfica podemos observar una asíntota vertical en x = −3.",
             "Un error frecuente es pensar que, porque aparece el infinito, el límite "
             "existe y la función es continua. Esto es incorrecto.",
             "Por lo tanto, concluimos que la función presenta una discontinuidad "
             "inevitable infinita en x = −3.",
         ]),
    dict(num=6, title="Repaso y conclusión", dur=45, speaker="Todos",
         text_multi=[
             ("Sofía Cabrera", "En conclusión, para saber si una función es continua, "
                                 "debemos comprobar siempre las tres condiciones fundamentales."),
             ("Micaela Cubilla", "Si el límite existe, pero no coincide con el valor de la "
                                 "función, podemos tener una discontinuidad evitable."),
             ("Fabrizio Riquelme", "Si los límites laterales son finitos pero diferentes, "
                                 "tenemos una discontinuidad de salto."),
             ("Jerónimo Lovera", "Y si la función presenta un comportamiento infinito cerca "
                                 "de un punto, tenemos una discontinuidad infinita."),
             ("Todos / Sofía Cabrera", "¡Y así podemos identificar los distintos tipos de "
                                         "continuidad y discontinuidad de una función!"),
         ]),
]

t = 0
for sc in SCENES:
    sc["t_start"] = t
    t += sc["dur"]
    sc["t_end"] = t
TOTAL = t

doc = Document()
section = doc.sections[0]
section.left_margin = Cm(2.0)
section.right_margin = Cm(2.0)
section.top_margin = Cm(1.8)
section.bottom_margin = Cm(1.8)

title = doc.add_heading("Guion — Detectives de la continuidad", level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run("Develando los secretos de las funciones")
r.italic = True
r.font.size = Pt(13)

course = doc.add_paragraph()
course.alignment = WD_ALIGN_PARAGRAPH.CENTER
cr = course.add_run("Matemática · 3° B BATIN")
cr.font.size = Pt(11)
cr.font.color.rgb = RGBColor(0x60, 0x60, 0x60)

team = doc.add_paragraph()
team.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = team.add_run(
    "Equipo: Sofía Cabrera · Micaela Cubilla · Fabrizio Riquelme · Jerónimo Lovera"
)
tr.font.size = Pt(11)

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run(f"Duración total del video: {fmt_time(TOTAL)} min  ({TOTAL} s)")
r2.font.size = Pt(10.5)
r2.font.color.rgb = RGBColor(0x60, 0x60, 0x60)

doc.add_paragraph()

instr = doc.add_paragraph()
instr.add_run(
    "Instrucciones de grabación: cada integrante graba su propia parte en un archivo de "
    "audio separado (.mp3 / .m4a / .wav), hablando con naturalidad. Los tiempos (m:ss) "
    "marcan dónde empieza cada escena en el video ya editado. La Escena 6 (cierre) es "
    "compartida: pueden grabarla los cuatro juntos en una sola toma, pasándose el turno "
    "para hablar, o grabar cuatro clips cortos por separado — el script "
    "sincronizar_audios.py acepta ambas formas. No hace falta cronometrarse de forma "
    "exacta: el script ajusta la duración de cada escena a la del audio grabado."
).italic = True

doc.add_paragraph()

doc.add_heading("Reparto por escena", level=2)
table = doc.add_table(rows=1, cols=4)
table.style = "Light Grid Accent 1"
table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = table.rows[0].cells
for i, h in enumerate(["#", "Escena", "Tiempo", "Integrante"]):
    hdr[i].text = h
    for run in hdr[i].paragraphs[0].runs:
        run.bold = True

for sc in SCENES:
    row = table.add_row().cells
    row[0].text = str(sc["num"])
    row[1].text = sc["title"]
    row[2].text = f'{fmt_time(sc["t_start"])}–{fmt_time(sc["t_end"])}'
    row[3].text = sc["speaker"]
    color = PERSON_COLORS[sc["speaker"]]
    for run in row[3].paragraphs[0].runs:
        run.font.color.rgb = color
        run.bold = True

doc.add_page_break()
doc.add_heading("Guion completo", level=1)

for sc in SCENES:
    h = doc.add_heading(
        f'Escena {sc["num"]} — {sc["title"]}  ({fmt_time(sc["t_start"])}–{fmt_time(sc["t_end"])})',
        level=2,
    )

    if "text_multi" in sc:
        for speaker, line in sc["text_multi"]:
            color = PERSON_COLORS.get(speaker, PERSON_COLORS["Sofía Cabrera"])
            sp = doc.add_paragraph()
            srun = sp.add_run(f"{speaker}: ")
            srun.bold = True
            srun.font.color.rgb = color
            srun.font.size = Pt(12)
            lrun = sp.add_run(line)
            lrun.font.color.rgb = color
            lrun.font.size = Pt(12.5)
            sp.paragraph_format.space_after = Pt(8)
    else:
        color = PERSON_COLORS[sc["speaker"]]
        sp = doc.add_paragraph()
        run = sp.add_run(f'Habla: {sc["speaker"]}')
        run.bold = True
        run.font.color.rgb = color
        run.font.size = Pt(12)

        for line in sc["text"]:
            lp = doc.add_paragraph()
            lp.paragraph_format.space_after = Pt(6)
            lrun = lp.add_run(line)
            lrun.font.color.rgb = color
            lrun.font.size = Pt(12.5)

    doc.add_paragraph()

doc.add_heading("Créditos finales", level=2)
cred = doc.add_paragraph()
cred.add_run(
    "Los nombres de los cuatro integrantes ya aparecen en pantalla al final de la "
    "Escena 6, debajo del mensaje de cierre."
).italic = True

doc.save("/home/user/Video-Mate/video_continuidad/Guion_Detectives_Continuidad.docx")
print("Guion generado. Duración total:", fmt_time(TOTAL), f"({TOTAL}s)")
for sc in SCENES:
    print(sc["num"], sc["title"], fmt_time(sc["t_start"]), "-", fmt_time(sc["t_end"]), sc["speaker"])
