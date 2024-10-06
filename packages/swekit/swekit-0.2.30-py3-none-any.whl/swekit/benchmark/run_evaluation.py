import datetime
import json
import os
import random
import time
import typing as t
from pathlib import Path

from pydantic import BaseModel, Field
from swebench.harness.test_spec import make_test_spec
from tqdm import tqdm

from composio import Action, WorkspaceConfigType, WorkspaceFactory, WorkspaceType
from composio.utils.logging import WithLogger

from composio_crewai import ComposioToolSet

from swekit.benchmark.utils import (
    build_issue_description,
    get_issues_dataset,
    get_score,
    setup_workspace,
)
from swekit.config.constants import LOCAL_CACHE_DIRECTORY_NAME, LOGS_DIR
from swekit.config.store import IssueConfig


def _get_logs_dir() -> Path:
    """Logs dir factory."""
    return (
        Path.home()
        / LOCAL_CACHE_DIRECTORY_NAME
        / LOGS_DIR
        / (
            str(int(datetime.datetime.now().timestamp()))
            + str(random.randint(1000, 9999))
        )
    )


class EvaluationConfig(BaseModel):
    """Benchmark evaluation config."""

    test_range: str = Field(
        default="20:30",
        description="slice for the test split range",
    )
    dry_run: bool = Field(
        default=False,
        description="dry-run will only print short issue description",
    )
    include_hints: bool = Field(
        default=False,
    )
    logs_dir: Path = Field(
        default_factory=_get_logs_dir,
        description="Logs directory",
    )
    generate_report: bool = Field(
        default=True,
        description="generate evaluation report after running evaluation",
    )
    test_instance_ids: t.List[str] = Field(
        default=[],
        description="test instance ids",
    )
    workspace_type: t.Type[WorkspaceConfigType] = Field(
        default=WorkspaceType.Docker,
        description="workspace environment",
    )
    image_name: t.Optional[str] = Field(
        default=None,
        description="image name",
    )
    num_instances: int = Field(
        default=1,
        description="number of instances to run",
    )


