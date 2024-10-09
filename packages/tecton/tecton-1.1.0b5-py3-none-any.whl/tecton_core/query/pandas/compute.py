import inspect
from typing import Optional
from typing import Union

import attrs
import pandas
import pyarrow

from tecton_core import conf
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.pandas.nodes import PandasDataSourceScanNode
from tecton_core.query.query_tree_compute import ComputeMonitor
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.query.query_tree_compute import logger
from tecton_core.schema import Schema
from tecton_core.secrets import SecretResolver
from tecton_core.specs import PandasBatchSourceSpec


@attrs.frozen
class PandasCompute(SQLCompute):
    @staticmethod
    def from_context() -> "PandasCompute":
        return PandasCompute()

    def run_sql(
        self,
        sql_string: str,
        return_dataframe: bool = False,
        expected_output_schema: Optional[Schema] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> Optional[pyarrow.RecordBatchReader]:
        msg = "Use DuckDBCompute directly"
        raise NotImplementedError(msg)

    def get_dialect(self) -> Dialect:
        return Dialect.DUCKDB

    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pandas.DataFrame) -> None:
        msg = "Use DuckDBCompute directly"
        raise NotImplementedError(msg)

    def register_temp_table(
        self, table_name: str, table_or_reader: Union[pyarrow.Table, pyarrow.RecordBatchReader]
    ) -> None:
        msg = "Use DuckDBCompute directly"
        raise NotImplementedError(msg)

    def load_from_data_source(
        self,
        ds: DataSourceScanNode,
        expected_output_schema: Optional[Schema] = None,
        secret_resolver: Optional[SecretResolver] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> pyarrow.RecordBatchReader:
        assert isinstance(ds.ds.batch_source, PandasBatchSourceSpec)

        pandas_node = PandasDataSourceScanNode.from_node_inputs(
            query_node=ds, input_node=None, secret_resolver=secret_resolver
        )

        if monitor:
            try:
                monitor.set_query(inspect.getsource(ds.ds.batch_source.function))
            except OSError:
                pass

        return pandas_node.to_arrow(expected_output_schema=expected_output_schema)

    def run_odfv(
        self, qt_node: NodeRef, input: pyarrow.RecordBatchReader, monitor: Optional[ComputeMonitor] = None
    ) -> pyarrow.RecordBatchReader:
        from tecton_core.query.pandas.translate import pandas_convert_odfv_only

        if conf.get_bool("DUCKDB_DEBUG"):
            logger.warning(f"Input dataframe to ODFV execution: {input.schema}")

        pandas_node = pandas_convert_odfv_only(qt_node, input)
        # ToDo: extract code from pandas_node and send it to monitor
        df = pandas_node.to_arrow()
        return df
