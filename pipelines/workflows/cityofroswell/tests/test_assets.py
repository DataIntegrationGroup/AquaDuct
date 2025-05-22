from unittest.mock import MagicMock, Mock
from dagster import build_op_context
from ..assets import get_csv_from_gcs

def test_get_csv_from_gcs():
    # Create mock blob
    mock_blob = Mock()
    mock_blob.name = "observations_test_file.csv"
    mock_blob.download_as_text.return_value = "test content"
    mock_blob.updated = "2025-05-21"

    # Create mock bucket
    mock_bucket = Mock()
    mock_bucket.list_blobs.return_value = [mock_blob]

    # Create mock client
    mock_client = Mock()
    mock_client.bucket.return_value = mock_bucket

    # Create mock GCS resource
    mock_gcs = Mock()
    mock_gcs.get_client.return_value = mock_client
    mock_gcs.gcs_bucket = "test-bucket"
    mock_gcs.gcs_prefix = "test-prefix"

    # Build context with mock resource
    context = build_op_context(resources={"gcs": mock_gcs})

    # Run the asset
    result = get_csv_from_gcs(context)

    # Assertions
    assert len(result) == 1
    assert result[0]["name"] == "observations_test_file.csv"
    assert result[0]["content"] == "test content"
    assert result[0]["updated"] == "2025-05-21"

    # Verify mock calls
    mock_client.bucket.assert_called_once_with("test-bucket")
    mock_bucket.list_blobs.assert_called_once_with(prefix="test-prefix")
    mock_blob.download_as_text.assert_called_once()