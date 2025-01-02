const std = @import("std");

pub const Part = enum { One, Two, Both };

pub const Solver = fn (input: []const u8, part: Part, allocator: std.mem.Allocator, solution: *Solution) anyerror!void;

pub const Frame = struct { message: []const u8, time: u64 };

pub const SolutionType = union(enum) {
    Integer: u64,
    String: []const u8,

    pub fn toString(self: SolutionType, allocator: std.mem.Allocator) ![]const u8 {
        switch (self) {
            .Integer => |*value| return try std.fmt.allocPrint(allocator, "{d}", .{value.*}),
            .String => |*value| return value.*,
        }
    }

    pub fn compareSolutionByType(self: SolutionType, expected: SolutionType) bool {
        switch (self) {
            .Integer => |ai| switch (expected) {
                .Integer => |ei| return (ai == ei),
                .String => unreachable,
            },
            .String => |as| switch (expected) {
                .String => |es| return std.mem.eql(u8, as, es),
                .Integer => unreachable,
            },
        }
    }
};

pub const Solution = struct {
    part_one: ?SolutionType,
    part_two: ?SolutionType,
    frames: std.ArrayList(Frame),
    timer: std.time.Timer,

    pub fn init(allocator: std.mem.Allocator) !Solution {
        var frames = std.ArrayList(Frame).init(allocator);

        try frames.append(.{ .message = "Start timer", .time = 0 });

        return Solution{
            .part_one = null,
            .part_two = null,
            .frames = frames,
            .timer = try std.time.Timer.start(),
        };
    }

    pub fn split(self: *Solution, message: []const u8) !void {
        try self.frames.append(.{ .message = message, .time = self.timer.read() });
    }

    pub fn stopTheClock(self: *Solution) !void {
        try self.frames.append(.{ .message = "Stop Timer", .time = self.timer.read() });
    }

    pub fn set(self: *Solution, part: Part, value: anytype) void {
        const typeInfo = @typeInfo(@TypeOf(value));
        switch (part) {
            Part.One => {
                switch (typeInfo) {
                    .Int => {
                        if (typeInfo.Int.bits <= 64 and typeInfo.Int.signedness == std.builtin.Signedness.unsigned) {
                            self.part_one = SolutionType{ .Integer = @as(u64, value) };
                        } else {
                            unreachable;
                        }
                    },
                    .ComptimeInt => {
                        self.part_one = SolutionType{ .Integer = @as(u64, value) };
                    },
                    .Pointer => {
                        self.part_one = SolutionType{ .String = value };
                    },
                    else => {
                        unreachable;
                    },
                }
            },
            Part.Two => {
                switch (typeInfo) {
                    .Int => {
                        if (typeInfo.Int.bits <= 64 and typeInfo.Int.signedness == std.builtin.Signedness.unsigned) {
                            self.part_two = SolutionType{ .Integer = @as(u64, value) };
                        } else {
                            unreachable;
                        }
                    },
                    .ComptimeInt => {
                        self.part_two = SolutionType{ .Integer = @as(u64, value) };
                    },
                    .Pointer => {
                        self.part_two = SolutionType{ .String = value };
                    },
                    else => {
                        unreachable;
                    },
                }
            },
            else => unreachable,
        }
    }

    pub fn add(self: *Solution, part: Part, value: anytype) void {
        const typeInfo = @typeInfo(@TypeOf(value));
        switch (part) {
            Part.One => {
                switch (typeInfo) {
                    .Int => {
                        if (typeInfo.Int.bits <= 64 and typeInfo.Int.signedness == std.builtin.Signedness.unsigned) {
                            if (self.part_one == null) {
                                self.part_one = SolutionType{ .Integer = @as(u64, value) };
                            } else {
                                self.part_one.?.Integer += value;
                            }
                        } else {
                            unreachable;
                        }
                    },
                    .ComptimeInt => {
                        if (self.part_one == null) {
                            self.part_one = SolutionType{ .Integer = @as(u64, value) };
                        } else {
                            self.part_one.?.Integer += value;
                        }
                    },
                    else => {
                        std.debug.print("{any}", .{typeInfo});
                        unreachable;
                    },
                }
            },
            Part.Two => {
                switch (typeInfo) {
                    .Int => {
                        if (typeInfo.Int.bits <= 64 and typeInfo.Int.signedness == std.builtin.Signedness.unsigned) {
                            if (self.part_two == null) {
                                self.part_two = SolutionType{ .Integer = @as(u64, value) };
                            } else {
                                self.part_two.?.Integer += value;
                            }
                        } else {
                            unreachable;
                        }
                    },
                    .ComptimeInt => {
                        if (self.part_two == null) {
                            self.part_two = SolutionType{ .Integer = @as(u64, value) };
                        } else {
                            self.part_two.?.Integer += value;
                        }
                    },
                    else => {
                        unreachable;
                    },
                }
            },
            else => unreachable,
        }
    }
};
