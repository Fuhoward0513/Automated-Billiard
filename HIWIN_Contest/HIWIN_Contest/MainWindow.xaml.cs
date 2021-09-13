using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.IO.Ports;
using System.Threading;
using System.IO;

namespace HIWIN_Contest
{
    /// <summary>
    /// MainWindow.xaml 的互動邏輯
    /// </summary>
    /// 

    public partial class MainWindow : Window
    {
        IoT IoT = new IoT();
        LoadFile LF = new LoadFile();
        MotionControl MC = new MotionControl();
        StateMachine SM = new StateMachine();

        private static HRobot.CallBackFun callback;
        private static HRobot.CallBackFun Grippercallback;

        private System.Windows.Forms.Timer timer1;      /* Refresh information, should implement System.Windows.Forms.dlls*/  
        private System.Threading.Thread ThreadRunNC;    /* Loop of program execution */
        private System.Threading.Thread ThreadSM;       /* Waiting for external program command */

        /* The definition of robot status */
        const int STATE_READY = 0x00;
        const int STATE_ALARM_EMERGENCY = 0x01;
        const int STATE_RUNNING_NCFILE = 0x10;

        /* Initialization parameters, CK means check */
        public int device_id;
        public int XEG32_id;

        int ConnectCK = 1;
        int ServoCK = 1;
        int SMCK = 1;
        int RICK = 1;
        int showRobotState = -1;
        int EmgStopCK = 0;      /* No press emergency = 0， press emergency = 1 */
        int RunLoadNCCK = 0;    /* without execution NC code RunLoadNCCK = 0；with excution RunLoadNCCK = 1 */

        /* Constrain the feedrate of the robotic */
        public const int PTP_SPEED_MAX_LIMIT = 100;
        public const int LIN_SPEED_MAX_LIMIT = 200;
        public MainWindow()
        {
            InitializeComponent();

            /* Enable Timer1 */
            timer1 = new System.Windows.Forms.Timer();
            timer1.Interval = 10;
            timer1.Tick += new EventHandler(timer1_Tick);
            timer1.Enabled = true;

            ThreadRunNC = new Thread(FuncRunNC_Loop);
            ThreadRunNC.Start();
        }

        private void btn_Connect_Click(object sender, RoutedEventArgs e)
        {
            if(ConnectCK == 1)
            {
                if (radioBtn_virtual.IsChecked == true)
                    device_id = HRobot.Connect("127.0.0.1", 1, callback);   // Connect to  HRSS
                else if (radioBtn_robotic.IsChecked == true)
                    device_id = HRobot.Connect("192.168.0.4", 1, callback); // Connect to actual Robot

                if (device_id >= 0)
                {
                    showRobotState = 0;
                    Console.WriteLine("Robot connect successful.");
                    callback = new HRobot.CallBackFun(EventFun);

                    /* Enable button */
                    btn_ServoONOFF.IsEnabled = true;
                    btn_Home.IsEnabled = true;
                    btn_LoadFile.IsEnabled = true;
                    btn_RunLoadFile.IsEnabled = true;
                    btn_StateMachine.IsEnabled = true;
                    btn_ClearAlarm.IsEnabled = true;
                    btn_EmgStop.IsEnabled = true;
                    gb_GripperControl.IsEnabled = true;
                    //gb_IOControl.IsEnabled = true;

                    /* */
                    XEG32_id = EG_Control.StartConnect(Convert.ToInt32(TB_XEG32_Port.Text), 32);
                    if(XEG32_id < 100 && EG_Control.DetectConnect() == 0)
                    {
                        Console.WriteLine("XEG32 Gripper connect successful.");
                        Grippercallback = new HRobot.CallBackFun(EventFun);
                    }
                    else
                        Console.WriteLine("XEG32 Gripper connect failure.");
                    
                }
                else
                {
                    Console.WriteLine("Robot connect failure.");
                    return;
                }

                HRobot.set_override_ratio(device_id, 100);   /* override speed ratio */
                btn_Connect.Content = "Disconnect";
                ConnectCK = 0;
            }
            else
            {
                showRobotState = -1;
                HRobot.set_motor_state(device_id, 0);
                HRobot.Close(device_id);
                EG_Control.CloseConnect();

                /* Disenable button */
                btn_ServoONOFF.IsEnabled = false;
                btn_Home.IsEnabled = false;
                btn_LoadFile.IsEnabled = false;
                btn_RunLoadFile.IsEnabled = false;
                btn_StateMachine.IsEnabled = false;
                btn_ClearAlarm.IsEnabled = false;
                btn_EmgStop.IsEnabled = false;
                gb_GripperControl.IsEnabled = false;
                //gb_IOControl.IsEnabled = false;

                btn_Connect.Content = "Connect";
                ConnectCK = 1;
            }
        }

