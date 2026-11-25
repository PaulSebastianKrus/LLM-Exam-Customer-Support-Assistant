# AcmeFlow workspace and data guide

## Deleted workspaces

When an owner deletes a workspace, AcmeFlow places it in a 7-day recovery period. During this period, only the original workspace owner can request restoration. Support must verify the workspace ID and owner email, then escalate the restoration request to Data Operations.

After the 7-day recovery period, workspace content is permanently deleted from active systems and cannot be restored by support. Encrypted disaster-recovery backups expire within 30 additional days and are not used for individual customer restorations.

## Deleted projects and tasks

Deleted projects remain in the workspace trash for 30 days and can be restored by a workspace owner or administrator. Deleted tasks remain in project trash for 14 days and can be restored by any project administrator.

Archived projects are not deleted. Owners and administrators can restore an archived project without contacting support.

## Workspace export

Workspace owners on Team and Business plans can request a ZIP export from **Workspace settings → Data → Export workspace**. Exports contain task data in JSON format and file attachments in their original formats.

Starter workspaces can export one project at a time as CSV. Comments, automation history, and attachments are not included in a Starter CSV export.

An export link normally appears within 24 hours and remains valid for 48 hours. Support should escalate when an export has remained in the `Preparing` state for more than 24 hours.

## Account deletion

Deleting a personal account does not automatically delete workspaces owned by that account. The user must transfer or delete each owned workspace before deleting the account. Personal account deletion becomes permanent after a 72-hour cancellation period.
