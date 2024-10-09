##############################
 Helpdesk Email Reply to Team
##############################

When sending a message from a ticket, the recipient gets as reply-to
"catchall@mycompany.com". Instead, the reply to should be
"helpdesk-team-alias@mycompany.com".

This was fixed for Odoo 14 and this module backports the fix to Odoo 12.
(See https://github.com/OCA/helpdesk/pull/381)

**Table of contents**

.. contents::
   :local:

***************
 Configuration
***************

No configuration needed for this module.

*******
 Usage
*******

To use this module, you need to go to Helpdesk -> Configuration ->
Teams and create a team with an alias. Then, create a ticket and assign
it to the team. Finally, send an email from the ticket.

************************
 Known issues / Roadmap
************************

There are no issues for the moment.

*************
 Bug Tracker
*************

Bugs are tracked on `GitLab Issues
<https://gitlab.com/somitcoop/erp-research/odoo-helpdesk/-/issues>`_. In
case of trouble, please check there if your issue has already been
reported. If you spotted it first, help us smashing it by providing a
detailed and welcomed feedback.

Do not contact contributors directly about support or help with
technical issues.

*********
 Credits
*********

Authors
=======

-  SomIT SCCL

Contributors
============

-  `SomIT SCCL <https://somit.coop>`_:

      -  Juan Manuel Regalado <juanmanuel.regalado@somit.coop>
      -  Enrico Stano <enrico.stano@somit.coop>
      -  Guillem Alborch <guillem.alborch@somit.coop>

Maintainers
===========

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization
whose mission is to support the collaborative development of Odoo
features and promote its widespread use.

You are welcome to contribute. To learn how please visit
https://odoo-community.org/page/Contribute.
