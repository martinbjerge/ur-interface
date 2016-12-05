using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;
using log4net.Config;

namespace UniversalRobotsConnect
{
    public class RobotConnector
    {
        public RobotModel RobotModel;
        public RTDE RTDE;
        public RealTimeClient RealTimeClient;
        private ForceTourqe ForceTourqe;
        public DashboardClient DashboardClient;
        ConcurrentQueue<RobotModel> _robotData = new ConcurrentQueue<RobotModel>();

        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);
        private Thread _modelUpdaterThread;

        public RobotConnector(string ipAddress, bool hasForceTorque):this(new RobotModel(), ipAddress, hasForceTorque)
        {
            
        }

        public RobotConnector(RobotModel robotModel, string ipAddress, bool hasForceTorque)
        {
            Console.WriteLine("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     Initializing Robot     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
            FileInfo logFileInfo = new FileInfo(@"C:\SourceCode\ur-interface\URConnect\UniversalRobotsConnect\bin\Debug\Resources\logConfig.xml");
            XmlConfigurator.Configure(logFileInfo);
            

            log.Debug("Started Logging");

            RobotModel = robotModel;
            //RobotModel = new RobotModel();
            RobotModel.IpAddress = IPAddress.Parse(ipAddress);

            _modelUpdaterThread = new Thread(ReadRTDEData);
            _modelUpdaterThread.Start();

            RTDE = new RTDE(RobotModel, _robotData);
            RealTimeClient = new RealTimeClient(RobotModel);
            if (hasForceTorque)
            {
                ForceTourqe = new ForceTourqe(RobotModel);
            }
            DashboardClient = new DashboardClient(RobotModel);
            log.Debug("Started RobotConnector");


            //while (!robotModel.ClearToSend)
            //{
            //    Thread.Sleep(10);
            //}
            //log.Debug("Clear to send");
            Thread.Sleep(5000);
            Console.WriteLine("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   WE HAVE STARTED ROBOT    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
        }

        private void ReadRTDEData()
        {
            while (true)
            {
                RobotModel localRobotModel;
                if (_robotData.Count > 0)
                {
                    bool success = _robotData.TryDequeue(out localRobotModel);
                    if (success)
                    {
                        UpdateModel(localRobotModel);
                    }
                    if (_robotData.Count > 2)
                    {
                        log.Debug($"Robotmodels in queue: {_robotData.Count}");
                        //Console.WriteLine($"Robotmodels in queue: {_robotData.Count}");
                    }
                }
                Thread.Sleep(4);
            }
            
        }

        
        private void UpdateModel(RobotModel localRobotModel)
        {
            DateTime startTime = DateTime.Now;
            if (RobotModel.RobotTimestamp != 0)
            {
                double delta = localRobotModel.RobotTimestamp - RobotModel.RobotTimestamp;
                if (delta > 0.008001)
                {
                    log.Debug($"Too long since last robot timestamp {delta*1000} milliseconds!!!!  WE LOST A PACKAGE!!!!!");
                    //Console.WriteLine($"Too long since last ROBOT TIMESTAMP {delta*1000} milliseconds!!!!  WE LOST A PACKAGE!!!!!");
                }
            }

            RobotModel.ActualCurrent = localRobotModel.ActualCurrent;
            RobotModel.ActualExecutionTime = localRobotModel.ActualExecutionTime;
            RobotModel.ActualJointVoltage = localRobotModel.ActualJointVoltage;
            RobotModel.ActualMainVoltage = localRobotModel.ActualMainVoltage;
            RobotModel.ActualMomentum = localRobotModel.ActualMomentum;
            RobotModel.ActualQ = localRobotModel.ActualQ;
            RobotModel.ActualQD = localRobotModel.ActualQD;
            RobotModel.ActualRobotCurrent = localRobotModel.ActualRobotCurrent;
            RobotModel.ActualRobotVoltage = localRobotModel.ActualRobotVoltage;
            RobotModel.ActualTCPForce = localRobotModel.ActualTCPForce;
            RobotModel.ActualTCPPose = localRobotModel.ActualTCPPose;
            RobotModel.ActualTCPSpeed = localRobotModel.ActualTCPSpeed;
            RobotModel.ConfigurableInputBits.AllBits = localRobotModel.ConfigurableInputBits.AllBits;
            RobotModel.ConfigurableOutputBits.AllBits = localRobotModel.ConfigurableOutputBits.AllBits;

            RobotModel.DigitalInputbits.AllBits = localRobotModel.DigitalInputbits.AllBits;
            RobotModel.DigitalOutputBits.AllBits = localRobotModel.DigitalInputbits.AllBits;

            RobotModel.RuntimeState = localRobotModel.RuntimeState;
            RobotModel.StandardAnalogInput0 = localRobotModel.StandardAnalogInput0;
            RobotModel.StandardAnalogInput1 = localRobotModel.StandardAnalogInput1;
            RobotModel.StandardAnalogOutput0 = localRobotModel.StandardAnalogOutput;
            RobotModel.TargetMoment = localRobotModel.TargetMoment;
            RobotModel.TargetQ = localRobotModel.TargetQ;
            RobotModel.TargetQD = localRobotModel.TargetQD;
            RobotModel.TargetQDD = localRobotModel.TargetQDD;
            RobotModel.TargetSpeedFraction = localRobotModel.TargetSpeedFraction;
            RobotModel.TargetTCPPose = localRobotModel.TargetTCPPose;
            RobotModel.TargetTCPSpeed = localRobotModel.TargetTCPSpeed;
            RobotModel.ToolAnalogInput0 = localRobotModel.ToolAnalogInput0;
            RobotModel.ToolAnalogInput1 = localRobotModel.ToolAnalogInput1;
            RobotModel.ToolOutputCurrent = localRobotModel.ToolOutputCurrent;
            RobotModel.ToolOutputVoltage = localRobotModel.ToolOutputVoltage;

            TimeSpan realDelta = DateTime.Now - RobotModel.LastUpdateTimestamp;
            if (realDelta.TotalMilliseconds < 2)
            {
                Thread.Sleep(2);    //we want to allow time for clients to update 
            }
            if (realDelta.TotalMilliseconds > 32)
            {
                log.Debug($"Realtime {realDelta.TotalMilliseconds} MS since last update - too slow");
                //Console.WriteLine($"Realtime {realDelta.TotalMilliseconds} MS since last update - too slow");
            }
            RobotModel.LastUpdateTimestamp = DateTime.Now;
            RobotModel.RobotTimestamp = localRobotModel.RobotTimestamp;
            TimeSpan timespan = DateTime.Now - startTime;
            if (timespan.TotalMilliseconds > 4)
            {
                log.Debug($"Time to update model: {timespan.TotalMilliseconds}");
                //Console.WriteLine($"Time to update model: {timespan.TotalMilliseconds}");
            }

        }
    }
}
