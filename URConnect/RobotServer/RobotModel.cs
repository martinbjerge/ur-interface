using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using RobotServer.Types;

[assembly: log4net.Config.XmlConfigurator(Watch = true)]

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
        private static readonly log4net.ILog log = log4net.LogManager.GetLogger(typeof(RobotModel));
        private bool _digitalOutputBit0;
        private bool _digitalOutputBit1;
        private bool _digitalOutputBit2;
        private bool _digitalOutputBit3;
        private bool _digitalOutputBit4;
        private bool _digitalOutputBit5;
        private bool _digitalOutputBit6;
        private bool _digitalOutputBit7;
        private Vector6D _actualTCPPose;

        public string Password { get; set; }

        public IPAddress IpAddress { get; set; }

        public double RobotTimestamp { get; set; }

        public ConnectionState RTDEConnectionState { get; set; }


        #region Digital Output Bits

        public bool DigitalOutputBit0
        {
            get { return _digitalOutputBit0; }
            set
            {
                if (value != _digitalOutputBit0)
                {
                    _digitalOutputBit0 = value;
                    log.Info("DigitalOutputBit0, "+ _digitalOutputBit0);
                }
            }
        }
            
        public bool DigitalOutputBit1
        {
            get { return _digitalOutputBit1; }
            set
            {
                if (value != _digitalOutputBit1)
                {
                    _digitalOutputBit1 = value;
                    log.Info("DigitalOutputBit1, " + _digitalOutputBit1);
                }
            }
        }

        public bool DigitalOutputBit2
        {
            get { return _digitalOutputBit2; }
            set
            {
                if (value != _digitalOutputBit2)
                {
                    _digitalOutputBit2 = value;
                    log.Info("DigitalOutputBit2, " + _digitalOutputBit2);
                }
            }
        }

        public bool DigitalOutputBit3
        {
            get { return _digitalOutputBit3; }
            set
            {
                if (value != _digitalOutputBit3)
                {
                    _digitalOutputBit3 = value;
                    log.Info("DigitalOutputBit3, " + _digitalOutputBit3);
                }
            }
        }

        public bool DigitalOutputBit4
        {
            get { return _digitalOutputBit4; }
            set
            {
                if (value != _digitalOutputBit4)
                {
                    _digitalOutputBit4 = value;
                    log.Info("DigitalOutputBit4, " + _digitalOutputBit4);
                }
            }
        }

        public bool DigitalOutputBit5
        {
            get { return _digitalOutputBit5; }
            set
            {
                if (value != _digitalOutputBit5)
                {
                    _digitalOutputBit5 = value;
                    log.Info("DigitalOutputBit5, " + _digitalOutputBit5);
                }
            }
        }

        public bool DigitalOutputBit6
        {
            get { return _digitalOutputBit6; }
            set
            {
                if (value != _digitalOutputBit6)
                {
                    _digitalOutputBit6 = value;
                    log.Info("DigitalOutputBit6, " + _digitalOutputBit6);
                }
            }
        }

        public bool DigitalOutputBit7
        {
            get { return _digitalOutputBit7; }
            set
            {
                if (value != _digitalOutputBit7)
                {
                    _digitalOutputBit7 = value;
                    log.Info("DigitalOutputBit7, " + _digitalOutputBit7);
                }
            }
        }


        #endregion



        public int RTDEProtocolVersion { get; set; }

        public Vector6D ActualTCPPose
        {
            get { return _actualTCPPose; }
            set
            {
                if (!CompareVector6D(_actualTCPPose, value, 0.00001))
                {
                    _actualTCPPose = value;
                    log.Info($"ActualTCPPose,{_actualTCPPose.X}, {_actualTCPPose.Y}, {_actualTCPPose.Z}, {_actualTCPPose.RX}, {_actualTCPPose.RY}, {_actualTCPPose.RZ}");
                }
            }
        }

        public RobotMode RobotMode { get; set; }

        public SafetyMode SafetyMode { get; set; }

        private bool CompareVector6D(Vector6D firstVector6D, Vector6D secondVector6D, double precision)
        {
            if (firstVector6D == null || secondVector6D == null)
                return false;
            if (firstVector6D.X - secondVector6D.X > precision || secondVector6D.X - firstVector6D.X > precision )
            {
                return false;
            }
            if (firstVector6D.Y - secondVector6D.Y > precision || secondVector6D.Y - firstVector6D.Y > precision)
            {
                return false;
            }
            if (firstVector6D.Z - secondVector6D.Z > precision || secondVector6D.Z - firstVector6D.Z > precision)
            {
                return false;
            }
            if (firstVector6D.RX - secondVector6D.RX > precision || secondVector6D.RX - firstVector6D.RX > precision)
            {
                return false;
            }
            if (firstVector6D.RY - secondVector6D.RY > precision || secondVector6D.RY - firstVector6D.RY > precision)
            {
                return false;
            }
            if (firstVector6D.RZ - secondVector6D.RZ > precision || secondVector6D.RZ- firstVector6D.RZ > precision)
            {
                return false;
            }
            return true;
        }
    }
}
