from typing import Any

from sqlalchemy.orm import Session

from app.libs import datasets as m
from tests.utils.utils import random_lower_string


class TestImportDatasetPaths:
    def test_import_dataset_paths(self, mocker: Any, tmp_path: Any) -> None:
        input_path = tmp_path
        m.settings.SHARED_DATA_DIR = str(tmp_path)
        (tmp_path / "images").mkdir()
        (tmp_path / "pred").mkdir()
        p = m.ImportDatasetPaths(input_path, random_lower_string())
        assert p.pred_dir == str(input_path / "pred")
        assert p.asset_dir == str(input_path / "images")
        assert p.gt_dir is None


class TestIsFinishedDataset:
    def test_finished_dataset(self, db: Session, mocker: Any) -> None:
        dataset_info = {"related_task": {"state": m.TaskState.done.value}}
        assert m.is_finished_dataset(dataset_info)
        dataset_info = {"related_task": {"state": m.TaskState.error.value}}
        assert m.is_finished_dataset(dataset_info)
        dataset_info = {"related_task": {"state": m.TaskState.terminate.value}}
        assert m.is_finished_dataset(dataset_info)

    def test_not_finished_dataset(self, db: Session, mocker: Any) -> None:
        dataset_info = {"related_task": {"state": m.TaskState.running.value}}
        assert not m.is_finished_dataset(dataset_info)
        dataset_info = {"related_task": {"state": m.TaskState.pending.value}}
        assert not m.is_finished_dataset(dataset_info)
        dataset_info = {"related_task": {"state": m.TaskState.unknown.value}}
        assert not m.is_finished_dataset(dataset_info)
