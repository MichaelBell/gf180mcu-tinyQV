#!/usr/bin/env python3

import os
import sys

import librelane
from librelane.container import run_in_container
from librelane.flows import Flow


sources = ["project.v", 
         "tinyQV/cpu/tinyqv.v",
         "tinyQV/cpu/alu.v",
         "tinyQV/cpu/buffer.v",
         "tinyQV/cpu/core.v",
         "tinyQV/cpu/counter.v",
         "tinyQV/cpu/cpu.v",
         "tinyQV/cpu/decode.v",
         "tinyQV/cpu/mem_ctrl.v",
         "tinyQV/cpu/qspi_ctrl.v",
         "tinyQV/cpu/register.v",
         "tinyQV/cpu/time.v",
         "tinyQV/cpu/latch_reg.v",
         "tinyQV/peri/uart/uart_tx.v",
         "tinyQV/peri/uart/uart_rx.v",
         "tinyQV/peri/spi/spi.v",
         "tinyQV/peri/pwm/pwm.v"
]

if __name__ == '__main__':

    PDK_ROOT = os.getenv('PDK_ROOT')
    PDK = 'gf180mcuD'

    if "--no-container" not in sys.argv:
        container_image = f"ghcr.io/librelane/librelane:{librelane.__version__}"
        extended_argv = sys.argv + ["--no-container"]
        tty = True
        run_in_container(
            container_image,
            extended_argv,
            pdk_root=PDK_ROOT,
            other_mounts=(),
            tty=tty)
        exit()

    sources = [f"dir::src/{i}" for i in sources]

    flow_cfg = {
        "PL_TARGET_DENSITY_PCT": 71,
        "CLOCK_PERIOD": 24,
        "RUN_LINTER": True,
        "LINTER_INCLUDE_PDK_MODELS": True,
        "CLOCK_PORT": "clk",
        "RUN_KLAYOUT_XOR": False,
        "RUN_KLAYOUT_DRC": False,
        "DESIGN_REPAIR_BUFFER_OUTPUT_PORTS": False,
        "TOP_MARGIN_MULT": 1,
        "BOTTOM_MARGIN_MULT": 1,
        "LEFT_MARGIN_MULT": 6,
        "RIGHT_MARGIN_MULT": 6,
        "FP_SIZING": "absolute",
        "GRT_ALLOW_CONGESTION": True,
        "FP_IO_HLENGTH": 2,
        "FP_IO_VLENGTH": 2,
        "FP_PDN_HPITCH": 28.00,
        "FP_PDN_VPITCH": 28.00,
        "RUN_CTS": True,
        "FP_PDN_CORE_RING": True,
        "FP_PDN_MULTILAYER": True,
        "FP_PDN_CORE_RING_VWIDTH": 5,
        "FP_PDN_CORE_RING_HWIDTH": 5,
        "FP_PDN_CORE_RING_VOFFSET": 3,
        "FP_PDN_CORE_RING_HOFFSET": 3,
        "FP_PDN_CORE_RING_VSPACING": 2,
        "FP_PDN_CORE_RING_HSPACING": 2,
        "RT_MAX_LAYER": "Metal5",
        "MAGIC_DEF_LABELS": False,
        "MAGIC_WRITE_LEF_PINONLY": True,
        "DESIGN_NAME": "tt_um_MichaelBell_tinyQV",
        "VERILOG_FILES": sources,
        "DIE_AREA": [0, 0, 530.00, 530.00],
        "CORE_AREA": [20.00, 20.00, 510.00, 510.00],
        "FP_PIN_ORDER_CFG": "dir::pin_order.cfg",
        "FALLBACK_SDC_FILE": "dir::base.sdc",
        "SYNTH_LATCH_MAP": "dir::latch_map.v",
    }

    Classic = Flow.factory.get("Classic")
    flow = Classic(flow_cfg, design_dir=".", pdk_root=PDK_ROOT, pdk=PDK)

    flow.start(tag="test", overwrite=True)

