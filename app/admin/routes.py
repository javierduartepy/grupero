from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from app.models.persona import Persona
from app.models.grupo import Grupo
from app import db
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@admin_required
def dashboard():
    total_personas = Persona.query.count()
    total_grupos = Grupo.query.count()
    return render_template('admin/dashboard.html',
        total_personas=total_personas,
        total_grupos=total_grupos)


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '').strip()
        if usuario == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('admin/login_admin.html')


@admin_bp.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


@admin_bp.route('/personas')
@admin_required
def personas():
    personas = Persona.query.order_by(Persona.id).all()
    return render_template('admin/personas.html', personas=personas)


@admin_bp.route('/personas/eliminar/<int:persona_id>', methods=['POST'])
@admin_required
def eliminar_persona(persona_id):
    from app.grupo.services import obtener_ids_con_grupo
    ids_con_grupo = obtener_ids_con_grupo()
    if persona_id in ids_con_grupo:
        flash('No se puede eliminar una persona que está en un grupo.', 'danger')
        return redirect(url_for('admin.personas'))
    persona = Persona.query.get_or_404(persona_id)
    db.session.delete(persona)
    db.session.commit()
    flash('Persona eliminada.', 'warning')
    return redirect(url_for('admin.personas'))


@admin_bp.route('/grupos')
@admin_required
def grupos():
    grupos = Grupo.query.order_by(Grupo.id).all()
    return render_template('admin/grupos.html', grupos=grupos)


@admin_bp.route('/grupos/eliminar/<int:grupo_id>', methods=['POST'])
@admin_required
def eliminar_grupo(grupo_id):
    grupo = Grupo.query.get_or_404(grupo_id)
    db.session.delete(grupo)
    db.session.commit()
    flash('Grupo eliminado.', 'warning')
    return redirect(url_for('admin.grupos'))


@admin_bp.route('/grupos/asignar/<int:grupo_id>', methods=['POST'])
@admin_required
def asignar_tema(grupo_id):
    grupo = Grupo.query.get_or_404(grupo_id)
    grupo.tema = request.form.get('tema', '').strip()
    grupo.observacion = request.form.get('observacion', '').strip()
    grupo.fecha_exposicion = request.form.get('fecha_exposicion', '').strip()

    archivo = request.files.get('archivo')
    if archivo and allowed_file(archivo.filename):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(archivo.filename)
        archivo.save(os.path.join(UPLOAD_FOLDER, filename))
        grupo.archivo = filename

    db.session.commit()
    flash('Tema asignado correctamente.', 'success')
    return redirect(url_for('admin.grupos'))


@admin_bp.route('/grupos/eliminar-tema/<int:grupo_id>', methods=['POST'])
@admin_required
def eliminar_tema(grupo_id):
    grupo = Grupo.query.get_or_404(grupo_id)
    grupo.tema = None
    grupo.archivo = None
    grupo.observacion = None
    grupo.fecha_exposicion = None
    db.session.commit()
    flash('Tema eliminado.', 'warning')
    return redirect(url_for('admin.grupos'))


@admin_bp.route('/grupos/pdf')
@admin_required
def grupos_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    import io

    grupos = Grupo.query.order_by(Grupo.id).all()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph('GruPero — Grupos Formados', styles['Title']))
    elements.append(Paragraph('Arquitectura y Sistema Operativo · TUP · UTN FRRe', styles['Normal']))
    elements.append(Spacer(1, 20))

    data = [['#', 'Integrantes', 'Tema', 'Fecha']]
    for g in grupos:
        integrantes = ', '.join(f"{p.nombre} {p.apellido}" for p in g.personas)
        tema = g.tema or 'Sin asignar'
        fecha = g.fecha_exposicion or '—'
        if fecha and fecha != '—':
            try:
                from datetime import datetime
                fecha = datetime.strptime(fecha, '%Y-%m-%d').strftime('%d/%m/%Y')
            except:
                pass
        data.append([str(g.id), integrantes, tema, fecha])

    tabla = Table(data, colWidths=[30, 200, 150, 80])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a2e50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f4ff')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ddddee')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(tabla)
    doc.build(elements)

    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=grupos.pdf'
    return response