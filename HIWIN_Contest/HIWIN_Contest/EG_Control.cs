using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;

namespace HIWIN_Contest
{
    class EG_Control
    {
        #region EG_Control_API

        [DllImport("EG_Control_API.dll")]
        public static extern void CurSoftwareVersion(ref uint Ver1, ref uint Ver2, ref uint Ver3, ref uint Ver4);

        [DllImport("EG_Control_API.dll")]
        public static extern int StartConnect(int SettingComPort, int SelectModelType);

        [DllImport("EG_Control_API.dll")]
        public static extern int DetectConnect();

        [DllImport("EG_Control_API.dll")]
        public static extern int CloseConnect();

        [DllImport("EG_Control_API.dll")]
        public static extern int CurFirmwareVersion(ref int Ver1, ref int Ver2, ref int Ver3);

        [DllImport("EG_Control_API.dll")]
        public static extern double CurrentPos();

        [DllImport("EG_Control_API.dll")]
        public static extern void IOStatus(ref uint InputData, ref uint OutputData);

        [DllImport("EG_Control_API.dll")]
        public static extern bool WorkState();

        [DllImport("EG_Control_API.dll")]
        public static extern bool HoldState();

        [DllImport("EG_Control_API.dll")]
        public static extern int AlarmState();

        [DllImport("EG_Control_API.dll")]
        public static extern int ResetMotion();

        [DllImport("EG_Control_API.dll")]
        public static extern void StopMotion();

        [DllImport("EG_Control_API.dll")]
        public static extern int RunMove(double MovPosition, int MovSpeed);

        [DllImport("EG_Control_API.dll")]
        public static extern int RunGrip(char Dir, int Str, char GriSpeed, char GriForce);

        [DllImport("EG_Control_API.dll")]
        public static extern int RunExpert(char Dir, double MovStr, int MovSpeed, double GriStr, int GriSpeed, int GriForce);

        #endregion
    }
}