        public static void EventFun(UInt16 cmd, UInt16 rlt, ref UInt16 Msg, int len)
        {
            Console.WriteLine("Command: " + cmd + " Resault: " + rlt);
        }
        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            CloseThread();
        }
        private void CloseThread()
        {
            timer1.Stop();
            //IoT.IoTmainClose();
            if (ThreadRunNC.IsAlive == true) { ThreadRunNC.Abort(); }    /* 終止NC檔案的迴圈 */
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            IoT.Override = HRobot.get_override_ratio(device_id);
            IoT.MotorState = HRobot.get_motor_state(device_id);     // return 0 : servo off, return 1 : servo on, return -1 : faile
            IoT.MotionState = HRobot.get_motion_state(device_id);   // return 1 : Idle, return 2 : motion, return 3 : pause, return 4 : delay, return 5 : wait, return -1 : faile 
            //IoT.SpeedLimitState = HRobot.get_speed_limit_state(device_id);  // return 0 : close, return 1 : open

            HRobot.get_current_joint(device_id, IoT.CurrentJoint);
            HRobot.get_current_position(device_id, IoT.CurrentXYZABC);

            // lbl_ProgOvrd.Content = IoT.Override.ToString();

            lbl_CurJointAxis1.Content = IoT.CurrentJoint[0].ToString("F3");
            lbl_CurJointAxis2.Content = IoT.CurrentJoint[1].ToString("F3");
            lbl_CurJointAxis3.Content = IoT.CurrentJoint[2].ToString("F3");
            lbl_CurJointAxis4.Content = IoT.CurrentJoint[3].ToString("F3");
            lbl_CurJointAxis5.Content = IoT.CurrentJoint[4].ToString("F3");
            lbl_CurJointAxis6.Content = IoT.CurrentJoint[5].ToString("F3");

            lbl_CurPosX.Content = IoT.CurrentXYZABC[0].ToString("F3");
            lbl_CurPosY.Content = IoT.CurrentXYZABC[1].ToString("F3");
            lbl_CurPosZ.Content = IoT.CurrentXYZABC[2].ToString("F3");
            lbl_CurPosA.Content = IoT.CurrentXYZABC[3].ToString("F3");
            lbl_CurPosB.Content = IoT.CurrentXYZABC[4].ToString("F3");
            lbl_CurPosC.Content = IoT.CurrentXYZABC[5].ToString("F3");

            if (showRobotState == -1) { lbl_RobotState.Content = "..."; }
            else if (showRobotState == STATE_READY) { lbl_RobotState.Content = "Ready"; }
            else if (showRobotState == STATE_ALARM_EMERGENCY) { lbl_RobotState.Content = "EMERGENCY STOP"; }
            else if (showRobotState == STATE_RUNNING_NCFILE) { lbl_RobotState.Content = "RUNNING"; }
        }

