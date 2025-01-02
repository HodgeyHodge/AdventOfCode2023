const std = @import("std");

const common = @import("../common.zig");
const Part = common.Part;
const Solution = common.Solution;

pub fn solve(args: struct { min: u8, max: u8 }) (fn ([]const u8, part: Part, allocator: std.mem.Allocator, solution: *Solution) anyerror!void) {
    const CurriedSolver = struct {
        fn solve(input: []const u8, part: Part, allocator: std.mem.Allocator, solution: *Solution) !void {
            return innerSolve(input, part, allocator, solution, args.min, args.max);
        }
    };
    return CurriedSolver.solve;
}

fn innerSolve(input: []const u8, part: Part, allocator: std.mem.Allocator, solution: *Solution, comptime min: u8, comptime max: u8) !void {
    try solution.split("Read in the input");

    var data = try Data.init(input, allocator);

    try solution.split("Traverse the graph (two vertices per tile, one per orientation)");

    const total = try data.traverse(min, max, allocator);

    solution.set(part, total);
}

const Orientation = enum { NorthSouth, EastWest };

const Data = struct {
    field: []u4,
    field_transpose: []u4,
    height: usize,
    width: usize,

    fn init(input: []const u8, allocator: std.mem.Allocator) !Data {
        var split_input = std.mem.splitScalar(u8, input, '\n');
        const first_line = split_input.next() orelse unreachable;
        const height = std.mem.count(u8, input, "\n") + 1;
        const width = first_line.len;
        var field = try allocator.alloc(u4, height * width);
        var field_transpose = try allocator.alloc(u4, height * width);
        var i: usize = 1;
        for (first_line, 0..) |c, j| {
            field[j] = @as(u4, @intCast(c - '0'));
            field_transpose[j * height] = @as(u4, @intCast(c - '0'));
        }
        while (split_input.next()) |line| : (i += 1) {
            for (line, 0..) |c, j| {
                field[i * width + j] = @as(u4, @intCast(c - '0'));
                field_transpose[j * height + i] = @as(u4, @intCast(c - '0'));
            }
        }

        return Data{
            .field = field,
            .field_transpose = field_transpose,
            .height = height,
            .width = width,
        };
    }

    fn traverse(self: *const Data, min: u8, max: u8, allocator: std.mem.Allocator) !u64 {
        var vertices_ns_adjacent = std.AutoHashMap(usize, void).init(allocator);
        var vertices_ew_adjacent = std.AutoHashMap(usize, void).init(allocator);
        var vertices_ns_cost = try allocator.alloc(u16, self.height * self.width);
        var vertices_ew_cost = try allocator.alloc(u16, self.height * self.width);

        for (0..self.width * self.height) |i| {
            vertices_ns_cost[i] = std.math.maxInt(u16);
            vertices_ew_cost[i] = std.math.maxInt(u16);
        }

        var current_i: usize = 0;
        var current_j: usize = 0;
        var current_orientation = Orientation.NorthSouth;

        vertices_ns_cost[0] = 0;
        vertices_ew_cost[0] = 0;

        try vertices_ew_adjacent.put(0, {});

        while (true) {
            const current_index = current_i * self.width + current_j;

            switch (current_orientation) {
                Orientation.EastWest => {
                    _ = vertices_ew_adjacent.remove(current_index);

                    //East
                    {
                        var cost: u8 = 0;
                        for (1..max + 1) |j| {
                            if (current_j + j >= self.width) break;

                            cost += self.field[current_index + j];
                            if (j >= min and vertices_ew_cost[current_index] + cost < vertices_ns_cost[current_index + j]) {
                                vertices_ns_cost[current_index + j] = vertices_ew_cost[current_index] + cost;
                                try vertices_ns_adjacent.put(current_index + j, {});
                            }
                        }
                    }

                    //West
                    {
                        var cost: u8 = 0;
                        for (1..max + 1) |j| {
                            if (current_j < j) break;

                            cost += self.field[current_index - j];
                            if (j >= min and vertices_ew_cost[current_index] + cost < vertices_ns_cost[current_index - j]) {
                                vertices_ns_cost[current_index - j] = vertices_ew_cost[current_index] + cost;
                                try vertices_ns_adjacent.put(current_index - j, {});
                            }
                        }
                    }
                },
                Orientation.NorthSouth => {
                    _ = vertices_ns_adjacent.remove(current_index);

                    //North
                    {
                        var cost: u8 = 0;
                        for (1..max + 1) |i| {
                            if (current_i < i) break;

                            cost += self.field_transpose[current_j * self.height + current_i - i];
                            if (i >= min and vertices_ns_cost[current_index] + cost < vertices_ew_cost[current_index - i * self.width]) {
                                vertices_ew_cost[current_index - i * self.width] = vertices_ns_cost[current_index] + cost;
                                try vertices_ew_adjacent.put(current_index - i * self.width, {});
                            }
                        }
                    }

                    //South
                    {
                        var cost: u8 = 0;
                        for (1..max + 1) |i| {
                            if (current_i + i >= self.height) break;

                            cost += self.field_transpose[current_j * self.height + current_i + i];
                            if (i >= min and vertices_ns_cost[current_index] + cost < vertices_ew_cost[current_index + i * self.width]) {
                                vertices_ew_cost[current_index + i * self.width] = vertices_ns_cost[current_index] + cost;
                                try vertices_ew_adjacent.put(current_index + i * self.width, {});
                            }
                        }
                    }
                },
            }

            var new_index: ?usize = null;
            var new_orientation = Orientation.NorthSouth;

            var ns_iter = vertices_ns_adjacent.keyIterator();
            while (ns_iter.next()) |index| {
                if (new_index == null or (vertices_ns_cost[index.*] < (if (new_orientation == Orientation.NorthSouth) vertices_ns_cost[new_index.?] else vertices_ew_cost[new_index.?]))) {
                    new_index = index.*;
                    new_orientation = Orientation.NorthSouth;
                }
            }

            var ew_iter = vertices_ew_adjacent.keyIterator();
            while (ew_iter.next()) |index| {
                if (new_index == null or (vertices_ew_cost[index.*] < (if (new_orientation == Orientation.NorthSouth) vertices_ns_cost[new_index.?] else vertices_ew_cost[new_index.?]))) {
                    new_index = index.*;
                    new_orientation = Orientation.EastWest;
                }
            }

            if (new_index == null or (if (new_orientation == Orientation.NorthSouth) vertices_ns_cost[new_index.?] else vertices_ew_cost[new_index.?]) == std.math.maxInt(u16)) break;

            current_i = @divFloor(new_index.?, self.width);
            current_j = new_index.? % self.width;
            current_orientation = new_orientation;
        }

        return @as(u64, @min(
            vertices_ns_cost[self.width * self.height - 1],
            vertices_ew_cost[self.width * self.height - 1],
        ));
    }
};
