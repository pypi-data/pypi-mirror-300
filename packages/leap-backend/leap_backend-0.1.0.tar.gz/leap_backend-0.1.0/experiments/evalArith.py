#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Author: Hanyu Wang
Created time: 2024-07-04 23:30:46
Last Modified by: Hanyu Wang
Last Modified time: 2024-07-05 01:26:53
"""

import argparse

parser = argparse.ArgumentParser(description="Evaluate the delay arithmetic circuits.")
parser.add_argument("-t", "--unit_type", type=str, help="unit type", default="adder")
parser.add_argument("-n", "--num_stages", type=int, help="number of stages", default=1)
parser.add_argument(
    "-f", "--force", type=bool, help="if force to overwrite the output directory"
)


def pipeline(n_stages):
    reg_names = [f"out_{i}" for i in range(n_stages)]
    pipeline = "\n\t\t".join(
        [f"{reg_names[i]} <= {reg_names[i-1]};" for i in range(1, n_stages)]
    )

    return f"""
    reg [31:0] {", ".join(reg_names)};
    always @(posedge clk) begin
        {pipeline}
    end
    assign out = {reg_names[-1]};
    """


def unit(unit_type):
    assert unit_type in ["adder", "multiplier", "modulo", "divider"]
    op = None
    if unit_type == "adder":
        op = "+"
    elif unit_type == "multiplier":
        op = "*"
    elif unit_type == "modulo":
        op = "%"
    elif unit_type == "divider":
        op = "/"

    return f"""
    always @(*) begin
        out_0 <= a {op} b;
    end
    """


def run(n_stages, unit_type):
    # generate the verilog file with a single adder
    assert n_stages >= 1

    import os

    tmpDir = "./tmp"
    verilogFile = f"{tmpDir}/{unit_type}.v"
    yosysDir = os.path.join(tmpDir, "yosys")
    vtrDir = os.path.join(tmpDir, "vtr")
    blifFile = os.path.join(yosysDir, f"{unit_type}.mapped.blif")
    blifFile1 = os.path.join(yosysDir, f"{unit_type}.retimed.blif")

    if not os.path.exists(tmpDir):
        os.makedirs(tmpDir)

    with open(verilogFile, "w") as f:
        f.write(
            f"""
module {unit_type}(
    input wire clk,
    input wire [31:0] a,
    input wire [31:0] b,
    output wire [31:0] out
);
    {pipeline(n_stages)}
    {unit(unit_type)}
endmodule
        """
        )

    # # run sv2blif to generate the blif file
    # os.system(f"python ./scripts/sv2blif.py -i {verilogFile} -o {yosysDir} -f 1 -v 1")

    # # run blif2pnr to generate the pnr result
    # os.system(f"python ./scripts/blif2pnr.py -i {blifFile} -o {vtrDir} -f 1 -v 1")
    # os.system(f"python ./scripts/blif2pnr.py -i {blifFile1} -o {vtrDir} -f 1 -v 1")


if __name__ == "__main__":
    args = parser.parse_args()

    run(args.num_stages, args.unit_type)