        private void FuncRunNC_Loop()
        {
            while (true)
            {
                Thread.Sleep(100);
                //Console.Write("Loop\n");
                if (RunLoadNCCK == 1 && EmgStopCK == 0)
                {
                    showRobotState = STATE_RUNNING_NCFILE;
                    //HRobot.speed_limit_off(device_id);              // Turn off robot safe mode (convert to T2)
                    HRobot.set_override_ratio(device_id, 100);
                    for (int i = 0; i < LF.NumofFileLines; i++)
                    {
                        if (EmgStopCK == 1) { i = LF.NumofFileLines; break; }   // if software emergency stop is alives, the program can't be executed.
                        if (LF.LFN[i].Type.Equals("MOVE"))
                        {
                            if (LF.LFN[i].MotionType.Equals("L") && LF.LFN[i].Coordinate == LF.CoordinateWorld)         // LINE (world coordinate)
                            {
                                if (LF.LFN[i].F > LIN_SPEED_MAX_LIMIT) { LF.LFN[i].F = LIN_SPEED_MAX_LIMIT; }
                                HRobot.set_lin_speed(device_id, LF.LFN[i].F);
                                HRobot.lin_pos(device_id, 0, 0, LF.LFN[i].buf);
                                //Console.Write("LINPOS\n");
                            }
                            else if (LF.LFN[i].MotionType.Equals("L") && LF.LFN[i].Coordinate == LF.CoordinateJoint)     // LINE (joint coordinate)
                            {
                                if (LF.LFN[i].F > LIN_SPEED_MAX_LIMIT) { LF.LFN[i].F = LIN_SPEED_MAX_LIMIT; }
                                HRobot.set_lin_speed(device_id, LF.LFN[i].F);
                                HRobot.lin_axis(device_id, 0, 0, LF.LFN[i].buf);
                                //Console.Write("LINAXIS\n");
                            }
                            else if (LF.LFN[i].MotionType.Equals("J") && LF.LFN[i].Coordinate == LF.CoordinateWorld)    // PTP (world coordinate)
                            {
                                if (LF.LFN[i].F > PTP_SPEED_MAX_LIMIT) { LF.LFN[i].F = PTP_SPEED_MAX_LIMIT; }
                                HRobot.set_ptp_speed(device_id, LF.LFN[i].F);
                                HRobot.ptp_pos(device_id, 0, LF.LFN[i].buf);
                                //Console.Write("PTPPOS\n");
                            }
                            else if (LF.LFN[i].MotionType.Equals("J") && LF.LFN[i].Coordinate == LF.CoordinateJoint)    // PTP (joint coordinate)
                            {
                                if (LF.LFN[i].F > PTP_SPEED_MAX_LIMIT) { LF.LFN[i].F = PTP_SPEED_MAX_LIMIT; }
                                HRobot.set_ptp_speed(device_id, LF.LFN[i].F);
                                HRobot.ptp_axis(device_id, 0, LF.LFN[i].buf);
                                //Console.Write("PTPAXIS\n");
                            }

                            while (true)    /* Wait for the end of the line segment command */
                            {
                                int State = HRobot.get_motion_state(device_id);
                                Thread.Sleep(100);
                                //Console.WriteLine(State);                               
                                if (State == 1) { break; }
                                /*
                                else if (EmgStopCK == 1 || RunLoadNCCK == 0)    // software emergency stop enable or without execution NC code 
                                {
                                    i = LF.NumofFileLines;
                                    HRobot.motion_abort(device_id);
                                    break;
                                }
                                else if (HRobot.get_RI(device_id, 1) == 1 && RICK == 1)     // 給智慧分類的功能收到外部訊號就停止 
                                {
                                    RICK = 0;
                                    i = LF.NumofFileLines;
                                    HRobot.motion_abort(device_id);
                                    break;
                                }
                                else if (HRobot.get_RI(device_id, 1) == 0 && RICK == 0)
                                {
                                    RICK = 1;
                                }
                                */
                            }
                        }
                        else if (LF.LFN[i].Type.Equals("GRIP"))     /* this function for RobotIQ gripper */
                        {
                            // RIQG.SendGripperCmd((uint)LF.LFN[i].GripPos, (uint)LF.LFN[i].GripVel, (uint)LF.LFN[i].GripForce, LF.LFN[i].GripDelay);
                        }
                        else if (LF.LFN[i].Type.Equals("IO"))       /* control */
                        {
                            // for (int IOidx = 1; IOidx <= 3; IOidx++) { HRobot.set_robot_output(device_id, IOidx, false); }

                            if (LF.LFN[i].IOTF == 0)
                            {
                                int state = HRobot.set_DO(device_id, LF.LFN[i].IONum, false);
                                Console.WriteLine(HRobot.get_DO(17, 0));
                            }
                            else if (LF.LFN[i].IOTF == 1)
                            {
                                HRobot.set_DO(device_id, LF.LFN[i].IONum, true);
                                Console.WriteLine(HRobot.get_DO(17, 1));
                            }

                            Thread.Sleep(LF.LFN[i].IODelay);
                        }
                        else if (LF.LFN[i].Type.Equals("SLEEP"))
                        {
                            Thread.Sleep(LF.LFN[i].SleepDelay);
                        }
                        else if (LF.LFN[i].Type.Equals("null")) { }; 
                    }

                    if (HRobot.get_RI(device_id, 1) == 1)       /* For communication with other programs */
                    {
                        StreamWriter sw = new StreamWriter(@"C:\RobotStateMachine\SM_ON_OFF_File.txt");
                        sw.WriteLine("69");			// 寫入文字
                        sw.Close();
                    }
                    else
                    {
                        StreamWriter sw = new StreamWriter(@"C:\RobotStateMachine\SM_ON_OFF_File.txt");
                        sw.WriteLine("0");			// 寫入文字
                        sw.Close();
                    }

                    if (EmgStopCK == 1) { showRobotState = STATE_ALARM_EMERGENCY; }
                    else { showRobotState = STATE_READY; }

                    RunLoadNCCK = 0;
                }
            }
        }

        private void Btn_JOG_negative_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            int space_type = 0, index = 0;

