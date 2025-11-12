#! /usr/bin/env python

from datetime import datetime
import os

from jmapc import Client, MailboxQueryFilterCondition, Ref
from jmapc.methods import MailboxGet, MailboxGetResponse, MailboxQuery

FASTMAIL_API_HOST = os.environ['FASTMAIL_API_HOST']
FASTMAIL_API_TOKEN = os.environ['FASTMAIL_API_TOKEN']


def hello_world(_):
    """Method takes a single arg: a flask.Request. Since we fire the
    same code regardless of the incoming request, we don't need to
    do anything with this arg!
    """
    hello_fastmail()
    return 'OK'  # like, it's not a web endpoint but let's pretend??

def hello_fastmail():
    client = Client.create_with_api_token(
            host=FASTMAIL_API_HOST, api_token=FASTMAIL_API_TOKEN
    )

    # from https://github.com/smkent/jmapc/blob/main/examples/mailbox.py
    # Prepare two methods to be submitted in one request
    # The first method, Mailbox/query, will locate the ID of the Inbox folder
    # The second method, Mailbox/get, uses a result reference to the preceding
    # Mailbox/query method to retrieve the Inbox mailbox details
    methods = [
        MailboxQuery(filter=MailboxQueryFilterCondition(name="Inbox")),
        MailboxGet(ids=Ref("/ids")),
    ]

    # Call JMAP API with the prepared request
    results = client.request(methods)

    # Retrieve the InvocationResponse for the second method. The InvocationResponse
    # contains the client-provided method ID, and the result data model.
    method_2_result = results[1]

    # Retrieve the result data model from the InvocationResponse instance
    method_2_result_data = method_2_result.response

    # Retrieve the Mailbox data from the result data model
    assert isinstance(
        method_2_result_data, MailboxGetResponse
    ), "Error in Mailbox/get method"
    mailboxes = method_2_result_data.data

    # Although multiple mailboxes may be present in the results, we only expect a
    # single match for our query. Retrieve the first Mailbox from the list.
    mailbox = mailboxes[0]

    # Print some information about the mailbox
    print(f"Found the mailbox named {mailbox.name} with ID {mailbox.id}")
    print(
        f"\tThis mailbox has {mailbox.total_emails} emails, "
        f"{mailbox.unread_emails} of which are unread"
    )

if __name__ == "__main__":
    hello_fastmail()
