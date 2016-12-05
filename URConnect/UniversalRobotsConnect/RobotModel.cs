using System;
using System.Collections;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;
using UniversalRobotsConnect.Types;

[assembly: log4net.Config.XmlConfigurator(Watch = true)]

namespace UniversalRobotsConnect
{

    #region enums

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
        Normal = 1,
        Reduced = 2,
        ProtectiveStop = 3,
        Recovery = 4,
        SafeguardStop = 5,
        SystemEmergencyStop = 6,
        RobotEmergencyStop = 7,
        Violation = 8,
        Fault = 9
    }
    
    /// <summary>
    /// The State of a program running on the Robot - UnInitialized until the first program is send to robot, then alternating between Idle and Running depending.
    /// </summary>
    public enum RuntimeState : uint
    {
        UnInitialized = 0,
        Idle = 1,
        Running = 2
    }

    public enum JointMode : int
    {
        ShuttingDown = 236,
        PartDCalibration = 237,
        BackDrive = 238,
        PowerOff = 239,
        NotResponding = 245,
        MotorInitialization = 246,
        Booting = 247,
        PartDCalibrationError = 248,
        Bootloader = 249,
        Calibration = 250,
        Fault = 252,
        Running = 253,
        Idle = 255
    }

    #endregion

    public class RobotModel
    {

        //private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        #region BackingFields
        private double[] _actualTCPPose;
        private RobotMode _robotMode;
        private SafetyMode _safetyMode;
        private int _rtdeProtocolVersion;
        private double[] _targetQ;
        private double _vector6DPrecision = 0.00001;
        private double[] _targetQD;
        private double[] _targetQDD;
        private double[] _targetCurrent;
        private double[] _targetMoment;
        private double[] _actualQ;
        private double[] _actualQD;
        private double[] _actualCurrent;
        private double[] _targetTCPPose;
        private RuntimeState _runtimeState;
        //private bool _robotStatusPowerOn;
        private SafetyStatus _safetyStatus = new SafetyStatus();
        private RobotStatus _robotStatus = new RobotStatus();
        private double _robotTimeStamp;
        private double[] _forceTorque;
        private bool _stopRunningFlag = false;
        private OutputIntRegister _outputIntRegister = new OutputIntRegister();
        private OutputDoubleRegister _outputDoubleRegister = new OutputDoubleRegister();
        private readonly DigitalBits _digitalInputbits = new DigitalBits();
        private readonly DigitalBits _configurableInputbits = new DigitalBits();
        private readonly DigitalBits _digitalOutputbits = new DigitalBits();
        private readonly DigitalBits _configurableOutputBits = new DigitalBits();

        internal ConcurrentQueue<RobotModel> ModelUpdateQueue = new ConcurrentQueue<RobotModel>();
        private Thread _modelUpdaterThread;
        #endregion

        //public RobotModel()
        //{
        //    _modelUpdaterThread = new Thread(ProcessModelUpdates);
        //    _modelUpdaterThread.Start();
        //}


        private void ProcessModelUpdates()
        {
            while (true)
            {
                RobotModel localRobotModel;
                if (ModelUpdateQueue.Count > 0)
                {
                    bool success = ModelUpdateQueue.TryDequeue(out localRobotModel);
                    if (success)
                    {
                        UpdateModel(localRobotModel);
                    }
                    if (ModelUpdateQueue.Count > 2)
                    {
                        //log.Debug($"Robotmodels in queue: {ModelUpdateQueue.Count}");
                        Console.WriteLine($"Robotmodels in queue: {ModelUpdateQueue.Count}");
                    }
                }
                Thread.Sleep(6);
            }

        }

        private void UpdateModel(RobotModel localRobotModel)
        {
            DateTime startTime = DateTime.Now;
            double delta = localRobotModel.RobotTimestamp - RobotTimestamp;
            if (delta > 0.008001)
            {
                //log.Debug($"Too long since last robot timestamp {delta * 1000} milliseconds!!!!  WE LOST A PACKAGE!!!!!");
                //Console.WriteLine($"Too long since last ROBOT TIMESTAMP {delta*1000} milliseconds!!!!  WE LOST A PACKAGE!!!!!");
            }

            ActualCurrent = localRobotModel.ActualCurrent;
            ActualExecutionTime = localRobotModel.ActualExecutionTime;
            ActualJointVoltage = localRobotModel.ActualJointVoltage;
            ActualMainVoltage = localRobotModel.ActualMainVoltage;
            ActualMomentum = localRobotModel.ActualMomentum;
            ActualQ = localRobotModel.ActualQ;
            ActualQD = localRobotModel.ActualQD;
            ActualRobotCurrent = localRobotModel.ActualRobotCurrent;
            ActualRobotVoltage = localRobotModel.ActualRobotVoltage;
            ActualTCPForce = localRobotModel.ActualTCPForce;
            ActualTCPPose = localRobotModel.ActualTCPPose;
            ActualTCPSpeed = localRobotModel.ActualTCPSpeed;
            ConfigurableInputBits.AllBits = localRobotModel.ConfigurableInputBits.AllBits;
            ConfigurableOutputBits.AllBits = localRobotModel.ConfigurableOutputBits.AllBits;

            DigitalInputbits.AllBits = localRobotModel.DigitalInputbits.AllBits;
            DigitalOutputBits.AllBits = localRobotModel.DigitalInputbits.AllBits;

            RuntimeState = localRobotModel.RuntimeState;
            StandardAnalogInput0 = localRobotModel.StandardAnalogInput0;
            StandardAnalogInput1 = localRobotModel.StandardAnalogInput1;
            StandardAnalogOutput0 = localRobotModel.StandardAnalogOutput;
            TargetMoment = localRobotModel.TargetMoment;
            TargetQ = localRobotModel.TargetQ;
            TargetQD = localRobotModel.TargetQD;
            TargetQDD = localRobotModel.TargetQDD;
            TargetSpeedFraction = localRobotModel.TargetSpeedFraction;
            TargetTCPPose = localRobotModel.TargetTCPPose;
            TargetTCPSpeed = localRobotModel.TargetTCPSpeed;
            ToolAnalogInput0 = localRobotModel.ToolAnalogInput0;
            ToolAnalogInput1 = localRobotModel.ToolAnalogInput1;
            ToolOutputCurrent = localRobotModel.ToolOutputCurrent;
            ToolOutputVoltage = localRobotModel.ToolOutputVoltage;

            TimeSpan realDelta = DateTime.Now - LastUpdateTimestamp;
            if (realDelta.TotalMilliseconds < 2)
            {
                Thread.Sleep(2);    //we want to allow time for clients to update 
            }
            if (realDelta.TotalMilliseconds > 32)
            {
                //log.Debug($"Realtime {realDelta.TotalMilliseconds} MS since last update - too slow");
                //Console.WriteLine($"Realtime {realDelta.TotalMilliseconds} MS since last update - too slow");
            }
            LastUpdateTimestamp = DateTime.Now;
            RobotTimestamp = localRobotModel.RobotTimestamp;
            TimeSpan timespan = DateTime.Now - startTime;
            if (timespan.TotalMilliseconds > 4)
            {
                //log.Debug($"Time to update model: {timespan.TotalMilliseconds}");
                //Console.WriteLine($"Time to update model: {timespan.TotalMilliseconds}");
            }

        }

        public string Password { get; set; }

        public IPAddress IpAddress { get; set; }

        public double RobotTimestamp
        {
            get { return _robotTimeStamp; }
            set
            {
                //log.Info($"{RobotTimestamp} , RobotTimestamp");
                //double delta = value - _robotTimeStamp;
                //if (delta > 0.0081)
                //{
                //    log.Error($"Time since last RTDE timestamp: {delta}");
                //}
                _robotTimeStamp = value;
            }
        }

        public DateTime LastUpdateTimestamp { get; set; }

        public ConnectionState RTDEConnectionState { get; set; }

        /// <summary>
        /// Flag used when program using UR-Script and UR-ScriptEXT needs to shut down before completed
        /// This can be in seperate threads - set this flag when need to stop and listen in all threads
        /// </summary>
        public bool StopRunningFlag
        {
            get { return _stopRunningFlag; }
            set
            {
                if (_stopRunningFlag != value)
                {
                    _stopRunningFlag = value;
                    //log.Info($"{RobotTimestamp} , StopRunningFlag, {_stopRunningFlag}");
                }
            }
        }
        
        #region Digital Input Bits

        public DigitalBits DigitalInputbits
        {
            get { return _digitalInputbits; }
        }

        public DigitalBits ConfigurableInputBits
        {
            get { return _configurableInputbits; }
        }

        #endregion


        #region Digital Output Bits

        public DigitalBits DigitalOutputBits
        {
            get { return _digitalOutputbits; }
        }

        public DigitalBits ConfigurableOutputBits
        {
            get { return _configurableOutputBits; }
        }

        #endregion



        public int RTDEProtocolVersion
        {
            get { return _rtdeProtocolVersion; }
            set {
                if (_rtdeProtocolVersion != value)
                {
                    _rtdeProtocolVersion = value;
                    //log.Info(RobotTimestamp + " ,RTDEProtocolVersion: " + _rtdeProtocolVersion);
                }
            }
        }

        public double[] ActualTCPPose
        {
            get { return _actualTCPPose; }
            set
            {
                if (!Vector6DEquals(_actualTCPPose, value, _vector6DPrecision))
                {
                    _actualTCPPose = value;
                    //log.Info($"{RobotTimestamp}, ActualTCPPose,{_actualTCPPose[0]}, {_actualTCPPose[1]}, {_actualTCPPose[2]}, {_actualTCPPose[3]}, {_actualTCPPose[4]}, {_actualTCPPose[5]}");
                }
            }
        }

        public RobotMode RobotMode
        {
            get { return _robotMode; }
            set
            {
                if (_robotMode!= value)
                {
                    _robotMode = value;
                    //log.Info(RobotTimestamp + " ,Robotmode, " + _robotMode);
                }
            }
        }

        public SafetyMode SafetyMode
        {
            get { return _safetyMode; }
            set {
                if (_safetyMode != value)
                {
                    _safetyMode = value;
                    //log.Info(RobotTimestamp +" ,SafetyMode, " + _safetyMode);
                }
            }
        }

        public double[] TargetQ
        {
            get { return _targetQ; }
            set
            {
                if (!Vector6DEquals(_targetQ, value, _vector6DPrecision))
                {
                    _targetQ = value;
                    //log.Info($"{RobotTimestamp}, TargetQ,{_targetQ[0]}, {_targetQ[1]}, {_targetQ[2]}, {_targetQ[3]}, {_targetQ[4]}, {_targetQ[5]}");
                }
            }
        }

        public double[] TargetQD
        {
            get { return _targetQD; }
            set
            {
                if (!Vector6DEquals(_targetQD, value, _vector6DPrecision))
                {
                    _targetQD = value;
                    //log.Info($"{RobotTimestamp}, TargetQD,{_targetQD[0]}, {_targetQD[1]}, {_targetQD[2]}, {_targetQD[3]}, {_targetQD[4]}, {_targetQD[5]}");
                }
            }
        }

        public double[] TargetQDD
        {
            get { return _targetQDD; }
            set
            {
                if (!Vector6DEquals(_targetQDD, value, _vector6DPrecision))
                {
                    _targetQDD = value;
                    //log.Info($"{RobotTimestamp}, TargetQDD,{_targetQDD[0]}, {_targetQDD[1]}, {_targetQDD[2]}, {_targetQDD[3]}, {_targetQDD[4]}, {_targetQDD[5]}");
                }
            }
        }

        public double[] TargetCurrent 
        {
            get { return _targetCurrent; }
            set
            {
                if (!Vector6DEquals(_targetCurrent, value, _vector6DPrecision))
                {
                    _targetCurrent = value;
                    //log.Info($"{RobotTimestamp}, TargetCurrent,{_targetCurrent[0]}, {_targetCurrent[1]}, {_targetCurrent[2]}, {_targetCurrent[3]}, {_targetCurrent[4]}, {_targetCurrent[5]}");
                }
            }
        }

        public double[] TargetMoment       
        {
            get { return _targetMoment; }
            set
            {
                if (!Vector6DEquals(_targetMoment, value, _vector6DPrecision))
                {
                    _targetMoment = value;
                    //log.Info($"{RobotTimestamp}, TargetMoment,{_targetMoment[0]}, {_targetMoment[1]}, {_targetMoment[2]}, {_targetMoment[3]}, {_targetMoment[4]}, {_targetMoment[5]}");
                }
            }
        }

        public double[] ActualQ
        {
            get { return _actualQ; }
            set
            {
                if (!Vector6DEquals(_actualQ, value, _vector6DPrecision))
                {
                    _actualQ = value;
                    //log.Info($"{RobotTimestamp}, ActualQ,{_actualQ[0]}, {_actualQ[1]}, {_actualQ[2]}, {_actualQ[3]}, {_actualQ[4]}, {_actualQ[5]}");
                }
            }
        }

        public double[] ActualQD
        {
            get {return _actualQD;}
            set
            {
                if (!Vector6DEquals(_actualQD, value, _vector6DPrecision))
                {
                    _actualQD = value;
                    //log.Info($"{RobotTimestamp}, ActualQD,{_actualQD[0]}, {_actualQD[1]}, {_actualQD[2]}, {_actualQD[3]}, {_actualQD[4]}, {_actualQD[5]}");
                }
            }
        }

        public double[] ActualCurrent
        {
            get { return _actualCurrent; }
            set
            {
                if (!Vector6DEquals(_actualCurrent, value, _vector6DPrecision))
                {
                    _actualCurrent = value;
                    //log.Info($"{RobotTimestamp}, ActualCurrent,{_actualCurrent[0]}, {_actualCurrent[1]}, {_actualCurrent[2]}, {_actualCurrent[3]}, {_actualCurrent[4]}, {_actualCurrent[5]}");
                }
            }
        }

        public double[] JointControlOutput { get; set; }
        public double[] ActualTCPSpeed { get; set; }
        public double[] ActualTCPForce { get; set; }

        public double[] TargetTCPPose
        {
            get
            {
                return _targetTCPPose;
            }
            set
            {
                _targetTCPPose = value;
                //log.Info($"{RobotTimestamp}, TargetTCPPose,{_targetTCPPose.X}, {_targetTCPPose.Y}, {_targetTCPPose.Z}, {_targetTCPPose.RX}, {_targetTCPPose.RY}, {_targetTCPPose.RZ}");   //LOGSPAM
            }
        }
        public double[] TargetTCPSpeed { get; set; }
        public double[] JointTemperatures { get; set; }
        public double ActualExecutionTime { get; set; }
        public double[] JointMode { get; set; }     //must use jointmode enum
        public double[] ActualToolAccelerometer { get; set; }
        public double SpeedScaling { get; set; }
        public double TargetSpeedFraction { get; set; }
        public double ActualMomentum { get; set; }
        public double ActualMainVoltage { get; set; }
        public double ActualRobotVoltage { get; set; }
        public double ActualRobotCurrent { get; set; }
        public double[] ActualJointVoltage { get; set; }

        /// <summary>
        /// Running state of a RealTimeClient program send to the Robot
        /// </summary>
        public RuntimeState RuntimeState
        {
            get { return _runtimeState; }
            set
            {
                if (_runtimeState != value)
                {
                    //Debug.WriteLine($"RuntimeState {value} is just set in model - RobotTime {RobotTimestamp}");
                    _runtimeState = value;
                    ////log.Info($"{RobotTimestamp}, RuntimeState, {_runtimeState}");
                    //if (value == RuntimeState.Running)
                    //{
                    //    Debug.WriteLine("WE ARE FINALLY RUNNING");
                    //}
                }
            }
        }
        public double IOCurrent { get; set; }
        public double ToolAnalogInput0 { get; set; }
        public double ToolAnalogInput1 { get; set; }
        public double ToolOutputCurrent { get; set; }
        public int ToolOutputVoltage { get; set; }
        public double StandardAnalogInput0 { get; set; }
        public double StandardAnalogInput1 { get; set; }
        public double StandardAnalogOutput0 { get; set; }
        public double StandardAnalogOutput { get; set; }

        public RobotStatus RobotStatus
        {
            get { return _robotStatus; }
            set { _robotStatus = value; }
        }

        public SafetyStatus SafetyStatus
        {
            get { return _safetyStatus; }
            set { _safetyStatus = value; }
        }

        public double TCPForceScalar { get; set; }

        public double[] ForceTourqe
        {
            get { return _forceTorque; }
            set
            {
                if (!Vector6DEquals(_forceTorque, value, _vector6DPrecision))
                {
                    _forceTorque = value;
                    //log.Info($"{RobotTimestamp}, ForceTorque,{_forceTorque[0]}, {_forceTorque[1]}, {_forceTorque[2]}, {_forceTorque[3]}, {_forceTorque[4]}, {_forceTorque[5]}");
                }
            }
        }

        #region OutputBitRegisters

        public OutputBitRegister OutputBitRegister { get; } = new OutputBitRegister();

        #endregion

        #region OutputIntRegisters

        public OutputIntRegister OutputIntRegister
        {
            get { return _outputIntRegister; }
            set { _outputIntRegister = value; }
        }

        #endregion

        #region OutputDoubleRegisters

        public OutputDoubleRegister OutputDoubleRegister
        {
            get { return _outputDoubleRegister; }
            set { _outputDoubleRegister = value; }
        }

        public URControlVersion URControlVersion { get; set; }

        #endregion

        public bool ClearToSend { get; set; }



        private bool Vector6DEquals(double[] firstVector6D, double[] secondVector6D, double precision)
        {
            if (firstVector6D == null || secondVector6D == null)
                return false;
            if (firstVector6D[0] - secondVector6D[0] > precision || secondVector6D[0] - firstVector6D[0] > precision )
            {
                return false;
            }
            if (firstVector6D[1] - secondVector6D[1] > precision || secondVector6D[1] - firstVector6D[1] > precision)
            {
                return false;
            }
            if (firstVector6D[2] - secondVector6D[2] > precision || secondVector6D[2] - firstVector6D[2] > precision)
            {
                return false;
            }
            if (firstVector6D[3] - secondVector6D[3] > precision || secondVector6D[3] - firstVector6D[3] > precision)
            {
                return false;
            }
            if (firstVector6D[4] - secondVector6D[4] > precision || secondVector6D[4] - firstVector6D[4] > precision)
            {
                return false;
            }
            if (firstVector6D[5] - secondVector6D[5] > precision || secondVector6D[5] - firstVector6D[5] > precision)
            {
                return false;
            }
            return true;
        }
    }
}
