# Access requests to restricted files of a record

Functionality allows authenticated users and guests to request access to view the restricted files of a record. Access can be set to expire on a specific date as well as never expiring.


As a record owner, firstly, you need to allow different types of users to create access requests to your record's files:
0. Create a record with restricted files
1. Click on the "Share" button on the record landing page:
![Share button](./img/access_request_share_button.png)
2. Navigate to the "Access requests" tab of the modal:
![Access requests tab](./img/access_requests_tab.png)
3. These are the settings for all access requests in general. 
*  Allow authenticated or/and unauthenticated users to request access to restricted files of your record.
*  Accept conditions. Provide a message that will be visible to the users in the request form (see screenshots below)
*  Set access expiration date. This setting will be applied to all the approved requests, unless you individually set them to a different option on the request page.

4. Save your changes and close the modal
![Access requests tab save](./img/access_requests_tab_save.png)

Now both authenticated and anonymous users are able to **request** view access to your record’s files. You need to approve their request to grant them access to your record's files. The view for different types of users is different.

Here is the flow of a guest user:
1. Open the record with restricted files. See that there is an access request form on the page
![Access requests form guest](./img/access_request_form_guest.png)
2. Read request acceptance conditions in the form, provide your email address and your full name, add a request message. Click on the "Request access" button when done.
![Access requests form filled](./img/access_request_form_filled.png)
3. You will get an email with verification of your email address
![Confirm email modal](./img/confirm_email_modal.png)
4. Click on “Verify e-mail address” link
![Confirm email email](./img/confirm_email_email.png)
5. It will redirect you to the request page. At this point, the request is created and record owner can see it. You can add more comments to your request or cancel it.
![Guest access request view](./img/guest_access_request_view.png)

Now let's take a look at the request page of the record owner.
1. Navigate to "My dashboard" -> "Requests" and click on the title of the record to open the request main page
![Access request requests list](./img/access_request_requests_list.png)
2. Here there is a possibility to accept or decline a request, add a comment and change the access expiration date individually for this person.
![Access request request page guest](./img/access_request_request_page_guest.png)

After accepting the request, Sofia gets notified by email and is now able to access the files!
Guest user request page:
![Guest access request view accepted](./img/guest_access_request_view_accepted.png)
Record landing page:
![Restricted files open to guest](./img/restricted_files_open_to_guest.png)

The flow of an authenticated user is similar, with slightly different UI:
![Access requests form authorized user](./img/access_request_form_authorized.png)
There is no email confirmation, user gets redirected to the request onclick of the "Request access" button:
![Access request request page authorized](./img/access_request_request_page_authorized.png)