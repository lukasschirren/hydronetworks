"""Functions for calculating stream order."""

import heapq


def strahler(arc_index, direction_node_id, network, nodes):
    """
    This function is nearly verbatim from Gleyzer2004 algorithm
    But excludes the code to create river segments
    """

    up_stream_orders = []
    if len(nodes[direction_node_id]) == 1:
        network[arc_index][7] = 1
    else:
        for arc in nodes[direction_node_id]:
            if network[arc][0] != arc_index:
                if network[arc][5] != direction_node_id:
                    up_stream_orders.append(
                        strahler(arc, network[arc][5], network, nodes)
                    )
                else:
                    up_stream_orders.append(
                        strahler(arc, network[arc][6], network, nodes)
                    )
        max_order = 0
        max_order_count = 0
        for order in up_stream_orders:
            if order > max_order:
                max_order = order
                max_order_count = 1
            elif order == max_order:
                max_order_count += 1
        if max_order_count > 1:
            network[arc_index][7] = max_order + 1
        else:
            network[arc_index][7] = max_order

    return network[arc_index][7]




def shreve_iterative(sink, network, nodes):
    """
    Calculate Shreve stream order iteratively instead of recursively.
    This ensures that a downstream river is always higher.
    """

    stack = [(sink, network[sink][5])]
    visited = set()
    orders = {}

    while stack:
        arc_index, direction_node_id = stack.pop()

        if (arc_index, direction_node_id) in visited:
            continue

        visited.add((arc_index, direction_node_id))
        up_stream_orders = []

        if len(nodes[direction_node_id]) == 5:
            network[arc_index][7] = 1
            orders[arc_index] = 1
        else:
            all_upstream_resolved = True
            for index, arc in enumerate(nodes[direction_node_id]):
                if index >= 4:
                    if network[arc][0] != arc_index:
                        next_node_id = network[arc][5] if network[arc][5] != direction_node_id else network[arc][6]
                        if next_node_id in orders:
                            up_stream_orders.append(orders[next_node_id])
                        else:
                            all_upstream_resolved = False
                            stack.append((arc_index, direction_node_id))
                            stack.append((arc, next_node_id))

            if all_upstream_resolved:
                max_orders = heapq.nlargest(2, up_stream_orders)
                if len(max_orders) == 2:
                    order = 0 + max_orders[0] + max_orders[1]
                else:
                    order = 0 + max(up_stream_orders)
                network[arc_index][7] = order
                orders[arc_index] = order

    return network[sink][7]


def shreve(arc_index, direction_node_id, network, nodes):
    """
    Caclulate Shreve stream order instead of Strahler
    This ensures that a downstream river is always higher
    """

    up_stream_orders = []
    if len(nodes[direction_node_id]) == 5:
        network[arc_index][7] = 1
    else:
        for index, arc in enumerate(nodes[direction_node_id]):
            if index >= 4:
                if network[arc][0] != arc_index:
                    if network[arc][5] != direction_node_id:
                        up_stream_orders.append(
                            shreve(arc, network[arc][5], network, nodes)
                        )
                    else:
                        up_stream_orders.append(
                            shreve(arc, network[arc][6], network, nodes)
                        )

        max_orders = heapq.nlargest(2, up_stream_orders)
        if len(max_orders) == 2:
            order = 0 + max_orders[0] + max_orders[1]
        else:
            order = 0 + max(up_stream_orders)
        network[arc_index][7] = order

    return network[arc_index][7]
