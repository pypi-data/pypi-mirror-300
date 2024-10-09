from sentry_sdk._types import MYPY
from sentry_sdk.hub import Hub
from sentry_sdk.integrations import Integration
from sentry_sdk.scope import add_global_event_processor
from sentry_sdk.utils import Dsn

import clairview
from clairviewanalytics.request import DEFAULT_HOST
from clairviewanalytics.sentry import CLAIRVIEW_ID_TAG

if MYPY:
    from typing import Optional  # noqa: F401

    from sentry_sdk._types import Event, Hint  # noqa: F401


class ClairViewIntegration(Integration):
    identifier = "clairview-python"
    organization = None  # The Sentry organization, used to send a direct link from ClairView to Sentry
    project_id = None  # The Sentry project id, used to send a direct link from ClairView to Sentry
    prefix = "https://sentry.io/organizations/"  # URL of a hosted sentry instance (default: https://sentry.io/organizations/)

    @staticmethod
    def setup_once():
        @add_global_event_processor
        def processor(event, hint):
            # type: (Event, Optional[Hint]) -> Optional[Event]
            if Hub.current.get_integration(ClairViewIntegration) is not None:
                if event.get("level") != "error":
                    return event

                if event.get("tags", {}).get(CLAIRVIEW_ID_TAG):
                    clairview_distinct_id = event["tags"][CLAIRVIEW_ID_TAG]
                    event["tags"]["ClairView URL"] = f"{clairview.host or DEFAULT_HOST}/person/{clairview_distinct_id}"

                    properties = {
                        "$sentry_event_id": event["event_id"],
                        "$sentry_exception": event["exception"],
                    }

                    if ClairViewIntegration.organization:
                        project_id = ClairViewIntegration.project_id or (
                            not not Hub.current.client.dsn and Dsn(Hub.current.client.dsn).project_id
                        )
                        if project_id:
                            properties["$sentry_url"] = (
                                f"{ClairViewIntegration.prefix}{ClairViewIntegration.organization}/issues/?project={project_id}&query={event['event_id']}"
                            )

                    clairview.capture(clairview_distinct_id, "$exception", properties)

            return event
