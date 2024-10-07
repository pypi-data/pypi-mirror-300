import json
import traceback

from typing import Optional

from fastapi import Request


def get_span_id(request: Request) -> Optional[str]:
    span_id = None
    trace_context = request.headers.get("X-Cloud-Trace-Context")
    # check the trace context header is in the correct format
    if trace_context:
        # The X-Cloud-Trace-Context header is in the format "TRACE_ID/SPAN_ID;o=TRACE_TRUE"
        # So we split by '/' and take the second part, then split by ';' to remove the trace options
        span_id = trace_context.split("/")[1].split(";")[0]

        # Check that span_id is a 64 bit unsigned integer between 0 and 2^64 - 1
        return span_id

    return None


def format_exception(e: Exception) -> str:
    joined = "".join(traceback.format_exception(e))
    return json.dumps(joined)[1:-1]
