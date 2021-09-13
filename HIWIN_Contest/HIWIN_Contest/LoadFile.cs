using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace HIWIN_Contest
{
    class LoadFile
    {
        public int CoordinateWorld = 1;
        public int CoordinateJoint = 2;
        public int NumofFileLines;
        public struct LoadFileNC
        {
            public string Type;
            public string MotionType;
            public int Coordinate;           // 1:POSITION, 2:AXIS
            public double[] buf;
            public int F, CNT, GripPos, GripVel, GripForce, GripDelay;
            public int IONum, IOTF, IODelay;
            public int SleepDelay;
        }

        public LoadFileNC[] LFN;

        public int LoadNCFile()
        {
            Microsoft.Win32.OpenFileDialog dlg = new Microsoft.Win32.OpenFileDialog();

            // Set filter for file extension and default file extension
            dlg.DefaultExt = ".txt";
            dlg.Filter = "Text documents (.txt)|*.txt";

            // Display OpenFileDialog by calling ShowDialog method
            Nullable<bool> result = dlg.ShowDialog();

            // Get the selected file name and display in a TextBox
            if (result == true)
            {
                // Open document
                string filename = dlg.FileName;
                Interpretation_NCcode(filename);
                return 0;
            }
            else { return -1; }


        }

        public void Interpretation_NCcode(string filename)
        {
            StreamReader sr = new StreamReader(filename);

            string line;
            NumofFileLines = 0;
            int FileLineCnt = 0;        // File line count

            while ((line = sr.ReadLine()) != null) { NumofFileLines++; } // Calculate the number of file lines
            sr.BaseStream.Position = 0;             // Back to the first line
            LFN = new LoadFileNC[NumofFileLines];   // Define LFN struct size    
            /* Interpreting file content */
            while ((line = sr.ReadLine()) != null)
            {
                LFN[FileLineCnt].buf = new double[6];

                string[] strArray = line.Split('\t');
                for (int i = 0; i < strArray.Length; i++)        //透過迴圈將陣列值取出 也可用foreach
                {
                    if (strArray[i].Equals("")) { if (i == 0) { LFN[FileLineCnt].Type = "null"; } }
                    else if (strArray[i].Equals("MOVE")) { LFN[FileLineCnt].Type = strArray[i]; }
                    else if (strArray[i].Equals("GRIP")) { LFN[FileLineCnt].Type = strArray[i]; LFN[FileLineCnt].GripPos = int.Parse(strArray[i + 1]); LFN[FileLineCnt].GripVel = int.Parse(strArray[i + 2]); LFN[FileLineCnt].GripForce = int.Parse(strArray[i + 3]); LFN[FileLineCnt].GripDelay = int.Parse(strArray[i + 4]); }
                    else if (strArray[i].Equals("IO")) { LFN[FileLineCnt].Type = strArray[i]; LFN[FileLineCnt].IONum = int.Parse(strArray[i + 1]); LFN[FileLineCnt].IOTF = int.Parse(strArray[i + 2]); LFN[FileLineCnt].IODelay = int.Parse(strArray[i + 3]); }
                    else if (strArray[i].Equals("SLEEP")) { LFN[FileLineCnt].Type = strArray[i]; LFN[FileLineCnt].SleepDelay = int.Parse(strArray[i + 1]); }
                    else if (strArray[i].Equals("L")) { LFN[FileLineCnt].MotionType = strArray[i]; }
                    else if (strArray[i].Equals("J")) { LFN[FileLineCnt].MotionType = strArray[i]; }
                    else
                    {
                        string[] strArray2 = strArray[i].Split(' ');
                        for (int j = 0; j < strArray2.Length; j++)        //透過迴圈將陣列值取出 也可用foreach
                        {
                            if (strArray2[j].Equals("X")) { LFN[FileLineCnt].buf[0] = double.Parse(strArray2[j + 1]); LFN[FileLineCnt].Coordinate = CoordinateWorld; }
                            else if (strArray2[j].Equals("Y")) { LFN[FileLineCnt].buf[1] = double.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("Z")) { LFN[FileLineCnt].buf[2] = double.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("A")) { LFN[FileLineCnt].buf[3] = double.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("B")) { LFN[FileLineCnt].buf[4] = double.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("C")) { LFN[FileLineCnt].buf[5] = double.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("A1")) { LFN[FileLineCnt].buf[0] = double.Parse(strArray2[j + 1]); LFN[FileLineCnt].Coordinate = CoordinateJoint; }
                            else if (strArray2[j].Equals("A2")) { LFN[FileLineCnt].buf[1] = double.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("A3")) { LFN[FileLineCnt].buf[2] = double.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("A4")) { LFN[FileLineCnt].buf[3] = double.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("A5")) { LFN[FileLineCnt].buf[4] = double.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("A6")) { LFN[FileLineCnt].buf[5] = double.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("F")) { LFN[FileLineCnt].F = int.Parse(strArray2[j + 1]); }
                            else if (strArray2[j].Equals("CNT")) { LFN[FileLineCnt].CNT = int.Parse(strArray2[j + 1]); }
                        }
                    }
                }
                FileLineCnt = FileLineCnt + 1;
            }
            sr.Close();
            /* print NC file */
            //for (int i = 0; i < NumofFileLines; i++) { Console.WriteLine(LFN[i].Type + LFN[i].MotionType + LFN[i].Coordinate + LFN[i].X + LFN[i].Y + LFN[i].Z + LFN[i].A + LFN[i].B + LFN[i].C + LFN[i].F); }
        }

    }
}
