import logging

from fastapi import FastAPI

logger = logging.getLogger(__name__)


def setting_otlp(
    app: FastAPI,
    app_name: str,
    endpoint: str,
) -> None:
    try:
        from opentelemetry import trace  # type: ignore[import-not-found]
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (  # type: ignore[import-not-found]
            OTLPSpanExporter,
        )
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # type: ignore[import-not-found]
        from opentelemetry.instrumentation.logging import LoggingInstrumentor  # type: ignore[import-not-found]
        from opentelemetry.instrumentation.requests import RequestsInstrumentor  # type: ignore[import-not-found]
        from opentelemetry.sdk.resources import Resource  # type: ignore[import-not-found]
        from opentelemetry.sdk.trace import TracerProvider  # type: ignore[import-not-found]
        from opentelemetry.sdk.trace.export import BatchSpanProcessor  # type: ignore[import-not-found]
    except ImportError:
        logger.warning('OpenTelemetry is not installed. Skipping OpenTelemetry setup.')
        return

    # Setting OpenTelemetry
    # set the service name to show in traces
    resource = Resource.create(
        attributes={
            'service.name': app_name,
            'compose_service': app_name,
        },
    )

    # set the tracer provider
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)

    tracer.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    LoggingInstrumentor().instrument(set_logging_format=True)
    RequestsInstrumentor().instrument(tracer_provider=tracer)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
