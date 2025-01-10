const std = @import("std");

const common = @import("../common.zig");
const Part = common.Part;
const Solution = common.Solution;

const Graph = std.AutoHashMap(u16, std.ArrayList(u16));

fn ingestData(input: []const u8, allocator: std.mem.Allocator) !Graph {
    var output = Graph.init(allocator);
    var vertex_list = std.AutoArrayHashMap([3]u8, void).init(allocator);
    var split_input = std.mem.splitScalar(u8, input, '\n');

    while (split_input.next()) |line| {
        var line_split = std.mem.splitSequence(u8, line, ": ");
        const vertex_name = line_split.next() orelse unreachable;
        try vertex_list.put(vertex_name[0..3].*, {});
    }

    split_input.reset();
    while (split_input.next()) |line| {
        var line_split = std.mem.splitSequence(u8, line, ": ");
        const vertex_name = (line_split.next() orelse unreachable)[0..3].*;
        const edges_part = line_split.next() orelse unreachable;
        var edges = std.ArrayList(u16).init(allocator);
        var edges_iter = std.mem.splitScalar(u8, edges_part, ' ');
        while (edges_iter.next()) |edge| {
            const edge_name = edge[0..3].*;
            try vertex_list.put(edge_name, {});
            try edges.append(@as(u16, @intCast(vertex_list.getIndex(edge_name) orelse unreachable)));
        }

        try output.put(@as(u16, @intCast(vertex_list.getIndex(vertex_name) orelse unreachable)), edges);
    }

    //and again to make edges symmetric
    split_input.reset();
    while (split_input.next()) |line| {
        var line_split = std.mem.splitSequence(u8, line, ": ");
        const vertex_name = (line_split.next() orelse unreachable)[0..3].*;
        const vertex_index = @as(u16, @intCast(vertex_list.getIndex(vertex_name) orelse unreachable));
        const edges_part = line_split.next() orelse unreachable;
        var i: usize = 0;
        var edges_iter = std.mem.splitScalar(u8, edges_part, ' ');
        while (edges_iter.next()) |edge| : (i += 1) {
            const edge_index = @as(u16, @intCast(vertex_list.getIndex(edge[0..3].*) orelse unreachable));
            const res = try output.getOrPut(edge_index);
            if (!res.found_existing) {
                res.value_ptr.* = std.ArrayList(u16).init(allocator);
            }

            try output.getPtr(edge_index).?.append(vertex_index);
        }
    }

    return output;
}

fn enumerate_components(graph: *const Graph, exceptions: *const std.AutoHashMap([2]u16, void), allocator: std.mem.Allocator) !std.AutoHashMap(u16, void) {
    var output = std.AutoHashMap(u16, void).init(allocator);
    var burned = std.AutoHashMap(u16, void).init(allocator);

    var iter = graph.keyIterator();
    while (iter.next()) |v| {
        if (!burned.contains(v.*)) {
            var queue = std.AutoArrayHashMap(u16, void).init(allocator);
            try queue.put(v.*, {});
            var component_count: u16 = 0;
            var current_vertex = queue.pop().key;

            while (true) {
                component_count += 1;
                try burned.put(current_vertex, {});

                for ((graph.get(current_vertex) orelse unreachable).items) |e| {
                    if (!burned.contains(e) and !exceptions.contains([2]u16{ current_vertex, e }) and !exceptions.contains([2]u16{ e, current_vertex })) {
                        try queue.put(e, {});
                    }
                }

                const next = queue.popOrNull();
                if (next == null) {
                    break;
                } else {
                    current_vertex = next.?.key;
                }
            }

            try output.put(component_count, {});
        }
    }
    return output;
}

fn getRandomEdge(graph: *const Graph, r: *std.rand.DefaultPrng) [2]u16 {
    const n = @as(u16, @intCast(graph.count()));
    const v: u16 = @mod(r.random().int(u16), n);
    const edges = graph.get(v) orelse unreachable;
    const num_edges = edges.items.len;
    const e = edges.items[@mod(r.random().int(u16), num_edges)];

    return [2]u16{ v, e };
}

fn findSplittingEdgeSet(graph: *const Graph, magic_number: u16, allocator: std.mem.Allocator) !std.AutoHashMap([2]u16, void) {
    var rand = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));

    while (true) {
        var splitting_edges = std.AutoHashMap([2]u16, void).init(allocator);
        for (0..magic_number) |_| {
            const random_edge = getRandomEdge(graph, &rand);
            try splitting_edges.put(random_edge, {});
        }

        const components = try enumerate_components(graph, &splitting_edges, allocator);

        if (components.count() == 2) {
            var iter = components.keyIterator();
            while (iter.next()) |size| {
                if (size.* <= 100) { //magic_number
                    break;
                }
            } else {
                return splitting_edges;
            }
        }
    }
}

fn reduceSplittingEdgeSet(graph: *const Graph, splitting_edges: *std.AutoHashMap([2]u16, void), allocator: std.mem.Allocator) !?u64 {
    var rand = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));

    const original_components = try enumerate_components(graph, splitting_edges, allocator);
    try std.testing.expectEqual(original_components.count(), 2);

    //1. convert hashset to slice
    const size = splitting_edges.count();
    var edges_slice = try allocator.alloc([2]u16, size);
    var iter = splitting_edges.keyIterator();
    var i: u16 = 0;
    while (iter.next()) |key| : (i += 1) {
        edges_slice[i] = key.*;
    }

    //2. shuffle and pare down
    rand.random().shuffle([2]u16, edges_slice);

    const new_size: u32 = size * 8 / 10;

    edges_slice = edges_slice[0..new_size];

    //3. reconstitute in a hashset
    var candidate_set = std.AutoHashMap([2]u16, void).init(allocator);
    for (edges_slice) |edge| {
        try candidate_set.put(edge, {});
    }

    //4. check if it still splits
    const components = try enumerate_components(graph, &candidate_set, allocator);

    if (components.count() == 2) {
        var components_iter = components.keyIterator();
        var output: u64 = 1;
        while (components_iter.next()) |component_size| {
            if (component_size.* <= 3) {
                return null;
            }
            output *= component_size.*;
        } else {
            splitting_edges.* = candidate_set;
            return output;
        }
    } else {
        return null;
    }
}

pub fn solve(input: []const u8, _: Part, allocator: std.mem.Allocator, solution: *Solution) !void {
    try solution.split("Read in the input");

    const graph = try ingestData(input, allocator);

    while (true) {
        try solution.split("Find a superset of the three critical edges...");

        var splitting_edges = try findSplittingEdgeSet(&graph, 250, allocator);

        try solution.split("Try to pare down the superset...");

        for (0..50) |_| {
            const output = try reduceSplittingEdgeSet(&graph, &splitting_edges, allocator);

            if (splitting_edges.count() == 3) {
                if (output == null) {
                    continue;
                }
                solution.set(Part.One, output.?);
                return;
            }
        }
    }
}