            if (rbtn_JOG_X.IsChecked == true) { space_type = 0; index = 0; }
            else if (rbtn_JOG_Y.IsChecked == true) { space_type = 0; index = 1; }
            else if (rbtn_JOG_Z.IsChecked == true) { space_type = 0; index = 2; }
            else if (rbtn_JOG_A.IsChecked == true) { space_type = 0; index = 3; }
            else if (rbtn_JOG_B.IsChecked == true) { space_type = 0; index = 4; }
            else if (rbtn_JOG_C.IsChecked == true) { space_type = 0; index = 5; }
            else if (rbtn_JOG_A1.IsChecked == true) { space_type = 1; index = 0; }
            else if (rbtn_JOG_A2.IsChecked == true) { space_type = 1; index = 1; }
            else if (rbtn_JOG_A3.IsChecked == true) { space_type = 1; index = 2; }
            else if (rbtn_JOG_A4.IsChecked == true) { space_type = 1; index = 3; }
            else if (rbtn_JOG_A5.IsChecked == true) { space_type = 1; index = 4; }
            else if (rbtn_JOG_A6.IsChecked == true) { space_type = 1; index = 5; }

            HRobot.set_override_ratio(device_id, 50);
            HRobot.jog(device_id, space_type, index, -1);
        }

        private void Btn_JOG_negative_PreviewMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            HRobot.jog_stop(device_id);
        }

        private void Btn_JOG_positive_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            int space_type = 0, index = 0;

            if (rbtn_JOG_X.IsChecked == true) { space_type = 0; index = 0; }
            else if (rbtn_JOG_Y.IsChecked == true) { space_type = 0; index = 1; }
            else if (rbtn_JOG_Z.IsChecked == true) { space_type = 0; index = 2; }
            else if (rbtn_JOG_A.IsChecked == true) { space_type = 0; index = 3; }
            else if (rbtn_JOG_B.IsChecked == true) { space_type = 0; index = 4; }
            else if (rbtn_JOG_C.IsChecked == true) { space_type = 0; index = 5; }
            else if (rbtn_JOG_A1.IsChecked == true) { space_type = 1; index = 0; }
            else if (rbtn_JOG_A2.IsChecked == true) { space_type = 1; index = 1; }
            else if (rbtn_JOG_A3.IsChecked == true) { space_type = 1; index = 2; }
            else if (rbtn_JOG_A4.IsChecked == true) { space_type = 1; index = 3; }
            else if (rbtn_JOG_A5.IsChecked == true) { space_type = 1; index = 4; }
            else if (rbtn_JOG_A6.IsChecked == true) { space_type = 1; index = 5; }

            HRobot.set_override_ratio(device_id, 50);
            HRobot.jog(device_id, space_type, index, 1);
        }

        private void Btn_JOG_positive_PreviewMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            HRobot.jog_stop(device_id);
        }

        private void btn_ServoONOFF_Click(object sender, RoutedEventArgs e)
        {
            if (ServoCK == 1)
            {
                HRobot.set_motor_state(device_id, 1);   // Servo ON
                btn_ServoONOFF.Content = "ServoOFF";
                ServoCK = 0;
            }
            else
            {
                HRobot.motion_abort(device_id);
                HRobot.set_motor_state(device_id, 0);   // Servo OFF
                btn_ServoONOFF.Content = "ServoON";
                ServoCK = 1;
            }
        }

        private void btn_Home_Click(object sender, RoutedEventArgs e)
        {
            MC.HomeFunc();
        }

        private void btn_LoadFile_Click(object sender, RoutedEventArgs e)
        {
            LF.LoadNCFile();

            /* show NC file information */
            /*
            for (int i = 0; i < LF.NumofFileLines; i++)
            {
                Console.WriteLine(LF.LFN[i].Type + LF.LFN[i].MotionType + LF.LFN[i].Coordinate + LF.LFN[i].X + LF.LFN[i].Y + LF.LFN[i].Z + LF.LFN[i].A + LF.LFN[i].B + LF.LFN[i].C + LF.LFN[i].F);           
            }
            */
        }

        private void btn_RunLoadFile_Click(object sender, RoutedEventArgs e)
        {
            if (EmgStopCK == 1)
                RunLoadNCCK = 0;     /* RunLoadNCCK = 0，without NC file */
            else
                RunLoadNCCK = 1;     /* RunLoadNCCK = 1，with NC file */
        }

        private void btn_StateMachine_Click(object sender, RoutedEventArgs e)
        {
            if (SMCK == 1)
            {
                btn_StateMachine.Content = "SMOFF";
                SMCK = 0;

                ThreadSM = new Thread(FuncWaitSM_Loop);
                ThreadSM.Start();

                btn_ServoONOFF.IsEnabled = false;
                btn_Home.IsEnabled = false;
                btn_LoadFile.IsEnabled = false;
                btn_RunLoadFile.IsEnabled = false;
                btn_ClearAlarm.IsEnabled = false;
                btn_EmgStop.IsEnabled = false;

                gb_GripperControl.IsEnabled = false;
                //gb_IOControl.IsEnabled = false;
                gb_XEG32_Port.IsEnabled = false;
            }
            else
            {
                btn_StateMachine.Content = "SMON";
                SMCK = 1;

                /* -----與Emergency相同----- */
                RunLoadNCCK = 0;    // RunLoadNCCK = 0，未執行NCFILE；RunLoadNCCK = 1，執行NCFILE
                HRobot.motion_abort(device_id);
                /*---------------------------*/

                ThreadSM.Abort();

                btn_ServoONOFF.IsEnabled = true;
                btn_Home.IsEnabled = true;
                btn_LoadFile.IsEnabled = true;
                btn_RunLoadFile.IsEnabled = true;
                btn_ClearAlarm.IsEnabled = true;
                btn_EmgStop.IsEnabled = true;

                gb_GripperControl.IsEnabled = true;
                //gb_IOControl.IsEnabled = true;
                gb_XEG32_Port.IsEnabled = true;
            }
        }
        private void FuncWaitSM_Loop()
        {
            while (true)
            {
                if (RunLoadNCCK == 0)
                {
                    RunSMFile();
                }
                Thread.Sleep(200);
            }
        }
        public void RunSMFile()
        {
            try
            {
                var fileStream = new FileStream(@"C:\RobotStateMachine\SM_ON_OFF_File.txt", FileMode.Open, FileAccess.Read); // 讀取 state machine 狀態， 1 代表執行
                var sr = new StreamReader(fileStream);
                string line = sr.ReadLine();
                if (line.Equals("1"))
                {
                    Console.Write("\nRun\n");
                    /* The location of the state machine to read the program  */
                    LF.Interpretation_NCcode(@"C:\RobotStateMachine\HIWIN ROBOT NC CODE.txt");
                    RunLoadNCCK = 1;        /* with NC file */
                }
                else
                {
                    Console.Write("...\n");
                }
                sr.Close();
            }
            catch (Exception e)
            {
                Console.Write("failed\n");
            }

        }

        private void btn_ClearAlarm_Click(object sender, RoutedEventArgs e)
        {
            RunLoadNCCK = 0;    // RunLoadNCCK = 0，未執行NCFILE；RunLoadNCCK = 1，執行NCFILE
            EmgStopCK = 0;      // 無按下Emergency = 0，按下Emergency = 1
            showRobotState = STATE_READY;
            //HRobot.clear_alarm(device_id);
        }

        private void btn_EmgStop_Click(object sender, RoutedEventArgs e)
        {
            RunLoadNCCK = 0;    // RunLoadNCCK = 0，未執行NCFILE；RunLoadNCCK = 1，執行NCFILE
            EmgStopCK = 1;     // 無按下Emergency = 0，按下Emergency = 1
            HRobot.motion_abort(device_id);
            showRobotState = STATE_ALARM_EMERGENCY;
        }
        /*
        private void sld_ProgOvrd_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            HRobot.set_override_ratio(device_id, Convert.ToInt32(sld_ProgOvrd.Value));
        }
        */
        private void btn_IO_ON_Click(object sender, RoutedEventArgs e)
        {
            /*
            for (int i = 1; i <= 3; i++)
                HRobot.set_robot_output(device_id, i, false);

            HRobot.set_robot_output(device_id, cmb_IOControl.SelectedIndex + 1, true);
            */
        }

        private void btn_IO_OFF_Click(object sender, RoutedEventArgs e)
        {
            /*
            for (int i = 1; i <= 3; i++)
                HRobot.set_robot_output(device_id, i, false);
            */
        }

        private void btn_MoveGripper_Click(object sender, RoutedEventArgs e)
        {
            EG_Control.RunMove(Convert.ToInt32(TB_GripPos.Text), 30);
        }

        private void btn_ResetGripper_Click(object sender, RoutedEventArgs e)
        {
            EG_Control.ResetMotion();
        }

        private void btn_GripOpen_Click(object sender, RoutedEventArgs e)
        {
            EG_Control.RunMove(10, 5);
            //EG_Control.RunGrip('o', 10, 'm', 'm');
        }

        private void btn_GripClose_Click(object sender, RoutedEventArgs e)
        {
            EG_Control.RunMove(32, 5);
            //EG_Control.RunGrip('c', 10, 'm', 'm');
        }

    }
}
