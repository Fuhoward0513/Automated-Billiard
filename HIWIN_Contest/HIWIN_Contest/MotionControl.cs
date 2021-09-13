using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HIWIN_Contest
{
    class MotionControl
    {
        public int device_id;
        public void HomeFunc()
        {
            double[] Home = { 0, 0, 0, 0, -90, 0 };
            HRobot.set_ptp_speed(device_id, 100);    // 設定點對點運動速度，參數:裝置的ID/點對點速度比例 1-100(%)，回傳值 0:成功(INT)
            HRobot.ptp_axis(device_id, 0, Home);    //ptp to robot home ，參數: 裝置的ID/關節座標
        }
    }
}
