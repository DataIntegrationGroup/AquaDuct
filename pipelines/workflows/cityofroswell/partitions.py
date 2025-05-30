import dagster as dg

file_partitions = dg.DynamicPartitionsDefinition(name="cityofroswell_file_partitions")