using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;

namespace HIWIN_Contest
{
    class HRobot
    {
        // will send message from Hiwin Controller
        public delegate void CallBackFun(UInt16 cmd, UInt16 rlt, ref UInt16 Msg, int len);

        #region HRobot_API

        [DllImport("HRSDK.dll")]
        public static extern int Connect(String a, int mode, CallBackFun func);
        [DllImport("HRSDK.dll")]
        public static extern void Close(int a);
        [DllImport("HRSDK.dll")]
        public static extern int get_HRSDK_version(StringBuilder v);
        [DllImport("HRSDK.dll")]
        public static extern int get_connection_level(int a);

        [DllImport("HRSDK.dll")]
        public static extern int get_timer(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int set_timer(int robot, int index, int value);
        [DllImport("HRSDK.dll")]
        public static extern int get_counter(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int set_counter(int robot, int index, int value);
        [DllImport("HRSDK.dll")]
        public static extern int get_pr_type(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int set_pr_type(int robot, int index, int value);
        [DllImport("HRSDK.dll")]
        public static extern int get_pr_coordinate(int robot, int index, [In, Out] double[] value);
        [DllImport("HRSDK.dll")]
        public static extern int set_pr_coordinate(int robot, int index, double[] value);
        [DllImport("HRSDK.dll")]
        public static extern int get_pr_tool_base(int robot, int index, [In, Out] int[] value);
        [DllImport("HRSDK.dll")]
        public static extern int set_pr_tool_base(int robot, int index, [In] int tool, int _base);
        [DllImport("HRSDK.dll")]
        public static extern int set_pr(int robot, int pr_num, int pr_type, [In, Out] double[] coor, int tool, int _base);

        [DllImport("HRSDK.dll")]
        public static extern int set_acc_dec_ratio(int robot, int v);
        [DllImport("HRSDK.dll")]
        public static extern int get_acc_dec_ratio(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int set_ptp_speed(int robot, int v);
        [DllImport("HRSDK.dll")]
        public static extern int get_ptp_speed(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int set_lin_speed(int robot, double v);
        [DllImport("HRSDK.dll")]
        public static extern double get_lin_speed(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int set_override_ratio(int robot, int v);
        [DllImport("HRSDK.dll")]
        public static extern int get_override_ratio(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int get_alarm_code(int robot, [In, Out] ref int count, [Out] UInt64[] alarm_code);

        [DllImport("HRSDK.dll")]
        public static extern int get_DI(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int get_DO(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int set_DO(int robot, int index, bool On_Off);
        [DllImport("HRSDK.dll")]
        public static extern int get_FI(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int get_FO(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int get_RI(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int get_RO(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int set_RO(int robot, int index, bool On_Off);
        [DllImport("HRSDK.dll")]
        public static extern int get_VO(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int set_VO(int robot, int index, bool On_Off);

        [DllImport("HRSDK.dll")]
        public static extern int get_base_number(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int set_base_number(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int get_base_data(int robot, int index, [In, Out] double[] data);
        [DllImport("HRSDK.dll")]
        public static extern int define_base(int robot, int index, [In] double[] data);
        [DllImport("HRSDK.dll")]
        public static extern int get_tool_number(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int set_tool_number(int robot, int index);
        [DllImport("HRSDK.dll")]
        public static extern int get_tool_data(int robot, int index, [In, Out] double[] data);
        [DllImport("HRSDK.dll")]
        public static extern int define_tool(int robot, int index, [In] double[] data);

        [DllImport("HRSDK.dll")]
        public static extern int ext_task_start(int robot, int mode, int select);
        [DllImport("HRSDK.dll")]
        public static extern int task_start(int robot, string name);
        [DllImport("HRSDK.dll")]
        public static extern int task_hold(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int task_abort(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int task_continue(int robot);

        [DllImport("HRSDK.dll")]
        public static extern int set_motor_state(int robot, int onOff);
        [DllImport("HRSDK.dll")]
        public static extern int get_motor_state(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int get_speed_limit_state(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int speed_limit_on(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int speed_limit_off(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int clear_alarm(int robot);


        [DllImport("HRSDK.dll")]
        public static extern int jog(int robot, int type, int index, int dir);
        [DllImport("HRSDK.dll")]
        public static extern int jog_stop(int robot);


        [DllImport("HRSDK.dll")]
        public static extern int ptp_axis(int robot, int mode, double[] point);
        [DllImport("HRSDK.dll")]
        public static extern int ptp_pos(int robot, int mode, double[] point);
        [DllImport("HRSDK.dll")]
        public static extern int ptp_rel_pos(int robot, int mode, double[] point);
        [DllImport("HRSDK.dll")]
        public static extern int ptp_rel_axis(int robot, int mode, double[] point);
        [DllImport("HRSDK.dll")]
        public static extern int ptp_pr(int robot, int mode, int point);
        [DllImport("HRSDK.dll")]
        public static extern int lin_axis(int robot, int mode, double smooth_value, double[] point);
        [DllImport("HRSDK.dll")]
        public static extern int lin_pos(int robot, int mode, double smooth_value, double[] point);
        [DllImport("HRSDK.dll")]
        public static extern int lin_rel_pos(int robot, int mode, double smooth_value, double[] point);
        [DllImport("HRSDK.dll")]
        public static extern int lin_rel_axis(int robot, int mode, double smooth_value, double[] point);
        [DllImport("HRSDK.dll")]
        public static extern int lin_pr(int robot, int mode, double smooth_value, int point);
        [DllImport("HRSDK.dll")]
        public static extern int circ_pos(int robot, int mode, double[] point_aux, double[] point_end);
        [DllImport("HRSDK.dll")]
        public static extern int circ_axis(int robot, int mode, double[] point_aux, double[] point_end);
        [DllImport("HRSDK.dll")]
        public static extern int circ_pr(int robot, int mode, int point_aux, int point_end);
        [DllImport("HRSDK.dll")]
        public static extern int get_motion_state(int robot);

        [DllImport("HRSDK.dll")]
        public static extern int motion_hold(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int motion_continue(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int motion_abort(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int motion_delay(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int set_command_id(int robot, int num);
        [DllImport("HRSDK.dll")]
        public static extern int get_command_id(int robot);

        [DllImport("HRSDK.dll")]
        public static extern int get_command_count(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int get_encoder_count(int robot, [In, Out] Int32[] value);
        [DllImport("HRSDK.dll")]
        public static extern int get_current_joint(int robot, [In, Out] double[] value);
        [DllImport("HRSDK.dll")]
        public static extern int get_current_position(int robot, [In, Out] double[] value);
        [DllImport("HRSDK.dll")]
        public static extern int get_current_rpm(int robot, [In, Out] double[] value);
        [DllImport("HRSDK.dll")]
        public static extern int get_device_born_date(int robot, int[] date);
        [DllImport("HRSDK.dll")]
        public static extern int get_operation_time(int robot, [In, Out] int[] value);
        [DllImport("HRSDK.dll")]
        public static extern int get_mileage(int robot, [In, Out] double[] value);
        [DllImport("HRSDK.dll")]
        public static extern int get_total_mileage(int robot, [In, Out] double[] value);
        [DllImport("HRSDK.dll")]
        public static extern int get_utilization(int robot, [In, Out] int[] value);
        [DllImport("HRSDK.dll")]
        public static extern int get_utilization_ratio(int robot);
        [DllImport("HRSDK.dll")]
        public static extern int get_motor_torque(int robot, [In, Out] double[] value);
        [DllImport("HRSDK.dll")]
        public static extern int get_HRSS_version(int robot, StringBuilder value);
        [DllImport("HRSDK.dll")]
        public static extern int get_robot_type(int robot, StringBuilder value);

        #endregion

        public enum Connection_Level
        {
            Monitor,
            Controller,
        };

        public enum operation_mode
        {
            Safety,
            Running,
        };

        public enum space_system_type
        {
            Cart,
            Joint,
            Tool
        };

        public enum space_direction
        {
            positive = 1,
            negative = -1,
        };

        public enum robot_axis
        {
            joint_1,
            joint_2,
            joint_3,
            joint_4,
            joint_5,
            joint_6
        };

        public enum robot_coor
        {
            Cart_x,
            Cart_y,
            Cart_z,
            Cart_a,
            Cart_b,
            Cart_c,
        };

        public enum robot_motion_status
        {
            MS_IDLE = 1,
            MS_RUNNING = 2,
            MS_HOLD = 3,
            MS_DELAY = 4,
            MS_WAIT_CMD = 5
        };
    }
}