class EvaluationManager(WithLogger):
    """Benchmark evaluation manager."""

    def __init__(self, config: EvaluationConfig):
        """Initialize evaluation manager."""
        super().__init__()

        self.issues = get_issues_dataset(
            test_split=config.test_range,
            test_instance_ids=config.test_instance_ids,
        )
        self.dry_run = config.dry_run
        self.include_hints = config.include_hints
        self.logs_dir = os.path.expanduser(config.logs_dir)
        self.repo_to_workspace_map = {}
        self.repo_to_image_id_map = {}
        self.image_name = config.image_name
        self.num_instances = config.num_instances
        self.workspace_env = config.workspace_type
        logs_dir = Path(config.logs_dir)
        if not logs_dir.exists():
            logs_dir.mkdir(parents=True)

    def get_issue_config(self, issue) -> IssueConfig:
        issue_description = build_issue_description(
            issue["repo"],
            issue["hints_text"],
            issue["problem_statement"],
            self.include_hints,
        )
        test_spec = make_test_spec(issue)
        eval_script = test_spec.eval_script
        test_command = eval_script.splitlines()[-2]

        return IssueConfig(
            repo_name=issue["repo"],
            issue_id=issue["instance_id"],
            base_commit_id=issue["base_commit"],
            issue_desc=issue_description,
            test_command=test_command,
            eval_script=eval_script,
            install_repo_script=test_spec.install_repo_script,
        )

    def get_patch_for_issue(self, workspace_id: str, issue):
        composio_toolset = ComposioToolSet(workspace_id=workspace_id)
        self.logger.info(
            f"Agent run finished, getting patch for issue: {issue['instance_id']}"
        )
        get_patch_resp = composio_toolset.execute_action(
            action=Action.FILETOOL_GIT_PATCH,
            params={},
        )
        self.logger.info(f"Get patch response: {get_patch_resp}")
        if not get_patch_resp.get("successfull", False):
            error_message = get_patch_resp.get("error")
            if error_message:
                raise Exception(f"Error in get_patch: {error_message}")
            else:
                raise Exception("Unknown error occurred in get_patch")

        patch_data = get_patch_resp.get("data", {})
        if not patch_data:
            raise Exception("No data found in the patch response")

        patch = patch_data.get("patch")
        if not patch:
            error = patch_data.get("error")
            if error:
                self.logger.error(f"Error in patch data: {error}")
                return None
            else:
                self.logger.error("No patch found in the response data")
                return None

        self.logger.info(f"Final Patch: {patch}")
        return patch

    def save_agent_run(self, issue_config, issue_patch):
        Path(str(self.logs_dir)).mkdir(parents=True, exist_ok=True)
        task_output_log = f"{self.logs_dir}/agent_logs_{issue_config.issue_id}.json"
        with open(task_output_log, "w", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        issue_config.issue_id: [
                            {
                                "agent_action": "final_patch",
                                "agent_output": issue_patch if issue_patch else "",
                            }
                        ]
                    }
                )
            )

    def show_info_and_exit(self):
        """
        Display information about the evaluation setup and exit.
        """
        info = {
            "Dry Run": self.dry_run,
            "Include Hints": self.include_hints,
            "Logs Directory": str(self.logs_dir),
            "Total Issues": len(self.issues),
            "Test Range": (
                self.issues.num_rows if hasattr(self.issues, "num_rows") else "Unknown"
            ),
            "Dataset Description": (
                self.issues.info.description
                if hasattr(self.issues, "info") and self.issues.info.description
                else "No description available"
            ),
            "Number of Features": (
                len(self.issues.features)
                if hasattr(self.issues, "features")
                else "Unknown"
            ),
            "Features": (
                list(self.issues.features.keys())
                if hasattr(self.issues, "features")
                else "Unknown"
            ),
        }
        print("Evaluation Setup Information:")
        for key, value in info.items():
            print(f"{key}: {value}")

    def run(self, agent_func: t.Callable):
        """
        Main function to load and display entries from the SWE-bench lite dataset.
        """
        if self.dry_run:
            self.show_info_and_exit()
            return

        for count, issue in tqdm(  # type: ignore
            iterable=enumerate(self.issues, 1),
            total=len(self.issues),
            desc="Processing issues",
        ):
            try:
                repo = issue["repo"]
                self.logger.info(
                    f"Processing issue: {count} with repoMap: {self.repo_to_workspace_map} "
                    f"Repo: {repo} "
                    f"Issue id: {issue['instance_id']} "
                )
                tag = repo.replace("/", "-") + "-" + issue["version"].replace(".", "-")
                image_name = self.image_name or f"composio/swe:{tag}"
                self.logger.info(f"Using image: {image_name}")

                for attempt in range(3):
                    try:
                        workspace_ids = setup_workspace(
                            repo,
                            self.repo_to_workspace_map,
                            self.repo_to_image_id_map,
                            issue["base_commit"],
                            self.workspace_env,
                            image_name,
                            num_instances=self.num_instances,
                        )
                        break  # If successful, exit the retry loop
                    except Exception as e:
                        self.logger.error(
                            f"Error setting up workspace (attempt {attempt + 1}/3): {e}"
                        )
                        if attempt < 2:  # If this wasn't the last attempt
                            self.logger.info("Retrying in 5 seconds...")
                            time.sleep(5)  # Wait for 5 seconds before retrying
                        else:
                            self.logger.error(
                                "All attempts to set up workspace failed. Skipping this issue."
                            )
                else:
                    continue  # Skip to the next iteration of the outer loop if all attempts failed
                issue_config = self.get_issue_config(issue)
                self.logger.debug(
                    "found patch-id: %s and install_commit_id: %s",
                    issue["patch"],
                    issue["environment_setup_commit"],
                )
                issue_patch = agent_func(workspace_ids, issue_config)
                # issue_patch = self.get_patch_for_issue(workspace_id, issue)
                self.save_agent_run(issue_config, issue_patch)
                for workspace_id in workspace_ids:
                    WorkspaceFactory.close(id=workspace_id)

            except Exception as e:
                self.logger.error(f"Error processing issue {issue['instance_id']}: {e}")
                raise e

    def score_evaluation(self, run_id: str):
        get_score(self.logs_dir, run_id)


def evaluate(
    runnable: t.Callable,
    test_range: str = "20:22",
    workspace_type: t.Type[WorkspaceConfigType] = WorkspaceType.Docker,
    dry_run: bool = True,
    include_hints: bool = True,
    logs_dir: Path = _get_logs_dir(),
    generate_report: bool = True,
    test_instance_ids: t.List[str] = [],
    image_name: t.Optional[str] = None,
    run_id: str = "temp",
    num_instances: int = 1,
) -> None:
    """Evaluate a callable."""
    print("Inside the evaluate function")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    manager = EvaluationManager(
        EvaluationConfig(
            test_range=test_range,
            dry_run=dry_run,
            include_hints=include_hints,
            logs_dir=logs_dir,
            generate_report=generate_report,
            test_instance_ids=test_instance_ids,
            workspace_type=workspace_type,
            image_name=image_name,
            num_instances=num_instances,
        )
    )
    manager.run(runnable)
    manager.score_evaluation(run_id)
