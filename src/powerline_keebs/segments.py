# -*- coding: utf-8 -*-

import os
import re
import subprocess
from enum import Enum
from sys import platform

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info


class SegmentColorscheme(Enum):
    """Colorscheme configuration for the segment sections."""

    DIVIDER_HIGHLIGHT_GROUP = "keebs:divider"
    """Sections divider's background and foreground colors."""

    DEFAULT_HIGHLIGHT_GROUP = "keebs"
    """Icon and divider's background and foreground colors."""


class SegmentContent(Enum):
    """Default values for segment's sections."""

    KEEBS_ICON = u'\U00002328'
    """Default icon for segment."""


class SegmentVisibility(Enum):
    """Environment variable names for toggling segment visibility."""

    SHOW_SEGMENT = "POWERLINE_KEEBS_SHOW"
    """Toggle entire segment visibility by setting the value to either 1 (show) or 0 (hide)."""


@requires_segment_info
class KeebsSegment(Segment):
    """Constructs the segment's sections with the configured colorscheme and visibility options applied."""

    @staticmethod
    def detect_kbs(pl):
        if "linux" in platform:
            device_pattern = \
                b"Bus\\s+(?P<bus>\\d+)\\s+Device\\s+(?P<device>\\d+).+ID\\s(?P<id>\\w+:\\w+)\\s(?P<tag>.+)$"
            device_re = re.compile(device_pattern, re.I)
            devices = subprocess.check_output(
                "lsusb -v 2>/dev/null | egrep '(^Bus|Keyboard)' | grep -B1 Keyboard",
                shell=True
            )

            result = []
            for device in devices.split(b'\n'):
                if device:
                    match = device_re.match(device)
                    if match:
                        device_info = match.groupdict()
                        keeb = str(device_info['tag']).replace('b\'', '').replace('\'', '')
                        result.append(keeb)

            return result
        elif "darwin" in platform:
            # collect all connected device names as no further information about device type is available
            devices = subprocess.check_output(
                """
                system_profiler SPUSBDataType | egrep -B 2 -A 6 'Product ID' | sed 's/^--/#/'\
                    | egrep ':$' | sed -e 's/^ *//g' -e 's/ *:$//g'
                """,
                shell=True
            )

            result = []
            for device in devices.split(b'\n'):
                if device:
                    keeb = str(device).replace('b\'', '').replace('\'', '')
                    result.append(keeb)

            # filter out obvious false positives
            filtered = filter(
                lambda k: "hub" not in str(k).lower() and "mouse" not in str(k).lower() and "usb" not in str(k).lower(),
                result
            )

            return list(filtered)
        else:
            pl.debug("Unsupported platform: " + platform)
            return []

    @staticmethod
    def filter_dongles(kbs: list):
        filtered = filter(lambda k: "receiver" not in str(k).lower() and "dongle" not in str(k).lower(), kbs)
        return list(filtered)

    def __call__(self, pl, no_dongles=False, **kwargs):
        pl.debug('Running powerline-keebs...')

        sections = []
        show_segment = os.getenv(SegmentVisibility.SHOW_SEGMENT.value)
        if show_segment is None:
            pass
        elif int(show_segment) == 0:
            return sections

        self.no_dongles = no_dongles
        detected_keebs = self.filter_dongles(self.detect_kbs(pl)) if self.no_dongles else self.detect_kbs(pl)
        if detected_keebs is None:
            return sections

        sections.append({
            'contents': f'{SegmentContent.KEEBS_ICON.value}  ',
            'highlight_groups': [SegmentColorscheme.DEFAULT_HIGHLIGHT_GROUP.value],
            'divider_highlight_group': SegmentColorscheme.DIVIDER_HIGHLIGHT_GROUP.value,
        })

        kbs = f' {SegmentContent.KEEBS_ICON.value}  '.join(detected_keebs)
        sections.append({
            'contents': kbs,
            'highlight_groups': [SegmentColorscheme.DEFAULT_HIGHLIGHT_GROUP.value],
            'divider_highlight_group': SegmentColorscheme.DIVIDER_HIGHLIGHT_GROUP.value,
        })

        return sections


keebs = with_docstring(KeebsSegment(), """Return a list of currently connected keyboards.

Supports devices connected through a USB hub. Dongles or wireless receivers can be filtered out optionally.

Divider highlight group used: ``keebs:divider``.

Highlight groups used: ``keebs``.
""")
"""Custom segment entry point."""
