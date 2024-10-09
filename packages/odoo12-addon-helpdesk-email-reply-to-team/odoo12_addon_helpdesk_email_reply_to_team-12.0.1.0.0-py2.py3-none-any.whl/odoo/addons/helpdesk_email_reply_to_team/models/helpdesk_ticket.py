from odoo import models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    # See (https://github.com/OCA/helpdesk/pull/381/files)
    def _notify_get_reply_to(
        self, default=None, records=None, company=None, doc_names=None
    ):
        """Override to set alias of tasks to their team if any."""
        aliases = (
            self.sudo()
            .mapped("team_id")
            ._notify_get_reply_to(
                default=default, records=None, company=company, doc_names=None
            )
        )
        res = {ticket.id: aliases.get(ticket.team_id.id) for ticket in self}
        leftover = self.filtered(lambda rec: not rec.team_id)
        if leftover:
            res.update(
                super(HelpdeskTicket, leftover)._notify_get_reply_to(
                    default=default, records=None, company=company, doc_names=doc_names
                )
            )
        return res
