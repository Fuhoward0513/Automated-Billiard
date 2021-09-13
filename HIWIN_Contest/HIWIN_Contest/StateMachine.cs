using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace HIWIN_Contest
{
    class StateMachine
    {
        public int device_id;

        LoadFile LF = new LoadFile();
      
        public void ExcuteMotionInit()
        {
            // HRobot.speed_limit_on(device_id);           // it's need override before
            HRobot.set_override_ratio(device_id, 100);  // override speed ratio
            HRobot.set_motor_state(device_id, 1);       // Servo ON
        }

    }
}
