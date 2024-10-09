# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "SomItCoop ODOO helpdesk email reply to teams",
    "version": "12.0.1.0.0",
    "depends": [
        "helpdesk_mgmt",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Tools",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        ODOO helpdesk_mgmt email reply to teams.
        When sending a message from a ticket now the recipient gets as reply-to
        "catchall@mycompany.com". Instead, the reply to should be
        "helpdesk-team-alias@mycompany.com".
        This was fixed for Odoo 14 and this module backports the fix to Odoo 12.
        (See https://github.com/OCA/helpdesk/pull/381)
    """,
    "application": False,
    "installable": True,
}
