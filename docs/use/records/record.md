# Published record

Once you upload a record, it is immediately published and accessible to users. On the record landing page, you will find:

- All relevant **metadata information**.
- A list of **files with integrated previews**.
- Other valuable details like **statistics, versions, or communities**.

## Request access to restricted files

_Introduced in v12_

You can allow authenticated and non-authenticated (guest) users to request access to view the restricted files of a public record. Access can be set to expire on a specific date as well as never expire.

This can be useful for record owners to manage access to restricted files of each record. For unauthorized users, it gives the possibility to request access to the files.

Note: accepted access requests grant to the requestor access to **all** versions of the record.

### Enable access requests

As a record owner, you first need to allow accessing restricted files via a request:

0. Create a record with restricted files

1. Click on the "Share" button on the record landing page:
   ![Share button](../imgs/records/access_request_share_button.png)

2. Navigate to the "Settings" tab of the modal:
   ![Access requests tab](../imgs/records/access_requests_tab.png)

3. Change the settings for the access requests:

   - Allow authenticated or/and unauthenticated users to request access to restricted files of your record.
   - Accept conditions. Provide a message that will be visible to the users in the request form (see screenshot below)
   - Set access expiration date. This setting will be applied by default to all access requests. When reviewing an access request, you can set a different value.

4. Save your changes
   ![Access requests tab save](../imgs/records/access_requests_tab_save.png)

Now both authenticated and anonymous users are able to **request** view access to your record’s files. You need to approve their request to grant them access to your record's files.

### Request access to restricted files

As a user that would like to get access to restricted files of a record, it is necessary to **fill in the request form** appearing in the record landing page. This action creates and submits a new access request: the record's owner will be notified, and the request will appear on their respective dashboards.

### Accepting/Declining the request

The submitter and the record's owner can find the newly created access request in "My dashboard" -> "Requests", and can exchange comments. The record's owner can define a new expiration date (changing the default settings) for this access request, accept or decline it:
![Access request request page guest](../imgs/records/access_request_request_page_guest.png)

After accepting the request, the requestor will receive a notification by e-mail and will be able to access the restricted files:
![Restricted files open to guest](../imgs/records/restricted_files_open_to_guest.png)

## Include in multiple communities

_Introduced in v12_

A record can be **included in multiple communities**. To manage which communities your record is included in, navigate to the **"Communities" menu** on the record's landing page.

![Include record](../imgs/records/include-multiple-communities.jpg)

From there, use the "**Submit to community**" link to select additional communities where you would like your record to be added.

![Include record modal](../imgs/records/include-multiple-communities-modal.jpg)

For a deeper understanding of the high-level architecture behind requests, **refer to the dedicated documentation page** located [here](../../maintenance/architecture/requests.md).
