const std = @import("std");
const common = @import("common.zig");

const day1 = @import("solutions/1.zig");
const day17 = @import("solutions/17.zig");

const Frame = common.Frame;
const Part = common.Part;
const Solver = common.Solver;
const SolutionType = common.SolutionType;
const Solution = common.Solution;
const Run = struct {
    day: u8,
    part: Part,
    solver: *const Solver,
    input: []const u8,
    expected: []const SolutionType,
    input_file: []const u8,

    fn init(day: u8, part: Part, input: []const u8, solver: *const Solver, expected: []const SolutionType) Run {
        const input_file = @embedFile(std.fmt.comptimePrint("inputs/{d}/{s}", .{ day, input }));

        return Run{
            .day = day,
            .part = part,
            .input = input,
            .solver = solver,
            .expected = expected,
            .input_file = input_file,
        };
    }

    fn execute(self: *const Run) !void {
        var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
        defer arena.deinit();
        const allocator = arena.allocator();

        std.debug.print("\n==============================================================================================\n", .{});
        std.debug.print("Day {d}{s}: {s}\n", .{ self.day, if (self.part == Part.One) " Part one" else if (self.part == Part.Two) " Part two" else "", self.input });
        std.debug.print("==============================================================================================\n\n", .{});

        var solution = try Solution.init(allocator);
        try self.solver(self.input_file, self.part, allocator, &solution);
        try solution.stopTheClock();

        var prev: Frame = undefined;
        for (solution.frames.items, 0..) |f, i| {
            if (i > 1) {
                std.debug.print("* {s:<78}{s}\n", .{ prev.message, std.fmt.fmtDuration(f.time - prev.time) });
            }
            prev = f;
        }

        std.debug.print("\n", .{});

        if (self.part == Part.Both or self.part == Part.One) {
            if (solution.part_one != null) {
                std.debug.print("Part one result: {s:<63}", .{try solution.part_one.?.toString(allocator)});
                if (self.expected.len > 0) {
                    if (!self.expected[0].compareSolutionByType(solution.part_one.?)) {
                        return error.YaBlewItKid;
                    } else {
                        std.debug.print("correct!\n", .{});
                    }
                } else {
                    std.debug.print("(no expected value given)", .{});
                }
            } else {
                std.debug.print("(no answer submitted for part one)\n", .{});
            }
        }

        if (self.part == Part.Both or self.part == Part.Two) {
            if (solution.part_two != null) {
                std.debug.print("Part two result: {s:<63}", .{try solution.part_two.?.toString(allocator)});
                if ((self.part == Part.Both and self.expected.len < 2) or (self.part == Part.Two and self.expected.len == 0)) {
                    std.debug.print("(no expected value given)", .{});
                } else {
                    if (!(if (self.part == Part.Both) self.expected[1] else self.expected[0]).compareSolutionByType(solution.part_two.?)) {
                        return error.YaBlewItKid;
                    } else {
                        std.debug.print("correct!\n", .{});
                    }
                }
            } else {
                std.debug.print("(no answer submitted for part two)\n", .{});
            }
        }

        std.debug.print("\n{s:<80}{d}\n", .{ "Total time recorded:", std.fmt.fmtDuration(solution.frames.items[solution.frames.items.len - 1].time) });
    }
};

const runs = &[_]Run{
    Run.init(1, Part.One, "test1.txt", day1.solve, &[_]SolutionType{SolutionType{ .Integer = 142 }}),
    Run.init(1, Part.Two, "test2.txt", day1.solve, &[_]SolutionType{SolutionType{ .Integer = 281 }}),
    Run.init(1, Part.Both, "live.txt", day1.solve, &[_]SolutionType{ SolutionType{ .Integer = 53194 }, SolutionType{ .Integer = 54249 } }),

    //TODO: re-write 16 to move directly to corners, not one tile at a time

    Run.init(17, Part.One, "test1.txt", day17.solve(.{ .min = 1, .max = 3 }), &[_]SolutionType{SolutionType{ .Integer = 102 }}),
    Run.init(17, Part.One, "live.txt", day17.solve(.{ .min = 1, .max = 3 }), &[_]SolutionType{SolutionType{ .Integer = 1065 }}),
    Run.init(17, Part.Two, "test1.txt", day17.solve(.{ .min = 4, .max = 10 }), &[_]SolutionType{SolutionType{ .Integer = 94 }}),
    Run.init(17, Part.Two, "test2.txt", day17.solve(.{ .min = 4, .max = 10 }), &[_]SolutionType{SolutionType{ .Integer = 71 }}),
    Run.init(17, Part.Two, "live.txt", day17.solve(.{ .min = 4, .max = 10 }), &[_]SolutionType{SolutionType{ .Integer = 1249 }}),

    //TODO: re-write 21 to address part 2

    //TODO: re-write 22 to use a tree

    //TODO: re-write 23 to traverse the graph sensibly

    //TODO: re-write 24 to address part 2

    //TODO: re-write 25 to find the nodes automatically
};

pub fn main() !void {
    if (std.os.argv.len == 2) {
        const arg: ?u8 = std.fmt.parseInt(u8, std.mem.span(std.os.argv[1]), 10) catch null;
        for (runs) |run| {
            if ((arg != null and run.day == arg.?) or arg == null) {
                try run.execute();
            }
        }
    } else {
        for (runs) |run| {
            try run.execute();
        }
    }
}
