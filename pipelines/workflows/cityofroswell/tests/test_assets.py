from unittest.mock import Mock, patch
from dagster import build_op_context
from ..assets import get_csv_from_gcs

def test_get_csv_from_gcs():
    """Test that get_csv_from_gcs correctly retrieves and returns blob content."""
    # Arrange
    # Create mock blob with expected properties
    mock_blob = Mock()
    mock_blob.name = "observations/2025-05-22.csv"
    mock_blob.generation = "12345"
    mock_blob.download_as_text.return_value = "timestamp,value\n2025-05-22T12:00:00Z,42.0"

    # Create mock bucket that returns our blob
    mock_bucket = Mock()
    mock_bucket.blob.return_value = mock_blob
    mock_bucket.name = "roswellbubbler_dev"

    # Create mock GCS client that returns our bucket
    mock_client = Mock()
    mock_client.bucket.return_value = mock_bucket

    # Create mock GCS resource that returns our client
    mock_gcs_resource = Mock()
    mock_gcs_resource.get_client.return_value = mock_client

    # Create context with partition key and resource
    context = build_op_context(
        resources={"gcs_roswell": mock_gcs_resource},
        partition_key="observations/2025-05-22.csv"
    )

    # Act
    result = get_csv_from_gcs(context)

    # Assert
    # Check that we got the expected content back
    assert result == "timestamp,value\n2025-05-22T12:00:00Z,42.0"

    # Verify the correct chain of calls was made
    # mock_gcs_resource.get_client.assert_called_once()
    # mock_client.bucket.assert_called_once_with("roswellbubbler_dev")
    # mock_bucket.blob.assert_called_once_with("observations/2025-05-22.csv")
    # mock_blob.download_as_text.assert_called_once()

    # Verify logging and metadata
    # context.log.info.assert_any_call(
    #     "Fetching blobs from gs://%s/%s",
    #     "roswellbubbler_dev",
    #     "observations/2025-05-22.csv"
    # )
    # context.add_output_metadata.assert_called_once_with({"gcs_generation": "12345"})

    