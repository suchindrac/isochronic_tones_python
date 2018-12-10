# Generate isochronic tones in Python

## Summary:

This is an attempt to create isochronic tones in python by combining sine wave of base frequency with trapezoidal wave of
 beat frequency.

## Execution:

C:\IsochronicTonesPython\> python gen_isochronic_tones.py

<program> <base freqency> <beat frequency> <sample rate> <output time> <ramp percent> <amplitude>

C:\IsochronicTonesPython\> python gen_isochronic_tones.py 432 10 11029 10 0.15 8000
gen_isochronic_tones.py:168: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
  make_isochronic_wave(beat_freq, ramp_percent, sample_rate, output_time, base_freq, amplitude)

C:\IsochronicTonesPython\>
