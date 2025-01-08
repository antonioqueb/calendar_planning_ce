# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class TemporalPlanning(models.Model):
    _name = 'temporal.planning'
    _description = 'Planificación Temporal'
    _rec_name = 'project_id'

    # Campos básicos
    project_id = fields.Many2one(
        'project.project', 
        string="Proyecto", 
        required=True, 
        help="Selecciona el proyecto asociado con esta planificación."
    )
    start_date = fields.Date(
        string='Fecha de Inicio', 
        required=True, 
        help="Fecha en la que inicia la planificación."
    )
    end_date = fields.Date(
        string='Fecha de Finalización', 
        required=True, 
        help="Fecha en la que finaliza la planificación."
    )
    assigned_user_id = fields.Many2one(
        'res.users', 
        string="Responsable", 
        default=lambda self: self.env.user,
        help="Usuario responsable de esta planificación."
    )
    notes = fields.Text(
        string="Notas", 
        help="Información adicional o comentarios sobre esta planificación."
    )

    # Campos calculados
    duration_days = fields.Integer(
        string="Duración (días)", 
        compute="_compute_duration_days", 
        store=True, 
        help="Duración de la planificación en días."
    )

    # Restricciones
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de finalización.")

    @api.constrains('project_id', 'start_date', 'end_date')
    def _check_project_overlap(self):
        """Evita traslapos de fechas para un mismo proyecto"""
        for record in self:
            overlapping_records = self.env['temporal.planning'].search([
                ('id', '!=', record.id),
                ('project_id', '=', record.project_id.id),
                ('start_date', '<=', record.end_date),
                ('end_date', '>=', record.start_date)
            ])
            if overlapping_records:
                raise ValidationError(
                    f"El proyecto '{record.project_id.name}' ya tiene una planificación que traslapa con estas fechas."
                )

    # Métodos calculados
    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration_days = (record.end_date - record.start_date).days + 1
            else:
                record.duration_days = 0

    # Métodos CRUD (opcional)
    @api.model
    def create(self, vals):
        """Sobrecarga del método create para agregar lógica personalizada"""
        record = super(TemporalPlanning, self).create(vals)
        # Aquí puedes agregar lógica adicional si es necesario
        return record

    def write(self, vals):
        """Sobrecarga del método write para agregar lógica personalizada"""
        result = super(TemporalPlanning, self).write(vals)
        # Aquí puedes agregar lógica adicional si es necesario
        return result

    def unlink(self):
        """Sobrecarga del método unlink para evitar eliminación de ciertos registros"""
        for record in self:
            if record.project_id and record.start_date > fields.Date.today():
                raise ValidationError("No puedes eliminar planificaciones futuras asociadas a un proyecto.")
        return super(TemporalPlanning, self).unlink()

    # Métodos auxiliares
    def action_open_project(self):
        """Acción para abrir el proyecto asociado"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Proyecto',
            'res_model': 'project.project',
            'view_mode': 'form',
            'res_id': self.project_id.id,
            'target': 'current',
        }
