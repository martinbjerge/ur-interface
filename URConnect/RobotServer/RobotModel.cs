using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using RobotServer.Types;

namespace RobotServer
{
    public enum ConnectionState : int
    {
        Error = 0,
        Disconnected = 1,
        Connected = 2,
        Paused = 3,
        Started = 4
    }

    public enum RobotMode : uint
    {
        DISCONNECTED = 0,
        CONFIRM_SAFETY = 1,
        BOOTING = 2,
        POWER_OFF = 3,
        POWER_ON = 4,
        IDLE = 5,
        BACKDRIVE = 6,
        RUNNING = 7,
        UPDATING_FIRMWARE = 8
    }

    public enum SafetyMode : uint
    {
        NORMAL = 1,
        REDUCED = 2,
        PROTECTIVE_STOP = 3,
        RECOVERY = 4,
        SAFEGUARD_STOP = 5,
        SYSTEM_EMERGENCY_STOP = 6,
        ROBOT_EMERGENCY_STOP = 7,
        VIOLATION = 8,
        FAULT = 9
    }

    public class RobotModel
    {
        public string Password { get; set; }

        public IPAddress IpAddress { get; set; }

        public double RobotTimestamp { get; set; }

        public ConnectionState RTDEConnectionState { get; set; }


        #region Digital Output Bits
        public bool DigitalOutputBit0 { get; set; }

        public bool DigitalOutputBit1 { get; set; }

        public bool DigitalOutputBit2 { get; set; }

        public bool DigitalOutputBit3 { get; set; }

        public bool DigitalOutputBit4 { get; set; }

        public bool DigitalOutputBit5 { get; set; }

        public bool DigitalOutputBit6 { get; set; }

        public bool DigitalOutputBit7 { get; set; }
        

        #endregion

        

        public int RTDEProtocolVersion { get; set; }

        public Vector6D ActualTCPPose { get; set; }

        public RobotMode RobotMode { get; set; }

        public SafetyMode SafetyMode { get; set; }
    }
}
