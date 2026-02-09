from src.mgt.transform.data_dictionary import to_data_dictionary_rows
from src.mgt.scanning.sqlalchemy_scanner import ColumnMeta

def test_transform_to_dictionary_rows():
    cols = [
        ColumnMeta(
            database_name="db",
            schema_name="s",
            object_name="t",
            object_type="TABLE",
            column_name="c",
            data_type="TEXT",
            nullable="Y",
        )
    ]
    rows = list(to_data_dictionary_rows(cols, system_name="local"))
    assert rows[0]["object_name"] == "t"
    assert rows[0]["column_name"] == "c"
