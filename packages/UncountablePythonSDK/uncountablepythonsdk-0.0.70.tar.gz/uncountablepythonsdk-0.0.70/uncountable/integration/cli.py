import argparse

from opentelemetry.trace import get_current_span

from uncountable.core.async_batch import AsyncBatchProcessor
from uncountable.integration.construct_client import construct_uncountable_client
from uncountable.integration.executors.executors import execute_job
from uncountable.integration.job import CronJobArguments
from uncountable.integration.scan_profiles import load_profiles
from uncountable.integration.telemetry import JobLogger, Logger
from uncountable.types import job_definition_t


def main() -> None:
    logger = Logger(get_current_span())

    profiles = load_profiles()

    parser = argparse.ArgumentParser(
        description="Process a job with a given command and job ID."
    )

    parser.add_argument(
        "command",
        type=str,
        choices=["run"],
        help="The command to execute (e.g., 'run')",
    )

    parser.add_argument("job_id", type=str, help="The ID of the job to process")

    args = parser.parse_args()

    with logger.push_scope(args.command):
        if args.command == "run":
            job_result: job_definition_t.JobResult | None = None
            for profile in profiles:
                for job in profile.definition.jobs:
                    if job.id == args.job_id:
                        profile_meta = job_definition_t.ProfileMetadata(
                            name=profile.name,
                            base_url=profile.definition.base_url,
                            auth_retrieval=profile.definition.auth_retrieval,
                            client_options=profile.definition.client_options,
                        )
                        job_logger = JobLogger(
                            base_span=logger.current_span,
                            profile_metadata=profile_meta,
                            job_definition=job,
                        )
                        client = construct_uncountable_client(
                            profile_meta=profile_meta, job_logger=job_logger
                        )
                        batch_processor = AsyncBatchProcessor(client=client)
                        job_args = CronJobArguments(
                            job_definition=job,
                            profile_metadata=profile_meta,
                            client=client,
                            batch_processor=batch_processor,
                            logger=job_logger,
                            payload=None,
                        )
                        job_result = execute_job(
                            job_definition=job,
                            profile_metadata=profile_meta,
                            args=job_args,
                        )
                        break
            if job_result is None:
                raise Exception(f"no such job id {args.job_id}")
        else:
            parser.print_usage()


main()
