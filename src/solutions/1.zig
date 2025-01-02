const std = @import("std");

const common = @import("../common.zig");
const Part = common.Part;
const Solution = common.Solution;

pub fn solve(input: []const u8, part: Part, allocator: std.mem.Allocator, solution: *Solution) !void {
    try solution.split("Iterate over each line forwards and backwards");

    var input_iter = std.mem.splitScalar(u8, input, '\n');

    while (input_iter.next()) |line| {
        var c11: u8 = undefined;
        var c12: u8 = undefined;
        var c21: u8 = undefined;
        var c22: u8 = undefined;

        if (part == Part.One or part == Part.Both) {
            for (0..line.len) |i| {
                if (matchSlice(line[i..], "#")) {
                    c11 = line[i];
                    break;
                }
            }
        }

        if (part == Part.Two or part == Part.Both) {
            const masks = [_][]const u8{ "#", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" };
            var first_ind: usize = std.math.maxInt(usize);
            for (0..line.len) |i| {
                for (masks, 0..) |mask, j| {
                    if (matchSlice(line[i..], mask)) {
                        if (i <= first_ind) {
                            first_ind = i;
                            if (j > 0) {
                                c21 = (try std.fmt.allocPrint(allocator, "{d}", .{j}))[0];
                            } else {
                                c21 = line[i];
                            }
                        }
                    }
                }
            }
        }

        var rev = std.ArrayList(u8).init(allocator);
        var rev_iter = std.mem.reverseIterator(line);
        while (rev_iter.next()) |c| {
            try rev.append(c);
        }
        const reversed_line = try rev.toOwnedSlice();

        if (part == Part.One or part == Part.Both) {
            for (0..reversed_line.len) |i| {
                if (matchSlice(reversed_line[i..], "#")) {
                    c12 = reversed_line[i];
                    break;
                }
            }

            solution.add(Part.One, try std.fmt.parseInt(u8, &[2]u8{ c11, c12 }, 10));
        }

        if (part == Part.Two or part == Part.Both) {
            const masks = [_][]const u8{ "#", "eno", "owt", "eerht", "ruof", "evif", "xis", "neves", "thgie", "enin" };
            var first_ind: usize = std.math.maxInt(usize);
            for (0..reversed_line.len) |i| {
                for (masks, 0..) |mask, j| {
                    if (matchSlice(reversed_line[i..], mask)) {
                        if (i <= first_ind) {
                            first_ind = i;
                            if (j > 0) {
                                c22 = (try std.fmt.allocPrint(allocator, "{d}", .{j}))[0];
                            } else {
                                c22 = reversed_line[i];
                            }
                        }
                    }
                }
            }

            solution.add(Part.Two, try std.fmt.parseInt(u8, &[2]u8{ c21, c22 }, 10));
        }
    }
}

fn matchSlice(string: []const u8, mask: []const u8) bool {
    if (string.len < mask.len) return false;

    for (mask, 0..) |m, i| {
        if (!matchChar(string[i], m)) return false;
    }
    return true;
}
fn isDigit(c: u8) bool {
    return (c >= '0' and c <= '9');
}
fn matchChar(c: u8, mask: u8) bool {
    if (mask == '#') {
        return isDigit(c);
    } else {
        return c == mask;
    }
}
