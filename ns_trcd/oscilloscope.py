import pyvisa as visa
import numpy as np


class Oscilloscope:
    def __init__(self, resource):
        manager = visa.ResourceManager()
        self._scope = manager.open_resource(resource)
        self._scope.timeout = 1000  # milliseconds

    def cleanup(self):
        self._scope.close()

    ####################################################################################
    # Acquisition Parameters
    ####################################################################################

    def set_hi_res_mode(self):
        self._scope.write("acquire:mode hires")

    def set_single_acquisition_mode(self):
        self._scope.write("acquire:stopafter sequence")

    def set_continuous_acquisition_mode(self):
        self._scope.write("acquire:stopafter runstop")

    def acquisition_start(self):
        self._scope.write("acquire:state run")

    def acquisition_stop(self):
        self._scope.write("acquire:state stop")

    def get_acquisition_state(self):
        return self._scope.query("acquire:state?").lower().strip()

    ####################################################################################
    # Horizontal Parameters
    ####################################################################################

    def set_time_per_div(self, div_time):
        self._scope.write(f"horizontal:main:scale {div_time:.2E}")

    def set_horizontal_position(self, percentage):
        self._scope.write(f"horizontal:position {percentage}")

    def set_horizontal_points(self, points):
        self._scope.write(f"horizontal:resolution {points}")

    def get_time_resolution(self):
        return float(self._scope.query("wfmoutpre:xincr?"))

    ####################################################################################
    # Vertical Parameters
    ####################################################################################

    def set_channel_on(self, channel):
        self._scope.write(f"select:ch{channel} on")

    def set_channel_off(self, channel):
        self._scope.write(f"select:ch{channel} off")

    def set_channels_on(self, channel_list):
        for channel in channel_list:
            self.set_channel_on(channel)

    def set_channels_off(self, channel_list):
        for channel in channel_list:
            self.set_channel_off(channel)

    def set_vertical_scale(self, channel, scale_volts):
        self._scope.write(f"ch{channel}:scale {scale_volts:.4E}")

    def set_vertical_offset(self, channel, offset_volts):
        self._scope.write(f"ch{channel}:offset {offset_volts:.4E}")

    def zero_vertical_position(self, channel):
        self._scope.write(f"ch{channel}:position 0")

    def zero_vertical_positions(self, channel_list):
        for channel in channel_list:
            self.zero_vertical_position(channel)

    def zero_all_vertical_positions(self):
        for i in range(1, 5):
            self.zero_vertical_position(i)

    def vertically_center_channel(self, channel):
        avg = self.measure_channel_mean(channel)
        self.set_vertical_offset(channel, avg)

    def get_voltage_scale_factor(self):
        return float(self._scope.query("wfmoutpre:ymult?"))

    def get_vertical_offset_dig_levels(self):
        return int(self._scope.query("wfmoutpre:yoff?"))

    def get_vertical_offset_volts(self):
        return float(self._scope.query("wfmoutpre:yzero?"))

    ####################################################################################
    # Measurements
    ####################################################################################

    def turn_off_all_measurements(self):
        for i in range(1, 9):
            self._scope.write(f"measurement:meas{i}:state off")

    def add_displayed_mean_measurement(self, channel, meas_num):
        self._scope.write(f"measurement:meas{meas_num}:source ch{channel}")
        self._scope.write(f"measurement:meas{meas_num}:state on")
        self._scope.write(f"measurement:meas{meas_num}:type mean")

    def add_displayed_max_measurement(self, channel, meas_num):
        self._scope.write(f"measurement:meas{meas_num}:source ch{channel}")
        self._scope.write(f"measurement:meas{meas_num}:state on")
        self._scope.write(f"measurement:meas{meas_num}:type high")

    def add_displayed_min_measurement(self, channel, meas_num):
        self._scope.write(f"measurement:meas{meas_num}:source ch{channel}")
        self._scope.write(f"measurement:meas{meas_num}:state on")
        self._scope.write(f"measurement:meas{meas_num}:type low")

    def get_displayed_measurement_value(self, meas_num):
        return float(self._scope.query(f"measurement:meas{meas_num}:value?"))

    def add_immediate_mean_measurement(self, channel):
        self._scope.write(f"measurement:immed:source ch{channel}")
        self._scope.write("measurement:immed:type mean")

    def add_immediate_max_measurement(self, channel):
        self._scope.write(f"measurement:immed:source ch{channel}")
        self._scope.write("measurement:immed:type high")

    def add_immediate_min_measurement(self, channel):
        self._scope.write(f"measurement:immed:source ch{channel}")
        self._scope.write("measurement:immed:type low")

    def get_immediate_measurement_value(self):
        return float(self._scope.write("measurement:immed:value?"))

    def measure_channel_mean(self, channel):
        self.add_immediate_mean_measurement(channel)
        self.set_scope_to_run()
        self.wait_while_arming()
        self.wait_until_triggered()
        return float(self.get_immediate_measurement_value())

    #################################################
    # Output waveform parameters
    #################################################

    def set_waveform_encoding_ascii(self):
        self._scope.write("data:encdg ascii")

    def set_waveform_encoding_unsigned_le_binary(self):
        self._scope.write("data:encdg srpbinary")

    def set_waveform_encoding_signed_le_binary(self):
        self._scope.write("data:encdg sribinary")

    def set_waveform_encoding_unsigned_be_binary(self):
        self._scope.write("data:encdg rpbinary")

    def set_waveform_encoding_signed_be_binary(self):
        self._scope.write("data:encdg ribinary")

    def get_waveform_encoding(self):
        return self._scope.query("wfmoutpre:encdg?").lower().strip()

    def get_waveform_length(self):
        return int(self._scope.query("wfmoutpre:nr_pt?"))

    ####################################################################################
    # Obtaining Waveforms
    ####################################################################################

    def set_waveform_data_source_single_channel(self, channel):
        self._scope.write(f"data:source ch{channel}")

    def set_waveform_data_source_multiple_channels(self, channel_list):
        channels = ", ".join([f"ch{x}" for x in channel_list])
        self._scope.write(f"data:source {channels}")

    def set_waveform_start_point(self, point):
        self._scope.write(f"data:start {point}")

    def set_waveform_stop_point(self, point):
        self._scope.write(f"data:stop {point}")

    def get_curve(self):
        return self._scope.query_ascii_values("curve?", container=np.array)

    def retrieve_waveform(self):
        value_list = self._scope.query_ascii_values("curve?", delay=0.5)
        array = np.array(value_list)
        y_scale_factor = self.get_waveform_voltage_scale_factor()
        y_offset_volts = self.get_waveform_vertical_offset_volts()
        scaled_data = array * y_scale_factor + y_offset_volts
        return scaled_data

    ####################################################################################
    # Triggering
    ####################################################################################

    def set_trigger_source(self, channel):
        self._scope.write(f"trigger:a:edge:source ch{channel}")

    def trigger_from_line(self):
        self._scope.write("trigger:a:edge:source line")

    def trigger_on_rising_edge(self):
        self._scope.write("trigger:a:edge:slope rise")

    def trigger_on_falling_edge(self):
        self._scope.write("trigger:a:edge:slope fall")

    def set_trigger_level(self, volts):
        self._scope.write(f"trigger:a:level {volts}")

    def get_trigger_state(self):
        return self._scope.query("trigger:state?").lower().strip()

    def wait_until_triggered(self):
        while self.get_trigger_state() != "save":
            pass
