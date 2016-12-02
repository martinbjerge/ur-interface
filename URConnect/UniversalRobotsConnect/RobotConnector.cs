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

            RobotModel = robotModel;  //todo fixme - big big ups .. 
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

            //string movetype = "movel";
            //string velocity = "0.4";

            //RealTimeClient.SendProgram($"def {movetype}():\n{movetype}(p[0.6, 0.606, -0.0302, 2.8509, 0.0054, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2, 0.605, -0.0302, 2.8341, 0.0076, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.6, 0.6167, -0.0336, 2.8142, 0.01, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2, 0.6159, -0.0339, 2.7911, 0.0123, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.6, 0.6273, -0.0375, 2.7664, 0.0144, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2, 0.6265, -0.0381, 2.7355, 0.0167, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.6, 0.6378, -0.042, 2.7028, 0.0187, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2, 0.6363, -0.0427, 2.6655, 0.0205, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6472, -0.0469, 2.6236, 0.0222, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6456, -0.048, 2.574, 0.0238, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6563, -0.0526, 2.5192, 0.0251, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6539, -0.054, 2.459, 0.0261, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.664, -0.0589, 2.3888, 0.027, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6611, -0.0507, 2.3047, 0.0276, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6702, -0.0659, 2.1975, 0.028, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2002, 0.666, -0.0476, 2.0403, 0.0278, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5002, 0.6732, -0.0716, 1.7941, 0.0265, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2002, 0.667, -0.0505, 1.4085, 0.0231, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5002, 0.6732, -0.0723, 1.0041, 0.0184, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2002, 0.6656, -0.0722, 0.5205, 0.0147, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5002, 0.6689, -0.056, 0.552, 0.0124, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6587, -0.0764, 0.4503, 0.0109, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.6, 0.6604, -0.0501, 0.38, 0.0099, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6492, -0.0803, 0.331, 0.0092, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6502, -0.0536, 0.2931, 0.0086, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6384, -0.0535, 0.2637, 0.0082, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6392, -0.0466, 0.2406, 0.0078, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6276, -0.0462, 0.2225, 0.0076, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6281, -0.0491, 0.2061, 0.0073, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6155, -0.0487, 0.1913, 0.0071, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.616, -0.0915, 0.1796, 0.0069, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.4645, -0.0907, 0.1706, 0.0068, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6054, -0.0533, 0.1622, 0.0066, -0.0], a = 0.4, v = {velocity}, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //while (RobotModel.RuntimeState != RuntimeState.Idle)
            //{
            //    Thread.Sleep(5);
            //}
            //Console.WriteLine("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!WE FINISHED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
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
            double delta = localRobotModel.RobotTimestamp - RobotModel.RobotTimestamp;
            if (delta > 0.008001)
            {
                log.Debug($"Too long since last robot timestamp {delta*1000} milliseconds!!!!  WE LOST A PACKAGE!!!!!");
                //Console.WriteLine($"Too long since last ROBOT TIMESTAMP {delta*1000} milliseconds!!!!  WE LOST A PACKAGE!!!!!");
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
