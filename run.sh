#!/bin/bash

# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: MIT

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

source /opt/intel/openvino/bin/setupvars.sh

# Adding path of libcpu_extension.so to LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$GO_WORK_DIR/common/video/udfs/native/build/ie_cpu_extension

# Adding path of Generic Plugin
export GST_PLUGIN_PATH=$GST_PLUGIN_PATH:"/usr/local/lib/gstreamer-1.0"

if [[ ${RUN_MODE} != "EVA" ]]; then
  python3 -m evas
else
  python3 -m vaserving
fi

