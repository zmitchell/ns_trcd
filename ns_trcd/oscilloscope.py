import pyvisa as visa
import numpy as np


class Oscilloscope:
    def __init__(self):
        manager = visa.ResourceManager()
        self._scope = manager.open_resource('TCPIP::192.168.20.4::gpib0,1::INSTR')
        self._scope.timeout = 1000  # milliseconds
        print(self._scope.query("*IDN?"))

    def _query_scope(self, query):
        raw_resp = self._scope.query(query)
        return raw_resp.strip('\n').lower()

    def send_and_log_command(self, header, argument):
        header = header.lower()
        argument = argument.lower()
        cmd = ' '.join([header, argument])
        self._scope.write(cmd)
        query = header + '?'
        resp = self._query_scope(query)
        return

    ####################################################################################
    # Acquisition Parameters
    ####################################################################################

    def set_acquisition_parameters(self):
        # Sets all of the common parameters at once
        self._scope.write('acquire:mode hires')
        self._scope.write('acquire:stopafter sequence')
        self.set_channels_on([1, 2, 3, 4])
        self.zero_all_vertical_positions()
        # self.set_vertical_scale(1, 20e-03)
        # self.set_vertical_scale(2, 20e-03)
        # self.set_vertical_scale(4, 5.0)
        self.set_time_per_div(40e-6)
        # self.set_horizontal_points(250000)
        # self.set_horizontal_position(10)
        self.set_trigger_source(4)
        self.trigger_on_rising_edge()
        # self.turn_off_all_measurements()
        return

    def set_hi_res_mode(self):
        self._scope.write('acquire:mode hires')
        return

    def set_single_acquisition_mode(self):
        self._scope.write('acquire:stopafter sequence')
        return

    def set_continuous_acquisition_mode(self):
        self._scope.write('acquire:stopafter runstop')
        return

    ######################################################################################
    # Horizontal Parameters
    ######################################################################################

    def set_time_parameters(self):
        # Sets the common parameters all at once
        # these two settings give you 1.6ns resolution
        time_per_div = '40E-06'
        number_of_points = '250000'
        time_div_cmd = 'horizontal:main:scale ' + time_per_div
        num_pts_cmd = 'horizontal:resolution ' + number_of_points
        self._scope.write(time_div_cmd)
        self._scope.write(num_pts_cmd)
        self._scope.write('horizontal:position 10.0000')
        return

    def set_time_per_div(self, div_time):
        time_string = '{:.2E}'.format(div_time)
        cmd = 'horizontal:main:scale {}'.format(time_string)
        self._scope.write(cmd)
        return

    def set_horizontal_position(self, percentage):
        cmd = 'horizontal:position {}'.format(percentage)
        self._scope.write(cmd)
        return

    def set_horizontal_points(self, points):
        cmd = 'horizontal:resolution {}'.format(points)
        self._scope.write(cmd)
        return

    ######################################################################################
    # Vertical Parameters
    ######################################################################################

    def set_channel_on(self, channel):
        cmd = 'select:ch{} on'.format(channel)
        self._scope.write(cmd)
        return

    def set_channel_off(self, channel):
        cmd = 'select:ch{} off'.format(channel)
        self._scope.write(cmd)
        return

    def set_channels_on(self, channel_list):
        for channel in channel_list:
            self.set_channel_on(channel)
        return

    def set_channels_off(self, channel_list):
        for channel in channel_list:
            self.set_channel_off(channel)
        return

    def set_vertical_scale(self, channel, scale_volts):
        scale_string = '{:.4E}'.format(scale_volts)
        cmd = 'ch{}:scale {}'.format(channel, scale_string)
        self._scope.write(cmd)
        return

    def set_vertical_offset(self, channel, offset_volts):
        offset_string = '{:.4E}'.format(offset_volts)
        cmd = 'ch{}:scale {}'.format(channel, offset_string)
        self._scope.write(cmd)
        return

    def zero_vertical_position(self, channel):
        cmd = 'ch{}:position 0'.format(channel)
        self._scope.write(cmd)
        return

    def zero_vertical_positions(self, channel_list):
        for channel in channel_list:
            self.zero_vertical_position(channel)
        return

    def zero_all_vertical_positions(self):
        for i in range(1,5):
            self.zero_vertical_position(i)
        return

    def vertically_center_channel(self, channel):
        avg = self.measure_channel_mean(channel)
        self.set_vertical_offset(channel, avg)
        return

    ######################################################################################
    # Measurements
    ######################################################################################

    def turn_off_all_measurements(self):
        for i in range(1,9):
            cmd = 'measurement:meas{}:state off'.format(i)
            self._scope.write(cmd)
        return

    def add_displayed_mean_measurement(self, channel, meas_num):
        src_cmd = 'measurement:meas{}:source ch{}'.format(meas_num, channel)
        state_cmd = 'measurement:meas{}:state on'.format(meas_num)
        type_cmd = 'measurement:meas{}:type mean'.format(meas_num)
        self._scope.write(src_cmd)
        self._scope.write(state_cmd)
        self._scope.write(type_cmd)
        return

    def add_displayed_max_measurement(self, channel, meas_num):
        src_cmd = 'measurement:meas{}:source ch{}'.format(meas_num, channel)
        state_cmd = 'measurement:meas{}:state on'.format(meas_num)
        type_cmd = 'measurement:meas{}:type high'.format(meas_num)
        self._scope.write(src_cmd)
        self._scope.write(state_cmd)
        self._scope.write(type_cmd)
        return

    def add_displayed_min_measurement(self, channel, meas_num):
        src_cmd = 'measurement:meas{}:source ch{}'.format(meas_num, channel)
        state_cmd = 'measurement:meas{}:state on'.format(meas_num)
        type_cmd = 'measurement:meas{}:type low'.format(meas_num)
        self._scope.write(src_cmd)
        self._scope.write(state_cmd)
        self._scope.write(type_cmd)
        return

    def get_displayed_measurement_value(self, meas_num):
        cmd = 'measurement:meas{}:value?'.format(meas_num)
        resp = self._query_scope(cmd)
        return float(resp)

    def add_immediate_mean_measurement(self, channel):
        src_cmd = 'measurement:immed:source ch{}'.format(channel)
        type_cmd = 'measurement:immed:type mean'
        self._scope.write(src_cmd)
        self._scope.write(type_cmd)
        return

    def add_immediate_max_measurement(self, channel):
        src_cmd = 'measurement:immed:source ch{}'.format(channel)
        type_cmd = 'measurement:immed:type high'
        self._scope.write(src_cmd)
        self._scope.write(type_cmd)
        return

    def add_immediate_min_measurement(self, channel):
        src_cmd = 'measurement:immed:source ch{}'.format(channel)
        type_cmd = 'measurement:immed:type low'
        self._scope.write(src_cmd)
        self._scope.write(type_cmd)
        return

    def get_immediate_measurement_value(self):
        cmd = 'measurement:immed:value?'
        resp = self._query_scope(cmd)
        return float(resp)

    def measure_channel_mean(self, channel):
        # add an immediate measurement
        # wait for the scope to trigger
        # get the value
        # return the value
        self.add_immediate_mean_measurement(channel)
        self.set_scope_to_run()
        self.wait_while_arming()
        self.wait_until_triggered()
        value = self.get_immediate_measurement_value()
        return float(value)

    #################################################
    # Output waveform parameters
    #################################################

    def set_waveform_encoding(self):
        cmd = 'wfmoutpre:encdg asc'
        self._scope.write(cmd)
        return

    def get_waveform_encoding(self):
        cmd = 'wfmoutpre:encdg?'
        resp = scope.write(cmd)
        return resp

    def get_waveform_length(self):
        cmd = 'wfmoutpre:nr_pt?'
        resp = self._query_scope(cmd)
        return int(resp)

    def get_waveform_time_resolution(self):
        cmd = 'wfmoutpre:xincr?'
        resp = self._query_scope(cmd)
        return float(resp)

    def get_waveform_voltage_scale_factor(self):
        cmd = 'wfmoutpre:ymult?'
        resp = self._query_scope(cmd)
        return float(resp)

    def get_waveform_vertical_offset_levels(self):
        cmd = 'wfmoutpre:yoff?'
        resp = self._query_scope(cmd)
        return int(resp)

    def get_waveform_vertical_offset_volts(self):
        cmd = 'wfmoutpre:yzero?'
        resp = self._query_scope(cmd)
        return float(resp)

    ######################################################################################
    # Obtaining Waveforms
    ######################################################################################

    def set_waveform_data_source(self, channel):
        cmd = 'data:source ch{}'.format(channel)
        self._scope.write(cmd)
        return

    def set_waveform_start_point(self, point):
        cmd = 'data:start {}'.format(point)
        self._scope.write(cmd)
        return

    def set_waveform_stop_point(self, point):
        cmd = 'data:stop {}'.format(point)
        self._scope.write(cmd)
        return

    def set_waveform_parameters(self):
        self.set_waveform_encoding()
        self.set_waveform_start_point(1)
        self.set_waveform_stop_point(250000)
        return

    def prepare_channel_for_output(self, channel):
        self.set_waveform_data_source(channel)
        self.set_waveform_parameters()
        return

    def retrieve_waveform(self):
        # length = int(scope.query('horizontal:recordlength?').strip('\n'))
        length = int(self._query_scope('horizontal:recordlength?'))
        value_list = self._scope.query_ascii_values('curve?', delay=0.5)
        array = numpy.array(value_list)
        y_scale_factor = self.get_waveform_voltage_scale_factor()
        y_offset_volts = self.get_waveform_vertical_offset_volts()
        scaled_data = array * y_scale_factor + y_offset_volts
        return scaled_data

    def make_waveform_x_data(self):
        length = self.get_waveform_length()
        points_left_of_zero = int(length/10)
        start_time = -1.6e-09 * points_left_of_zero
        array = numpy.zeros((length))
        for i in range(length):
            array[i] = start_time + i * 1.6e-09
        return array

    def assemble_dataset_for_channels(self, channel_list):
        data_array = numpy.zeros((250000,len(channel_list)+1))
        for i in range(len(channel_list)):
            channel = channel_list[i]
            self.prepare_channel_for_output(channel)
            data_array[:,i+1] = self.retrieve_waveform()
        data_array[:,0] = self.make_waveform_x_data()
        return data_array

    ############################
    ## Triggering
    ############################

    def set_trigger_source(self, channel):
        cmd = 'trigger:a:edge:source ch{}'.format(channel)
        self._scope.write(cmd)
        return

    def trigger_from_line(self):
        cmd = 'trigger:a:edge:source line'
        self._scope.write(cmd)
        return

    def trigger_on_rising_edge(self):
        cmd = 'trigger:a:edge:slope rise'
        self._scope.write(cmd)
        return

    def trigger_on_falling_edge(self):
        cmd = 'trigger:a:edge:slope fall'
        self._scope.write(cmd)
        return

    def set_trigger_level(self, volts):
        # sets the voltage at which a trigger will be registered
        cmd = 'trigger:a:level {}'.format(volts)
        self._scope.write(cmd)
        return

    def set_scope_to_run(self):
        query = 'trigger:state?'
        resp = self._query_scope(query)
        if resp == 'save':
            cmd = 'acq:state run'
            self._scope.write(cmd)
        return

    def get_trigger_state(self):
        query = 'trigger:state?'
        resp = self._query_scope(query)
        return resp

    def wait_while_arming(self):
        clock_start = time.time()
        timeout = 10
        trigger_not_ready = True
        not_timed_out = True
        while trigger_not_ready and not_timed_out:
            trigger_not_ready = (get_trigger_state(scope) != 'ready')
            not_timed_out = (time.time() - clock_start) < timeout
        if (not not_timed_out):
            self.set_scope_to_run()
            self.wait_while_arming()
        return

    def wait_until_triggered(self):
        while self.get_trigger_state() != 'save':
            pass
        return
