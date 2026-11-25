# AcmeFlow troubleshooting guide

## Desktop application cannot synchronise

The desktop application shows `SYNC-104` when it cannot establish a secure connection to the AcmeFlow service. The support agent should ask the customer to check whether AcmeFlow works in a browser, confirm that the computer clock is set automatically, and retry on a network without a VPN or HTTPS-inspecting proxy.

If browser access works but the desktop application still shows `SYNC-104`, the customer should sign out of the desktop application, restart it, and sign in again. Reinstalling should be suggested only after these checks.

## Attachment upload errors

The maximum size for one attachment is 25 MB on Starter, 250 MB on Team, and 2 GB on Business. A failed upload with `FILE-413` means the individual file exceeds the plan limit. Compressing or splitting the file is the recommended action.

The error `STORE-507` means the workspace has reached its total attachment-storage limit. Deleting a file does not immediately free storage because deleted attachments remain in trash for 14 days. A workspace owner can permanently empty attachment trash from **Workspace settings → Storage**.

## Invitation errors

The error `MEMBER-403` appears when an invitation would exceed the workspace member limit. On Starter, deactivate an existing member or upgrade the workspace before retrying. A user invited to exactly one project can instead be added as a guest, subject to the guest limit.

An invitation expires after 72 hours. Owners and administrators can revoke an expired invitation and create a new one.

## Browser support

AcmeFlow supports the latest two major versions of Chrome, Edge, Firefox, and Safari. Internet Explorer is not supported. Before escalating a browser-specific display issue, support should ask the customer to disable browser extensions, retry in a private window, and test a supported browser.
