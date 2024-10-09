import numpy as np
import pandas as pd
import networkx as nx
from swmm_api import read_inp_file, read_out_file
from swmm_api.input_file.macros import inp_to_graph
from swmm_api.output_file import VARIABLES as swmm_vars
from swmm_api.output_file import OBJECTS as swmm_objs
import logging

logger = logging.getLogger("routing")


class Router:
    def __init__(self, g_network=None, df_flows=None):
        self.g_network = g_network
        self.df_flows = df_flows
        return

    def get_flows_from_outfile(self, path_out, start=None, end=None):
        with read_out_file(path_out) as out:
            # import outfile as dataframe
            flows = out.get_part(kind=swmm_objs.LINK, variable=swmm_vars.LINK.VELOCITY)
        self.df_flows = flows[start:end]
        logger.info(f"Flows read from {path_out}")
        return

    def get_network_from_inpfile(self, path_inp):
        inp = read_inp_file(path_inp)
        self.g_network = inp_to_graph(inp)
        logger.info(f"Network read from {path_inp}")
        return

    def generate_empty_routingtable(self, target=None):
        """
        creates an empty table from the topologically ordered nodes of the input graph
        Args:
            graph (NetworkX.DiGraph): input graph, hydraulic network
            target (str): outlet / target node of the hydraulic network

        Returns:
            pd.DataFrame: table for hydraulic routing of packages
        """
        graph = self.g_network
        if target is not None:
            graph = graph.subgraph(list(nx.ancestors(graph, target)) + [target])
        columns = list(nx.topological_sort(graph))
        df_routing = pd.DataFrame(columns=columns)
        logger.info(f"Routing table from {target} with {len(columns)} columns created")
        return df_routing

    def from_seeding_table(self, seeding_table, target):
        """
        Uses a seeding table and a target to generate a routing table by copying only
        columns from seeding table that are in the target catchment to the routing table.
        Args:
            seeding_table: table with seeds for routing table
            target (str): node / catchment outlet

        Returns:
            routing_table: routing table
        """
        rt0 = self.generate_empty_routingtable(target)
        # Reindex df2 to match the columns of df1, filling missing columns with NaN
        seeding_table = seeding_table.reindex(columns=rt0.columns)
        # Concatenate df1 and df2_reindexed
        rt0 = pd.concat([rt0, seeding_table], ignore_index=True)
        return rt0


    @staticmethod
    def from_old_routingtable(rtable):
        """
        creates a routing table from an old routing table
        Args:
            graph (NetworkX.DiGraph): input graph, hydraulic network
            target (str): outlet / target node of the hydraulic network

        Returns:
            pd.DataFrame: table for hydraulic routing of packages
        """

        def keep_last_non_nan(row):
            # Drop all NaN values and keep the last element if the row is not entirely NaN
            if row.last_valid_index() is not None:
                # Create a series of NaNs with the same index as the row
                new_row = pd.Series(np.nan, index=row.index)
                # Keep the last non-NaN value
                new_row[row.last_valid_index()] = row[row.last_valid_index()]
                return new_row
            return row

        new_table = rtable.copy()
        # drop all packets that were routed to the end so that they're not routed again
        last_col = rtable.columns[-1]
        new_table = new_table[pd.isna(new_table[last_col])]
        new_table.apply(keep_last_non_nan, axis=1)
        return new_table

    @staticmethod
    def interpolate_on_dtindex(time, dtseries):
        return np.interp(time.to_numpy(), dtseries.index, dtseries.values, left=np.nan, right=np.nan)

    @staticmethod
    def route_packet(start_time, length, edge_velocities):
        try:
            velocity = Router.interpolate_on_dtindex(start_time, edge_velocities)
            if velocity == 0.0:
                # find first non-zero value in series, delay transport to next non-zero time
                start_time = edge_velocities[start_time:].ne(0).idxmax()
                velocity = edge_velocities[start_time]
            elif velocity is np.nan:
                # return nan if requested start time is not within edge velocities index
                return np.nan
            end_time = start_time + pd.to_timedelta(length / velocity, unit="s")
        except:
            return np.nan
        return end_time

    def route_table(self, routing_table, export=False):
        df = routing_table
        for node in df.columns[:-1]:
            succ_node = list(self.g_network.successors(node))[0]
            succ_edge, succ_length = self.g_network.edges[node, succ_node]["obj"].get(("name", "length"))
            # apply routing to each packet
            df.loc[df[node].notnull(), succ_node] = (df.loc[df[node].notnull(), node].
                                                     apply(self.route_packet,
                                                           args=(succ_length, self.df_flows[succ_edge])))
        if export:
            df.to_parquet(export)
        return df


def main():
    inp_path = r"../sample_data/sample_model.inp"
    router = Router(inp_path)
    pass


if __name__ == "__main__":
    main()
    pass
