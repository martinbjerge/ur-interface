using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;
using UniversalRobotsConnect.Types;

namespace UniversalRobotsConnect
{
    class ForceTourqeReceiver
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        private NetworkStream _stream;
        private RobotModel _robotModel;
        private Thread _thread;

        public ForceTourqeReceiver(NetworkStream stream, RobotModel robotModel)
        {
            _stream = stream;
            _robotModel = robotModel;
            _thread = new Thread(Run);
            _thread.Start();
        }

        private void Run()
        {
            while (true)
            {
                if (_stream.DataAvailable)
                {
                    if (_stream.CanRead)
                    {
                        List<byte> bytelist = new List<byte>();
                        byte readByte;
                        while (true)
                        {
                            readByte = (byte)_stream.ReadByte();
                            bytelist.Add(readByte);
                            if (readByte == ')')
                            {
                                DecodePacage(Encoding.UTF8.GetString(bytelist.ToArray()));
                                bytelist.Clear();
                            }
                        }
                    }
                    else
                    {
                        log.Error("Can not read from this network stream");
                        throw new SystemException();
                    }
                }
            }
        }

        private void DecodePacage(string forceTourqePacage)
        {
            //log.Debug("ForceTourqe Recieved: " + forceTourqePacage);
            forceTourqePacage = forceTourqePacage.Remove(0, 1);
            forceTourqePacage = forceTourqePacage.Remove(forceTourqePacage.Length - 1, 1);
            string[] values = forceTourqePacage.Split(',');
            double x, y, z, rx, ry, rz;
            double.TryParse(values[0], out x);
            double.TryParse(values[1], out y);
            double.TryParse(values[2], out z);
            double.TryParse(values[3], out rx);
            double.TryParse(values[4], out ry);
            double.TryParse(values[5], out rz);
            _robotModel.ForceTourqe = new double[] {};
        }
    }
}
