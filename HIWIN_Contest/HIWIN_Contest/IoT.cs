using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HIWIN_Contest
{
    class IoT
    {
        StateMachine SM = new StateMachine();
        public int device_id { get; set; }

        /* */
        public int Override, MotorState, MotionState; //SpeedLimitState
        public double[] CurrentXYZABC = new double[6];
        public double[] CurrentJoint = new double[6];

        /* Thread */
        private System.Threading.Thread t1;

        public void IoTmainClose()
        {
            if (t1.IsAlive == true) { t1.Abort(); }
        }

        private string UpLoad_Robot_POS_TCP()
        {
            return "[{\"CMD\":\"POS_TCP_X\",\"POS_TCP_X\":\"" + CurrentXYZABC[0].ToString("F3") + "\"}," +
            "{\"CMD\":\"POS_TCP_Y\",\"POS_TCP_Y\":\"" + CurrentXYZABC[1].ToString("F3") + "\"}," +
            "{\"CMD\":\"POS_TCP_Z\",\"POS_TCP_Z\":\"" + CurrentXYZABC[2].ToString("F3") + "\"}," +
            "{\"CMD\":\"POS_TCP_A\",\"POS_TCP_A\":\"" + CurrentXYZABC[3].ToString("F3") + "\"}," +
            "{\"CMD\":\"POS_TCP_B\",\"POS_TCP_B\":\"" + CurrentXYZABC[4].ToString("F3") + "\"}," +
            "{\"CMD\":\"POS_TCP_C\",\"POS_TCP_C\":\"" + CurrentXYZABC[5].ToString("F3") + "\"}]";
        }
        private string UpLoad_Robot_POS_AXIS()
        {
            return "[{\"CMD\":\"POS_AXIS_A1\",\"POS_AXIS_A1\":\"" + CurrentJoint[0].ToString("F3") + "\"}," +
            "{\"CMD\":\"POS_AXIS_A2\",\"POS_AXIS_A2\":\"" + CurrentJoint[1].ToString("F3") + "\"}," +
            "{\"CMD\":\"POS_AXIS_A3\",\"POS_AXIS_A3\":\"" + CurrentJoint[2].ToString("F3") + "\"}," +
            "{\"CMD\":\"POS_AXIS_A4\",\"POS_AXIS_A4\":\"" + CurrentJoint[3].ToString("F3") + "\"}," +
            "{\"CMD\":\"POS_AXIS_A5\",\"POS_AXIS_A5\":\"" + CurrentJoint[4].ToString("F3") + "\"}," +
            "{\"CMD\":\"POS_AXIS_A6\",\"POS_AXIS_A6\":\"" + CurrentJoint[5].ToString("F3") + "\"}]";
        }

        private string UpLoad_Robot_State()
        {
            return "[{\"CMD\":\"Robot_Motion_State\",\"Robot_Motion_State\":\"" + MotionState + "\"}," +
            "{\"CMD\":\"Robot_Motor_State\",\"Robot_Motor_State\":\"" + MotorState + "\"}," +
            "{\"CMD\":\"Robot_Override_State\",\"Robot_Override_State\":\"" + Override + "\"}";
            //+"{\"CMD\":\"Robot_Speed_Limit_State\",\"Robot_Speed_Limit_State\":\"" + SpeedLimitState + "\"}]";
        }
    }
}
